import glob
import re
import os

# Spanish conjunctions and prepositions to prevent ending a line
words = ['y', 'e', 'o', 'u', 'a', 'de', 'en', 'con', 'por', 'para', 'como', 'que', 'del', 'al']

# Match word boundary, word, word boundary, and then spaces
pattern = r'\b(' + '|'.join(words) + r')\b[ \t\r\n]+'
regex = re.compile(pattern, re.IGNORECASE)

def replace_in_text(text):
    if not text.strip():
        return text
    # Replace the whitespace following the matched word with &nbsp;
    return regex.sub(r'\1&nbsp;', text)

def process_html(html_content):
    # Split HTML by tags (preserving the tags in the list)
    parts = re.split(r'(<[^>]+>)', html_content)
    new_parts = []
    
    in_script = False
    in_style = False
    in_comment = False
    
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            tag_lower = part.lower()
            
            # Comment checks
            if tag_lower.startswith('<!--'):
                in_comment = True
            
            # Script checks
            if tag_lower.startswith('<script'):
                in_script = True
            elif tag_lower.startswith('</script'):
                in_script = False
                
            # Style checks
            if tag_lower.startswith('<style'):
                in_style = True
            elif tag_lower.startswith('</style'):
                in_style = False
                
            new_parts.append(part)
            
            # If the comment ends in this tag
            if tag_lower.endswith('-->'):
                in_comment = False
        else:
            if in_script or in_style or in_comment:
                new_parts.append(part)
            else:
                new_parts.append(replace_in_text(part))
                
    return ''.join(new_parts)

# Apply to all files in the workspace (excluding .git and .old directories)
html_files = []
for root, dirs, files in os.walk('.'):
    # Exclude .git and .old directories
    dirs[:] = [d for d in dirs if d not in ('.git', '.old', '.gemini', 'agy-sbx-kit')]
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for f in sorted(html_files):
    print("Processing:", f)
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = process_html(content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)

print("Replacement complete.")
