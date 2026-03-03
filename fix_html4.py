import pathlib
import re

files_to_fix = [
    r'd:\coding\For antigravity\chat kara\templates\marketplace\caterer_list.html',
    r'd:\coding\For antigravity\chat kara\templates\navbar.html'
]

def remove_newlines(match):
    return match.group(0).replace('\n', ' ').replace('\r', ' ')

for fpath in files_to_fix:
    p = pathlib.Path(fpath)
    content = p.read_text('utf-8')
    content = re.sub(r'\{\{.*?\}\}', remove_newlines, content, flags=re.DOTALL)
    p.write_text(content, 'utf-8')
    print(f"Fixed newlines in {p.name}")
