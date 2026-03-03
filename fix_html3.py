import pathlib
import re

file_path = pathlib.Path(r'd:\coding\For antigravity\chat kara\templates\marketplace\caterer_detail.html')
content = file_path.read_text('utf-8')

# Regex to safely replace all newlines within {{ ... }} blocks with spaces
# This uses a simple replacement logic since {{ }} typically don't nest.
import sys
# Replace `{{ \n... }}` with `{{ ... }}`
def remove_newlines(match):
    return match.group(0).replace('\n', ' ').replace('\r', ' ')

# Need to find any occurrences of {{ followed by anything, then }}
# re.sub(r'\{\{.*?\}\}', remove_newlines, content, flags=re.DOTALL)
content = re.sub(r'\{\{.*?\}\}', remove_newlines, content, flags=re.DOTALL)

file_path.write_text(content, 'utf-8')
print("Successfully fixed template tag newlines in caterer_detail.html.")
