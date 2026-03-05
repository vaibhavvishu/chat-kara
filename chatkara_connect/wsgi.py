import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Add the project root to the python path
path = Path(__file__).resolve().parent.parent
if str(path) not in sys.path:
    sys.path.append(str(path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatkara_connect.settings')
application = get_wsgi_application()

# Vercel serverless function expects a variable named 'app'
app = application
