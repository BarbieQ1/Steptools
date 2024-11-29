import requests, subprocess, sys, tempfile, os, time, threading
from tkinter import Tk, Label, StringVar
import psutil

def install(module): 
    subprocess.run([sys.executable, "-m", "pip", "install", module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try: 
    import psutil
except ImportError: 
    install("psutil")
    import psutil

url = "https://raw.githubusercontent.com/BarbieQ1/Steptools/main/Scripts/Steptools.pyw"

def show_loader():
    root = Tk()
    root.title("Loading...")
    root.geometry("300x100")
    root.resizable(False, False)
    status_text = StringVar()
    status_text.set("Loading Steptools Launcher...")
    label = Label(root, textvariable=status_text, font=("Arial", 12))
    label.pack(expand=True)

    def close_loader():
        while loading:
            time.sleep(0.1)
        root.quit()

    threading.Thread(target=close_loader, daemon=True).start()
    root.mainloop()

def is_launcher_open():
    try:
        for proc in psutil.process_iter(attrs=['name', 'cmdline']):
            if proc.info and 'Steptools' in (proc.info.get('name') or ''):
                return True
            if proc.info.get('cmdline') and any('Steptools' in arg for arg in proc.info['cmdline']):
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
        pass
    return False

loading = True

try:
    threading.Thread(target=show_loader, daemon=True).start()
    response = requests.get(url)
    response.raise_for_status()
    code = response.text
    temp_dir = tempfile.gettempdir()
    script_path = os.path.join(temp_dir, "Steptools_temp.pyw")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)
    subprocess.Popen([sys.executable.replace("python.exe", "pythonw.exe"), script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    while not is_launcher_open():
        time.sleep(0.01)

    loading = False
except Exception as e:
    loading = False
    sys.exit(f"Error while launching Steptools Launcher: {e}")
