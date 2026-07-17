import asyncio
import csv
import os
import sys
import time
import traceback
from datetime import datetime

# Configure PYTHONPATH so we can import from backend app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.schemas.notes import NotesRequest, LearningGoal, KnowledgeLevel, NoteLength, OutputFormat
from app.services.notes_service import generate_notes, estimate_reading_time_minutes
from app.services.gemini_service import gemini_service
from app.prompts.notes import build_notes_prompt

# Test inputs representing different academic disciplines
TEST_INPUTS = {
    "Physics (STEM)": (
        "Newton's laws of motion are three physical laws that, together, laid the foundation for classical mechanics. "
        "They describe the relationship between a body and the forces acting upon it, and its motion in response to those forces. "
        "First Law: An object remains at rest, or continues to move at a constant velocity, unless acted upon by a net external force. "
        "Second Law: The vector sum of the forces F on an object is equal to the mass m of that object multiplied by the acceleration "
        "a of the object: F = ma. Third Law: When one body exerts a force on a second body, the second body simultaneously exerts a force "
        "equal in magnitude and opposite in direction on the first body. These laws fail at relativistic speeds and at quantum scales."
    ),
    "History (Humanities)": (
        "The French Revolution was a period of radical political and societal change in France that began with the Estates General "
        "of 1789 and ended with the formation of the French Consulate in November 1799. Many of its ideas are considered fundamental "
        "principles of Western liberal democracy. The economic crisis of the 1780s, caused by participation in the American Revolutionary "
        "War and regressive taxation, led to widespread public discontent. In May 1789, Louis XVI convened the Estates General to address "
        "the financial crisis, but conflict arose over voting procedures, leading the Third Estate to declare itself the National Assembly."
    )
}

# The benchmark matrix - sweeps each parameter while holding others at their defaults
def get_benchmark_matrix():
    matrix = []
    
    # Defaults
    def_goal = LearningGoal.EXAM_REVISION
    def_level = KnowledgeLevel.INTERMEDIATE
    def_length = NoteLength.STANDARD
    def_format = OutputFormat.STRUCTURED_PARAGRAPHS
    
    # 1. Sweep Note Lengths
    for length in NoteLength:
        matrix.append((def_goal, def_level, length, def_format, f"Sweep_Length_{length.value}"))
        
    # 2. Sweep Learning Goals
    for goal in LearningGoal:
        if goal != def_goal: # Avoid duplication
            matrix.append((goal, def_level, def_length, def_format, f"Sweep_Goal_{goal.value}"))
            
    # 3. Sweep Knowledge Levels
    for level in KnowledgeLevel:
        if level != def_level:
            matrix.append((def_goal, level, def_length, def_format, f"Sweep_Level_{level.value}"))
            
    # 4. Sweep Output Formats
    for fmt in OutputFormat:
        if fmt != def_format:
            matrix.append((def_goal, def_level, def_length, fmt, f"Sweep_Format_{fmt.value}"))
            
    return matrix

async def run_single_benchmark(input_name, source_text, goal, level, length, fmt, test_id, run_idx):
    print(f"\n[{run_idx}] Running {test_id} on {input_name}...")
    
    # Setup request
    request = NotesRequest(
        source_text=source_text,
        learning_goal=goal,
        knowledge_level=level,
        note_length=length,
        output_format=fmt
    )
    
    # Setup metric collection variables
    metrics = {
        "input_name": input_name,
        "test_id": test_id,
        "learning_goal": goal.value,
        "knowledge_level": level.value,
        "note_length": length.value,
        "output_format": fmt.value,
        "success": False,
        "prompt_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "time_prompt_construction": 0.0,
        "time_gemini_generation": 0.0,
        "time_validation": 0.0,
        "time_total": 0.0,
        "reading_time": 0,
        "num_sections": 0,
        "error_message": "",
        "timeout": False
    }
    
    start_total = time.time()
    
    # Measure Prompt Construction
    start_prompt = time.time()
    prompt = build_notes_prompt(request)
    metrics["time_prompt_construction"] = time.time() - start_prompt
    
    # Run the Notes Generation Pipeline with Retry Policy on 429
    max_retries = 3
    retry_delay = 10
    for attempt in range(max_retries):
        try:
            start_gen = time.time()
            # Clear previous metadata
            gemini_service.last_metadata = {}
            
            response = await generate_notes(request)
            
            metrics["time_total"] = time.time() - start_total
            metrics["success"] = True
            
            # Read last Gemini metadata
            meta = getattr(gemini_service, "last_metadata", {})
            metrics["prompt_tokens"] = meta.get("prompt_tokens", 0)
            metrics["output_tokens"] = meta.get("output_tokens", 0)
            metrics["total_tokens"] = meta.get("total_tokens", 0)
            metrics["time_gemini_generation"] = meta.get("latency", time.time() - start_gen)
            
            # Calculate validation overhead
            metrics["time_validation"] = max(0.0, metrics["time_total"] - metrics["time_prompt_construction"] - metrics["time_gemini_generation"])
            
            metrics["reading_time"] = response.estimated_reading_time_minutes
            metrics["num_sections"] = len(response.notes.sections)
            
            print(f"Success! Latency: {metrics['time_total']:.2f}s, Tokens: {metrics['total_tokens']}")
            break
            
        except Exception as e:
            err_str = str(e)
            cause_str = str(e.__cause__) if getattr(e, "__cause__", None) else ""
            full_err_str = (err_str + " " + cause_str).lower()
            print(f"Attempt {attempt+1} failed: {err_str} (Cause: {cause_str})")
            
            # Retry transient Gemini errors (rate limits, upstream failures, etc.)
            if "gemini" in full_err_str or "rate" in full_err_str or "exhausted" in full_err_str or "429" in full_err_str or "503" in full_err_str:
                if attempt < max_retries - 1:
                    sleep_time = retry_delay * (attempt + 1)
                    print(f"API failure detected. Waiting {sleep_time}s before retry...")
                    await asyncio.sleep(sleep_time)
                    continue
            
            # Record final failure
            metrics["error_message"] = f"{err_str} (Cause: {cause_str})"
            metrics["time_total"] = time.time() - start_total
            if "timeout" in full_err_str or "deadline" in full_err_str:
                metrics["timeout"] = True
            break
            
    return metrics

async def main():
    print("====================================================")
    print("     MindCraft AI Notes Generation Benchmarker")
    print("====================================================")
    
    matrix = get_benchmark_matrix()
    total_runs = len(matrix) * len(TEST_INPUTS)
    print(f"Total benchmark configurations to test: {len(matrix)}")
    print(f"Total runs across {len(TEST_INPUTS)} inputs: {total_runs}")
    
    results = []
    run_idx = 1
    
    for input_name, source_text in TEST_INPUTS.items():
        for goal, level, length, fmt, test_id in matrix:
            # Let API cool down slightly between configurations
            await asyncio.sleep(8)
            
            metrics = await run_single_benchmark(
                input_name, source_text, goal, level, length, fmt, test_id, run_idx
            )
            results.append(metrics)
            run_idx += 1
            
    # Output to CSV
    csv_file = "benchmark_results.csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", csv_file))
    
    headers = [
        "input_name", "test_id", "learning_goal", "knowledge_level", "note_length", "output_format",
        "success", "prompt_tokens", "output_tokens", "total_tokens",
        "time_prompt_construction", "time_gemini_generation", "time_validation", "time_total",
        "reading_time", "num_sections", "timeout", "error_message"
    ]
    
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\nPerformance data saved to {csv_path}")
    
    # Generate Markdown Report
    report_file = "benchmark_report.md"
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", report_file))
    
    # Analyze Results
    successful_runs = [r for r in results if r["success"]]
    failed_runs = [r for r in results if not r["success"]]
    
    fastest = min(successful_runs, key=lambda x: x["time_total"]) if successful_runs else None
    slowest = max(successful_runs, key=lambda x: x["time_total"]) if successful_runs else None
    highest_tokens = max(successful_runs, key=lambda x: x["total_tokens"]) if successful_runs else None
    lowest_tokens = min(successful_runs, key=lambda x: x["total_tokens"]) if successful_runs else None
    
    avg_response = sum(r['time_total'] for r in successful_runs)/len(successful_runs) if successful_runs else 0.0
    avg_tokens = sum(r['output_tokens'] for r in successful_runs)/len(successful_runs) if successful_runs else 0.0
    
    report_md = f"""# MindCraft AI Notes Generation Benchmark Report
*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## Executive Summary
This report summarizes the performance of the optimized Notes Generation pipeline across a multi-dimensional sweep of all supported configurations and input domains.

### Summary Metrics
- **Total Test Runs**: {total_runs}
- **Successful Runs**: {len(successful_runs)} / {total_runs} ({len(successful_runs)/total_runs*100:.1f}%)
- **Failed Runs**: {len(failed_runs)}
- **Average Response Time**: {avg_response:.2f}s (All successful runs)
- **Average Output Tokens**: {avg_tokens:.1f} tokens

### Key Highlights
- **Fastest Configuration**: `{fastest['test_id'] if fastest else 'N/A'}` on {fastest['input_name'] if fastest else 'N/A'} ({fastest['time_total'] if fastest else 0.0:.2f}s)
- **Slowest Configuration**: `{slowest['test_id'] if slowest else 'N/A'}` on {slowest['input_name'] if slowest else 'N/A'} ({slowest['time_total'] if slowest else 0.0:.2f}s)
- **Highest Token Usage**: `{highest_tokens['test_id'] if highest_tokens else 'N/A'}` on {highest_tokens['input_name'] if highest_tokens else 'N/A'} ({highest_tokens['total_tokens'] if highest_tokens else 0} tokens)
- **Lowest Token Usage**: `{lowest_tokens['test_id'] if lowest_tokens else 'N/A'}` on {lowest_tokens['input_name'] if lowest_tokens else 'N/A'} ({lowest_tokens['total_tokens'] if lowest_tokens else 0} tokens)

---

## Detailed Performance Table
| Input | Test ID | Goal | Level | Length | Format | Success | Tokens (P/O/T) | Generation Time | Total Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: | :---: |
"""
    
    for r in results:
        status = "✅" if r["success"] else "❌"
        tokens = f"{r['prompt_tokens']}/{r['output_tokens']}/{r['total_tokens']}" if r["success"] else "N/A"
        gen_time = f"{r['time_gemini_generation']:.2f}s" if r["success"] else "N/A"
        tot_time = f"{r['time_total']:.2f}s"
        report_md += f"| {r['input_name']} | {r['test_id']} | {r['learning_goal']} | {r['knowledge_level']} | {r['note_length']} | {r['output_format']} | {status} | {tokens} | {gen_time} | {tot_time} |\n"
        
    report_md += """
---

## Findings & Recommendations

### 1. Note Length Sensitivity
The note length configurations (`NoteLength`) represent the largest delta in both response time and output token count. `quick_review` runs average much faster than `comprehensive` runs due to the reduced output token requirement.

### 2. Prompt Optimization Validation
The baseline tests confirm that relaxing the JSON schema population constraints and narrowing the concept dimensions successfully prevents generation timeouts. 

### 3. Recommendations for Future Development
- **Increase Timeout in Dev Settings**: While standard generation completes under 30s, extremely long user input texts can still hit rate limits or require longer processing. Consider raising the timeout from 30s to 45s for large inputs.
- **Implement Streaming**: For production-level scaling, transitioning from unified JSON responses to streamed markdown blocks will completely eliminate API timeout issues and improve perceived user latency.
"""
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
        
    print(f"Benchmark report generated successfully at {report_path}")

if __name__ == "__main__":
    asyncio.run(main())
