import requests
import threading
import os
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import Tk, Label, Button, StringVar, Entry, messagebox, filedialog

UPLOAD_URL = "https://file.io/"

def upload_file(file_path, output_var, sand_timer_label, upload_button, output_entry):
    try:
        sand_timer_label.config(text="Uploading...")
        sand_timer_label.pack(pady=10)
        upload_button.config(state="disabled")

        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size > 2000:
            messagebox.showerror("Error", "File exceeds 2GB size limit.")
            return

        with open(file_path, "rb") as file:
            response = requests.post(
                UPLOAD_URL,
                files={"file": (os.path.basename(file_path), file)}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    link = data.get("link")
                    output_var.set(link)
                    output_entry.config(state="normal")
                    output_entry.delete(0, "end")
                    output_entry.insert(0, link)
                    output_entry.config(state="readonly")
                else:
                    messagebox.showerror("Error", "Upload failed")
            else:
                messagebox.showerror("Error", f"Upload error: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        sand_timer_label.pack_forget()
        upload_button.config(state="normal")

def start_upload(file_path, output_var, sand_timer_label, upload_button, output_entry):
    thread = threading.Thread(
        target=upload_file,
        args=(file_path, output_var, sand_timer_label, upload_button, output_entry)
    )
    thread.start()

def select_file(output_var, sand_timer_label, upload_button, output_entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        start_upload(file_path, output_var, sand_timer_label, upload_button, output_entry)

def on_drop(event, output_var, sand_timer_label, upload_button, output_entry):
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path):
        start_upload(file_path, output_var, sand_timer_label, upload_button, output_entry)
    else:
        messagebox.showerror("Error", "Invalid file dropped.")

def main():
    root = TkinterDnD.Tk()
    root.title("File.io Upload")
    root.geometry("300x170")
    root.resizable(False, False)
    root.configure(bg="#2e2e2e")

    label = Label(root, text="Drag and drop a file or select from explorer", font=("Arial", 10), fg="#ffffff", bg="#2e2e2e")
    label.pack(pady=5)

    output_var = StringVar()
    sand_timer_label = Label(root, text="", font=("Arial", 10), fg="#ffffff", bg="#2e2e2e")

    output_entry = Entry(root, textvariable=output_var, font=("Arial", 10), width=40, bg="#ffffff", fg="#000000", state="readonly", justify="center")
    output_entry.pack(pady=5)

    upload_button = Button(
        root, text="Select File", command=lambda: select_file(output_var, sand_timer_label, upload_button, output_entry),
        font=("Arial", 10), bg="#444444", fg="#ffffff",
        activebackground="#555555", activeforeground="#ffffff"
    )
    upload_button.pack(pady=5)

    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", lambda e: on_drop(e, output_var, sand_timer_label, upload_button, output_entry))

    root.mainloop()

if __name__ == "__main__":
    main()
