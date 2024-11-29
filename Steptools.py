import os
import subprocess
import tempfile
import sys
import importlib
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import requests
import filecmp
import webbrowser1

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def install_standard_modules():
    essential_modules = ["Pillow", "pyperclip"]
    for module in essential_modules:
        try:
            importlib.import_module(module.lower() if module != "Pillow" else module)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

install_standard_modules()

def check_and_install_modules(script_path):
    missing_modules = []
    with open(script_path, "r") as script:
        for line in script:
            if line.startswith("import ") or line.startswith("from "):
                parts = line.split()
                module_name = parts[1].split(".")[0].strip(",")
                if module_name not in sys.builtin_module_names:
                    try:
                        importlib.import_module(module_name)
                    except ImportError:
                        if module_name == "PIL":
                            missing_modules.append("Pillow")
                        else:
                            missing_modules.append(module_name)
    for module in missing_modules:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

REPO_URL = "https://github.com/BarbieQ1/Steptools/archive/refs/heads/main.zip"

temp_dir = tempfile.mkdtemp()

zip_path = os.path.join(temp_dir, "Steptools.zip")
response = requests.get(REPO_URL)
with open(zip_path, "wb") as f:
    f.write(response.content)

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(temp_dir)

extracted_dir = os.path.join(temp_dir, "Steptools-main", "Scripts")

python_executable = sys.executable

root = tk.Tk()
root.title("Steptools PYw-Script Launcher")
root.geometry("500x600")
root.configure(bg="#333333")

if not os.path.isdir(extracted_dir):
    messagebox.showerror("Error", f"The directory '{extracted_dir}' was not found.")
    root.destroy()

# Check if the local script matches the version on GitHub
def is_new_version_available():
    local_script_path = os.path.join(temp_dir, "Steptools.py")
    github_script_url = "https://raw.githubusercontent.com/BarbieQ1/Steptools/main/Steptools.py"
    response = requests.get(github_script_url)
    if response.status_code == 200:
        github_script_path = os.path.join(temp_dir, "Steptools_github.py")
        with open(github_script_path, "w") as f:
            f.write(response.text)
        if os.path.exists(local_script_path):
            return not filecmp.cmp(local_script_path, github_script_path, shallow=False)
    return False

new_version_available = is_new_version_available()

def list_scripts():
    scripts = {}
    for f in os.listdir(extracted_dir):
        if f.endswith(".pyw"):
            script_name, _ = os.path.splitext(f)
            if "#" in script_name:
                category, name = script_name.split("#", 1)
                category = category.strip()
                name = name.strip()
            else:
                category = "Uncategorized"
                name = script_name
            if category not in scripts:
                scripts[category] = []
            scripts[category].append(name)
    return scripts

def run_script(script_name, category):
    script_path = os.path.join(extracted_dir, f"{category}#{script_name}.pyw")
    check_and_install_modules(script_path)
    subprocess.Popen([python_executable, script_path], shell=True)

title_label = tk.Label(root, text="Steptools Scripts", font=("Helvetica", 20, "bold"), fg="white", bg="#333333")
title_label.pack(pady=20)

if new_version_available:
    version_label = tk.Label(root, text="New Version available", font=("Helvetica", 10, "italic"), fg="red", bg="#333333", cursor="hand2")
    version_label.pack()
    version_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/BarbieQ1/Steptools"))

frame = tk.Frame(root, bg="#333333")
frame.pack(fill="both", expand=True, padx=20, pady=10)

scripts = list_scripts()

accordion = ttk.Notebook(frame)
accordion.pack(fill="both", expand=True)

style = ttk.Style()
style.configure("TFrame", background="#333333")
style.configure("TButton", background="#555555", foreground="white")

for category, script_list in scripts.items():
    category_frame = ttk.Frame(accordion)
    accordion.add(category_frame, text=category)

    for script in script_list:
        button = tk.Button(category_frame, text=script, command=lambda s=script, c=category: run_script(s, c), width=30, height=2, bg="#555555", fg="white", font=("Helvetica", 12))
        button.pack(pady=5, padx=10)

root.mainloop()
