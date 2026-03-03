import pathlib
import glob
import re

html_files = glob.glob(r'd:\coding\For antigravity\chat kara\templates\**\*.html', recursive=True)

def remove_newlines(match):
    return match.group(0).replace('\n', ' ').replace('\r', ' ')

for fpath in html_files:
    p = pathlib.Path(fpath)
    content = p.read_text('utf-8')
    if '{{' in content:
        new_content = re.sub(r'\{\{.*?\}\}', remove_newlines, content, flags=re.DOTALL)
        if new_content != content:
            p.write_text(new_content, 'utf-8')
            print(f"Fixed newlines in {p.name}")
print("Finished fixing template tags across the project.")
