import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/caterer/1/royal-feast-catering/')
    html = response.read().decode('utf-8')
    if '{{' in html:
        print("Raw tags found:", [line.strip() for line in html.split('\n') if '{{' in line])
    else:
        print("No raw tags found. Rendered perfectly!")
except urllib.error.HTTPError as e:
    print("STATUS:", e.getcode())
