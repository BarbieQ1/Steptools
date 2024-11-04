import os
import subprocess
import tempfile
import sys
import importlib
import zipfile
import tkinter as tk
from tkinter import messagebox
import shutil

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
root.geometry("500x400")
root.configure(bg="#333333")

if not os.path.isdir(extracted_dir):
    messagebox.showerror("Error", f"The directory '{extracted_dir}' was not found.")
    root.destroy()

def list_scripts():
    return [os.path.splitext(f)[0] for f in os.listdir(extracted_dir) if f.endswith(".pyw")]

def run_script(script_name):
    script_path = os.path.join(extracted_dir, script_name + ".pyw")
    check_and_install_modules(script_path)
    subprocess.Popen([python_executable, script_path], shell=True)

title_label = tk.Label(root, text="Steptools Scripts", font=("Helvetica", 20, "bold"), fg="white", bg="#333333")
title_label.pack(pady=20)

frame = tk.Frame(root, bg="#333333")
frame.pack(fill="both", expand=True, padx=20, pady=10)

listbox = tk.Listbox(frame, bg="#444444", fg="#ffffff", selectbackground="#555555", highlightthickness=0, bd=0, font=("Helvetica", 12), height=10)
listbox.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)

for script in list_scripts():
    listbox.insert("end", script)

def execute_selected_script():
    selected_script = listbox.get(listbox.curselection())
    if selected_script:
        run_script(selected_script)

execute_button = tk.Button(root, text="Run Script", command=execute_selected_script, width=20, height=2, bg="#555555", fg="white", font=("Helvetica", 12))
execute_button.pack(pady=20)

root.mainloop()
