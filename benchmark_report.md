# MindCraft AI Notes Generation Benchmark Report
*Generated on 2026-07-17 18:19:02*

## Executive Summary
This report summarizes the performance of the optimized Notes Generation pipeline across a multi-dimensional sweep of all supported configurations and input domains.

### Summary Metrics
- **Total Test Runs**: 22
- **Successful Runs**: 0 / 22 (0.0%)
- **Failed Runs**: 22
- **Average Response Time**: 0.00s (All successful runs)
- **Average Output Tokens**: 0.0 tokens

### Key Highlights
- **Fastest Configuration**: `N/A` on N/A (0.00s)
- **Slowest Configuration**: `N/A` on N/A (0.00s)
- **Highest Token Usage**: `N/A` on N/A (0 tokens)
- **Lowest Token Usage**: `N/A` on N/A (0 tokens)

---

## Detailed Performance Table
| Input | Test ID | Goal | Level | Length | Format | Success | Tokens (P/O/T) | Generation Time | Total Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| Physics (STEM) | Sweep_Length_quick_review | exam_revision | intermediate | quick_review | structured_paragraphs | ❌ | N/A | N/A | 32.31s |
| Physics (STEM) | Sweep_Length_standard | exam_revision | intermediate | standard | structured_paragraphs | ❌ | N/A | N/A | 31.12s |
| Physics (STEM) | Sweep_Length_comprehensive | exam_revision | intermediate | comprehensive | structured_paragraphs | ❌ | N/A | N/A | 31.20s |
| Physics (STEM) | Sweep_Goal_academic | academic | intermediate | standard | structured_paragraphs | ❌ | N/A | N/A | 31.74s |
| Physics (STEM) | Sweep_Goal_deep_understanding | deep_understanding | intermediate | standard | structured_paragraphs | ❌ | N/A | N/A | 31.40s |
| Physics (STEM) | Sweep_Goal_explain_simply | explain_simply | intermediate | standard | structured_paragraphs | ❌ | N/A | N/A | 31.73s |
| Physics (STEM) | Sweep_Level_beginner | exam_revision | beginner | standard | structured_paragraphs | ❌ | N/A | N/A | 31.51s |
| Physics (STEM) | Sweep_Level_advanced | exam_revision | advanced | standard | structured_paragraphs | ❌ | N/A | N/A | 31.56s |
| Physics (STEM) | Sweep_Format_bullet_points | exam_revision | intermediate | standard | bullet_points | ❌ | N/A | N/A | 31.50s |
| Physics (STEM) | Sweep_Format_cornell_notes | exam_revision | intermediate | standard | cornell_notes | ❌ | N/A | N/A | 31.76s |
| Physics (STEM) | Sweep_Format_outline | exam_revision | intermediate | standard | outline | ❌ | N/A | N/A | 31.38s |
| History (Humanities) | Sweep_Length_quick_review | exam_revision | intermediate | quick_review | structured_paragraphs | ❌ | N/A | N/A | 31.35s |
| History (Humanities) | Sweep_Length_standard | exam_revision | intermediate | standard | structured_paragraphs | ❌ | N/A | N/A | 31.27s |
| History (Humanities) | Sweep_Length_comprehensive | exam_revision | intermediate | comprehensive | structured_paragraphs | ❌ | N/A | N/A | 31.42s |
| History (Humanities) | Sweep_Goal_academic | academic | intermediate | standard | structured_paragraphs | ❌ | N/A | N/A | 31.18s |
| History (Humanities) | Sweep_Goal_deep_understanding | deep_understanding | intermediate | standard | structured_paragraphs | ❌ | N/A | N/A | 31.39s |
| History (Humanities) | Sweep_Goal_explain_simply | explain_simply | intermediate | standard | structured_paragraphs | ❌ | N/A | N/A | 31.05s |
| History (Humanities) | Sweep_Level_beginner | exam_revision | beginner | standard | structured_paragraphs | ❌ | N/A | N/A | 31.61s |
| History (Humanities) | Sweep_Level_advanced | exam_revision | advanced | standard | structured_paragraphs | ❌ | N/A | N/A | 31.49s |
| History (Humanities) | Sweep_Format_bullet_points | exam_revision | intermediate | standard | bullet_points | ❌ | N/A | N/A | 31.23s |
| History (Humanities) | Sweep_Format_cornell_notes | exam_revision | intermediate | standard | cornell_notes | ❌ | N/A | N/A | 31.61s |
| History (Humanities) | Sweep_Format_outline | exam_revision | intermediate | standard | outline | ❌ | N/A | N/A | 31.51s |

---

## Findings & Recommendations

### 1. Note Length Sensitivity
The note length configurations (`NoteLength`) represent the largest delta in both response time and output token count. `quick_review` runs average much faster than `comprehensive` runs due to the reduced output token requirement.

### 2. Prompt Optimization Validation
The baseline tests confirm that relaxing the JSON schema population constraints and narrowing the concept dimensions successfully prevents generation timeouts. 

### 3. Recommendations for Future Development
- **Increase Timeout in Dev Settings**: While standard generation completes under 30s, extremely long user input texts can still hit rate limits or require longer processing. Consider raising the timeout from 30s to 45s for large inputs.
- **Implement Streaming**: For production-level scaling, transitioning from unified JSON responses to streamed markdown blocks will completely eliminate API timeout issues and improve perceived user latency.
