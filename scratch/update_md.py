import sys

with open('docs/PROJECT_CONTEXT.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('* Milestone 9 \u2014 Reading Themes: **Complete**', '* Milestone 9 \u2014 Reading Themes: **Complete**\n  * Milestone 10 \u2014 Configurable Quiz & Flashcards: **Complete**')
content = content.replace('* Milestone 9 \u2013 Reading Themes: **Complete**', '* Milestone 9 \u2013 Reading Themes: **Complete**\n  * Milestone 10 \u2013 Configurable Quiz & Flashcards: **Complete**')

# The exact dash character used is different, let's just do a generic replacement
import re
content = re.sub(
    r'\* Milestone 9 (.*?) Reading Themes: \*\*Complete\*\*',
    r'* Milestone 9 \1 Reading Themes: **Complete**\n  * Milestone 10 \1 Configurable Quiz and Flashcards: **Complete**',
    content
)

with open('docs/PROJECT_CONTEXT.md', 'w', encoding='utf-8') as f:
    f.write(content)
