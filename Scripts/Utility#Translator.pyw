import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import threading
import pyperclip

def translate_text():
    input_text = input_field.get("1.0", tk.END).strip()
    target_language = language_dropdown.get()
    if input_text:
        threading.Thread(target=perform_translation, args=(input_text, target_language)).start()

def perform_translation(input_text, target_language):
    translator = Translator()
    try:
        translated = translator.translate(input_text, dest=language_codes[target_language])
        output_field.delete("1.0", tk.END)
        output_field.insert(tk.END, translated.text)
    except Exception:
        output_field.delete("1.0", tk.END)
        output_field.insert(tk.END, "Translation Error")

def paste_text():
    input_field.delete("1.0", tk.END)
    input_field.insert(tk.END, pyperclip.paste())
    translate_text()

def copy_text():
    output_text = output_field.get("1.0", tk.END).strip()
    pyperclip.copy(output_text)

app = tk.Tk()
app.title("Translator")
app.configure(bg="#2E2E2E")
app.geometry("700x300")

bg_color = "#2E2E2E"
fg_color = "#D3D3D3"
accent_color = "#3C3F41"
button_color = "#44475A"
highlight_color = "#61AFEF"

language_codes = {"English": "en", "German": "de", "Spanish": "es", "French": "fr", "Italian": "it", "Chinese": "zh-cn", "Russian": "ru", "Japanese": "ja", "Korean": "ko"}

input_label = tk.Label(app, text="Input", fg=fg_color, bg=bg_color, font=("Arial", 14, "bold"))
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

input_field = tk.Text(app, height=10, width=40, bg=accent_color, fg=fg_color, insertbackground=fg_color, highlightbackground=highlight_color, highlightthickness=1, relief="flat")
input_field.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
input_field.bind("<KeyRelease>", lambda event: translate_text())

output_label = tk.Label(app, text="Output", fg=fg_color, bg=bg_color, font=("Arial", 14, "bold"))
output_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

output_field = tk.Text(app, height=10, width=40, bg=accent_color, fg=fg_color, insertbackground=fg_color, highlightbackground=highlight_color, highlightthickness=1, relief="flat", state="normal")
output_field.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

paste_button = tk.Button(app, text="Paste", command=paste_text, bg=button_color, fg=fg_color, activebackground=highlight_color, activeforeground=fg_color, relief="flat")
paste_button.grid(row=2, column=0, pady=10, sticky="ew", padx=10)

copy_button = tk.Button(app, text="Copy", command=copy_text, bg=button_color, fg=fg_color, activebackground=highlight_color, activeforeground=fg_color, relief="flat")
copy_button.grid(row=2, column=1, pady=10, sticky="ew", padx=10)

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=accent_color, background=accent_color, foreground=fg_color, arrowcolor=highlight_color, selectbackground=accent_color, selectforeground=fg_color, relief="flat")
style.map("TCombobox", fieldbackground=[("readonly", accent_color)], foreground=[("readonly", fg_color)], background=[("readonly", accent_color)], arrowcolor=[("readonly", highlight_color)])

language_dropdown = ttk.Combobox(app, values=list(language_codes.keys()), state="readonly", font=("Arial", 12))
language_dropdown.set("English")
language_dropdown.grid(row=3, column=0, columnspan=2, pady=10)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.mainloop()
