import subprocess, sys, tempfile, os, time, threading

def install(m):
    try:
        subprocess.check_call([sys.executable.replace("pythonw.exe", "python.exe"), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable.replace("pythonw.exe", "python.exe"), "-m", "pip", "install", m])
    except subprocess.CalledProcessError as e:
        print(f"Error installing {m}: {e}")
        sys.exit(f"Failed to install {m}. Exiting...")

try: import pyperclip
except ImportError: install("pyperclip"); import pyperclip

try: import requests
except ImportError: install("requests"); import requests

try: import psutil
except ImportError: install("psutil"); import psutil

url = "https://raw.githubusercontent.com/BarbieQ1/Steptools/main/Scripts/Steptools.pyw"

def show_loader():
    from tkinter import Tk, Label, StringVar
    root = Tk()
    root.title("Loading..."); root.geometry("300x100"); root.resizable(False, False)
    status_text = StringVar(); status_text.set("Loading Steptools Launcher...")
    Label(root, textvariable=status_text, font=("Arial", 12)).pack(expand=True)

    def close_loader():
        while loading: time.sleep(0.1)
        root.quit()

    threading.Thread(target=close_loader, daemon=True).start()
    root.mainloop()

def is_launcher_open():
    try:
        for p in psutil.process_iter(attrs=['name', 'cmdline']):
            if p.info and 'Steptools' in (p.info.get('name') or ''): return True
            if p.info.get('cmdline') and any('Steptools' in arg for arg in p.info['cmdline']): return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError): pass
    return False

loading = True

try:
    threading.Thread(target=show_loader, daemon=True).start()
    response = requests.get(url); response.raise_for_status()
    code = response.text
    script_path = os.path.join(tempfile.gettempdir(), "Steptools_temp.pyw")
    with open(script_path, "w", encoding="utf-8") as f: f.write(code)
    subprocess.Popen([sys.executable.replace("python.exe", "pythonw.exe"), script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    while not is_launcher_open(): time.sleep(0.01)

    loading = False
except Exception as e: loading = False; sys.exit(f"Error: {e}")
