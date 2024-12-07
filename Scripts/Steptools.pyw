import os
import subprocess
import tempfile
import sys
import importlib
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox, Menu
import shutil
import requests
import filecmp
import webbrowser

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
root.title("Steptools Launcher")
root.geometry("500x700")
root.configure(bg="#333333")

if not os.path.isdir(extracted_dir):
    messagebox.showerror("Error", f"The directory '{extracted_dir}' was not found.")
    root.destroy()

new_version_available = False

def is_new_version_available():
    github_script_url = "https://raw.githubusercontent.com/BarbieQ1/Steptools/main/Steptools.py"
    response = requests.get(github_script_url)
    if response.status_code == 200:
        github_script_code = response.text.strip()
        local_script_path = os.path.join(extracted_dir, "Steptools.py")
        if os.path.exists(local_script_path):
            with open(local_script_path, "r") as local_file:
                local_script_code = local_file.read().strip()
            return github_script_code != local_script_code
        else:
            return True
    return False

def update_local_script():
    github_script_url = "https://raw.githubusercontent.com/BarbieQ1/Steptools/main/Steptools.py"
    response = requests.get(github_script_url)
    if response.status_code == 200:
        local_script_path = os.path.join(extracted_dir, "Steptools.py")
        with open(local_script_path, "w") as local_file:
            local_file.write(response.text)
        root.destroy()
        subprocess.Popen([python_executable, local_script_path], shell=True)

new_version_available = is_new_version_available()

def list_scripts():
    scripts = {}
    for f in os.listdir(extracted_dir):
        if f.endswith(".pyw") and f != "Steptools.pyw":
            script_name, _ = os.path.splitext(f)
            parts = script_name.split("#")
            if len(parts) == 3:
                category, subcategory, name = parts
            elif len(parts) == 2:
                category, name = parts
                subcategory = None
            else:
                category = "Uncategorized"
                subcategory = None
                name = script_name
            category = category.strip()
            name = name.strip()
            subcategory = subcategory.strip() if subcategory else None
            if category not in scripts:
                scripts[category] = {}
            if subcategory:
                if subcategory not in scripts[category]:
                    scripts[category][subcategory] = []
                scripts[category][subcategory].append(name)
            else:
                if None not in scripts[category]:
                    scripts[category][None] = []
                scripts[category][None].append(name)
    return scripts

def run_script(script_name, category, subcategory):
    if subcategory:
        script_path = os.path.join(extracted_dir, f"{category}#{subcategory}#{script_name}.pyw")
    else:
        script_path = os.path.join(extracted_dir, f"{category}#{script_name}.pyw")
    check_and_install_modules(script_path)
    subprocess.Popen([python_executable, script_path], shell=True)

title_label = tk.Label(root, text="Steptools Scripts", font=("Helvetica", 20, "bold"), fg="white", bg="#333333")
title_label.pack(pady=20)

refresh_button = tk.Button(root, text="↻", command=lambda: refresh_app(), font=("Helvetica", 15), fg="white", bg="#555555")
refresh_button.place(relx=0.95, rely=0.05, anchor="ne")

if new_version_available:
    version_label = tk.Label(root, text="New Version available", font=("Helvetica", 10, "italic"), fg="red", bg="#333333", cursor="hand2")
    version_label.pack()
    update_button = tk.Button(root, text="Update", font=("Helvetica", 10), fg="white", bg="#555555", command=update_local_script)
    update_button.pack(pady=5)

frame = tk.Frame(root, bg="#333333")
frame.pack(fill="both", expand=True, padx=20, pady=10)

scripts = list_scripts()

accordion = ttk.Notebook(frame)
accordion.pack(fill="both", expand=True)

style = ttk.Style()
style.configure("TFrame", background="#333333")
style.configure("TButton", background="#555555", foreground="white")
style.configure("TNotebook", tabposition="n")
style.configure("TNotebook.Tab", font=("Helvetica", 12), padding=[5, 5])

active_categories = {category: tk.BooleanVar(value=(category == 'Lost Ark')) for category in scripts}

def update_accordion():
    for tab in accordion.tabs():
        accordion.forget(tab)
    for category, subcategories in scripts.items():
        if active_categories[category].get():
            category_frame = ttk.Frame(accordion)
            accordion.add(category_frame, text=category)
            for subcategory, script_list in subcategories.items():
                if subcategory:
                    subcategory_label = tk.Label(category_frame, text=subcategory, font=("Helvetica", 14, "bold"), fg="white", bg="#333333")
                    subcategory_label.pack(pady=(10, 5))
                for script in script_list:
                    button = tk.Button(category_frame, text=script, command=lambda s=script, c=category, sc=subcategory: run_script(s, c, sc), width=30, height=2, bg="#555555", fg="white", font=("Helvetica", 12))
                    button.pack(pady=5, padx=10)

update_accordion()

def show_context_menu():
    context_menu = tk.Toplevel(root)
    context_menu.title("Category Selection")
    context_menu.geometry("250x400")
    context_menu.configure(bg="#333333")
    for category, var in active_categories.items():
        checkbox = tk.Checkbutton(context_menu, text=category, variable=var, font=("Helvetica", 12), fg="white", bg="#333333", selectcolor="#555555", command=update_accordion)
        checkbox.pack(anchor="w", pady=5, padx=10)

def refresh_app():
    root.destroy()
    subprocess.Popen([python_executable, __file__], shell=True)

menu_button = tk.Button(root, text="...", command=show_context_menu, font=("Helvetica", 15), fg="white", bg="#555555")
menu_button.place(relx=0.9, rely=0.05, anchor="ne")

root.mainloop()
