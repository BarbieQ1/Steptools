import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import threading
import time

def fetch_server_status():
    url = "https://www.playlostark.com/de-de/support/server-status"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            server_divs = soup.select(
                '.ags-ServerStatus-content-responses-response[data-index="2"] .ags-ServerStatus-content-responses-response-server'
            )
            
            server_status_list = []
            for server in server_divs:
                status_class = server.select_one(
                    '.ags-ServerStatus-content-responses-response-server-status'
                ).get("class")[1]
                status = status_class.split("--")[-1]
                name = server.select_one(
                    '.ags-ServerStatus-content-responses-response-server-name'
                ).text.strip()
                server_status_list.append((name, status))
            
            return server_status_list
        else:
            return [("Error", "offline")]
    except requests.exceptions.RequestException as e:
        return [("Error", "offline")]

def display_server_status():
    global current_status, monitored_status
    new_status = fetch_server_status()
    
    if new_status != current_status:
        current_status = new_status
        status_text.config(state=tk.NORMAL)
        status_text.delete(1.0, tk.END)
        
        for name, status in current_status:
            tag = {
                "good": "good",
                "busy": "busy",
                "full": "full",
                "maintenance": "maintenance",
                "offline": "offline"
            }.get(status, "default")
            line = f"{name:<20}{status.capitalize():>15}\n"
            status_text.insert(tk.END, line, tag)

            if monitor_checkbox_var.get() and name.lower() == monitored_server.get().lower():
                if monitored_status.get(name) != status:
                    monitored_status[name] = status
                    messagebox.showinfo("Server Status Changed", f"{name} is now {status.capitalize()}")
        
        if auto_refreshing[0]:
            status_text.insert(tk.END, "\n[Auto-Refresh active]", "info")
        status_text.config(state=tk.DISABLED)

def start_auto_refresh():
    try:
        interval = int(interval_entry.get())
        if interval <= 0:
            raise ValueError("Interval must be greater than 0.")
    except ValueError as e:
        status_text.config(state=tk.NORMAL)
        status_text.delete(1.0, tk.END)
        status_text.insert(tk.END, f"Error: {e}")
        status_text.config(state=tk.DISABLED)
        return

    def auto_refresh():
        while auto_refreshing[0]:
            display_server_status()
            root.after(interval * 1000, lambda: None)

    if not auto_refreshing[0]:
        auto_refreshing[0] = True
        auto_refresh_button.config(state=tk.DISABLED)
        stop_refresh_button.config(state=tk.NORMAL)
        threading.Thread(target=auto_refresh, daemon=True).start()

def stop_auto_refresh():
    auto_refreshing[0] = False
    auto_refresh_button.config(state=tk.NORMAL)
    stop_refresh_button.config(state=tk.DISABLED)
    display_server_status()

def update_ping():
    while True:
        try:
            start_time = time.time()
            requests.get("https://www.google.de", timeout=5)  # URL geändert zu google.de
            elapsed_time = (time.time() - start_time) * 1000
            ping_times.append(elapsed_time)
            if len(ping_times) > 5:
                ping_times.pop(0)
            avg_ping = sum(ping_times) / len(ping_times)
            ping_label.config(text=f"Ping (avg 5s): {avg_ping:.2f} ms")
        except requests.exceptions.RequestException:
            ping_label.config(text="Ping (avg 5s): Error")
        time.sleep(1)


def set_darkmode(widget, is_entry=False):
    widget.config(bg="#353535", fg="#FFFFFF")
    if is_entry:
        widget.config(insertbackground="white")
    widget.config(highlightbackground="#353535", highlightcolor="#353535")

root = tk.Tk()
root.title("Server Status with Auto-Refresh")

root.configure(bg="#2E2E2E")

status_text = tk.Text(root, wrap=tk.WORD, height=6, width=40, state=tk.DISABLED)
status_text.config(bg="#3A3A3A", fg="#FFFFFF")
status_text.pack(padx=10, pady=10)

status_text.tag_configure("good", foreground="#00FF00")
status_text.tag_configure("busy", foreground="#FFA500")
status_text.tag_configure("full", foreground="#9400D3")
status_text.tag_configure("maintenance", foreground="#FFFF00")
status_text.tag_configure("offline", foreground="#FF4500")
status_text.tag_configure("info", foreground="cyan")

refresh_button = tk.Button(root, text="Refresh", command=display_server_status)
set_darkmode(refresh_button)
refresh_button.pack(pady=5)

interval_frame = tk.Frame(root, bg="#2E2E2E")
interval_frame.pack(pady=5)

interval_label = tk.Label(interval_frame, text="Interval (sec):", bg="#2E2E2E", fg="#FFFFFF")
interval_label.pack(side=tk.LEFT, padx=5)

interval_entry = tk.Entry(interval_frame, width=5)
set_darkmode(interval_entry, is_entry=True)
interval_entry.pack(side=tk.LEFT, padx=5)

auto_refresh_button = tk.Button(interval_frame, text="Auto Refresh", command=start_auto_refresh)
set_darkmode(auto_refresh_button)
auto_refresh_button.pack(side=tk.LEFT, padx=5)

stop_refresh_button = tk.Button(interval_frame, text="Stop", command=stop_auto_refresh, state=tk.DISABLED)
set_darkmode(stop_refresh_button)
stop_refresh_button.pack(side=tk.LEFT, padx=5)

monitor_frame = tk.Frame(root, bg="#2E2E2E")
monitor_frame.pack(pady=10)

monitor_label = tk.Label(monitor_frame, text="Monitor Server:", bg="#2E2E2E", fg="#FFFFFF")
monitor_label.pack(side=tk.LEFT, padx=5)

monitored_server = tk.StringVar()
monitor_entry = tk.Entry(monitor_frame, textvariable=monitored_server, width=15)
set_darkmode(monitor_entry, is_entry=True)
monitor_entry.pack(side=tk.LEFT, padx=5)

monitor_checkbox_var = tk.BooleanVar()
monitor_checkbox = tk.Checkbutton(monitor_frame, text="Enable Alert", variable=monitor_checkbox_var, bg="#2E2E2E", fg="#FFFFFF", selectcolor="#2E2E2E")
monitor_checkbox.pack(side=tk.LEFT, padx=5)

ping_label = tk.Label(root, text="Ping (avg 5s): Calculating...", bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 8))
ping_label.pack(pady=5)

current_status = []
monitored_status = {}
auto_refreshing = [False]
ping_times = []

display_server_status()

threading.Thread(target=update_ping, daemon=True).start()

root.geometry("400x400")
root.mainloop()
