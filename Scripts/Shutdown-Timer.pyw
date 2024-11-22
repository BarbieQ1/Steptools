import tkinter as tk
from tkinter import messagebox
import os, time, threading

def shutdown_timer(hours, minutes):
    global shutdown_in_progress
    shutdown_in_progress = True
    total_seconds = (hours * 3600) + (minutes * 60)
    for _ in range(total_seconds):
        if not shutdown_in_progress: return
        time.sleep(1)
    if shutdown_in_progress: os.system("shutdown /s /t 0")

def start_timer():
    try:
        hours = int(entry_hours.get()) if entry_hours.get().strip() else 0
        minutes = int(entry_minutes.get()) if entry_minutes.get().strip() else 0
        if hours < 0 or minutes < 0: messagebox.showerror("Error", "Values must be positive."); return
        if messagebox.askyesno("Confirmation", f"PC will shut down in {hours} hours and {minutes} minutes. Proceed?"):
            global shutdown_thread
            shutdown_thread = threading.Thread(target=shutdown_timer, args=(hours, minutes), daemon=True)
            shutdown_thread.start()
            messagebox.showinfo("Timer Started", "Shutdown timer has been started.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def stop_timer():
    global shutdown_in_progress
    if shutdown_in_progress:
        shutdown_in_progress = False
        os.system("shutdown /a")
        messagebox.showinfo("Cancelled", "Shutdown has been cancelled.")
    else:
        messagebox.showinfo("No Timer Active", "No timer is currently active.")

def configure_dark_mode(widget):
    widget.configure(bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff")

shutdown_in_progress = False
shutdown_thread = None

root = tk.Tk()
root.title("PC Shutdown Timer")
root.geometry("300x250")
root.configure(bg="#2e2e2e")
tk.Label(root, text="Hours:", bg="#2e2e2e", fg="#ffffff").pack(pady=5)
entry_hours = tk.Entry(root, width=10)
configure_dark_mode(entry_hours)
entry_hours.pack(pady=5)
tk.Label(root, text="Minutes:", bg="#2e2e2e", fg="#ffffff").pack(pady=5)
entry_minutes = tk.Entry(root, width=10)
configure_dark_mode(entry_minutes)
entry_minutes.pack(pady=5)
go_button = tk.Button(root, text="GO", bg="#228B22", fg="#ffffff", command=start_timer, activebackground="#2E8B57", activeforeground="#ffffff")
go_button.pack(pady=10)
stop_button = tk.Button(root, text="STOP", bg="#aa4444", fg="#ffffff", command=stop_timer, activebackground="#bb5555", activeforeground="#ffffff")
stop_button.pack(pady=10)
root.mainloop()
