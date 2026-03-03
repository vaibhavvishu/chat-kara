import pathlib
import re

file_path = pathlib.Path(r'd:\coding\For antigravity\chat kara\templates\marketplace\caterer_list.html')
content = file_path.read_text('utf-8')

# Fix category stringformat by replacing the entire block
pattern = re.compile(r'{%\s*if\s+request_GET\.category\s*==\s*cat\.id\|stringformat:"s"\s*%}')
content = pattern.sub('{% if request_GET.category == cat.id|stringformat:"s" %}', content)

file_path.write_text(content, 'utf-8')
print("Successfully fixed template tag newlines.")
