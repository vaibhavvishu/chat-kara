import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/caterers/')
    print("STATUS:", response.getcode())
except urllib.error.HTTPError as e:
    print("STATUS:", e.getcode())
    error_html = e.read().decode('utf-8')
    import re
    # Extract the exception value block from django error page
    match = re.search(r'Exception Value:.*?<pre[^>]*>(.*?)</pre>', error_html, re.DOTALL)
    if match:
        print("EXCEPTION VALUE:")
        print(match.group(1).strip())
    else:
        print("Could not find exception value in HTML.")
        print("Here is a snippet:")
        print(error_html[:1000])
