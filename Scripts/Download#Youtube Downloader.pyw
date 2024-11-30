import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
import os
import threading
import time

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes', None)
        speed = d.get('speed', 0)
        eta = d.get('eta', 0)
        fragments_done = d.get('fragment_index', 0)
        fragments_total = d.get('fragment_count', 0)

        speed_mbps = (speed * 8) / (1024 * 1024) if speed else 0
        speed_label.config(text=f"Speed: {speed_mbps:.2f} Mbps")
        time_label.config(text=f"ETA: {time.strftime('%H:%M:%S', time.gmtime(eta))}" if eta else "ETA: Calculating...")

        if fragments_total:
            fragment_label.config(text=f"Fragment: {fragments_done}/{fragments_total}")

    elif d['status'] == 'finished':
        speed_label.config(text="Speed: 0 Mbps")
        time_label.config(text="ETA: 00:00:00")
        fragment_label.config(text="")

def start_download():
    download_thread = threading.Thread(target=download_video)
    download_thread.start()

def download_video():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Warning", "Please enter a YouTube link.")
        return

    download_path = filedialog.askdirectory(title="Select download location")
    if not download_path:
        return

    options = {
        'format': 'bestaudio' if toggle_var.get() == "MP3-Audio" else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ffmpeg_location': r'C:\ffmpeg\bin',
        'progress_hooks': [progress_hook],
    }

    if toggle_var.get() == "MP3-Audio":
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download complete.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during download: {e}")

def set_mp3():
    toggle_var.set("MP3-Audio")
    mp3_button.config(bg="green", fg="white")
    mp4_button.config(bg="#444444", fg="white")

def set_mp4():
    toggle_var.set("MP4-Video")
    mp4_button.config(bg="green", fg="white")
    mp3_button.config(bg="#444444", fg="white")

root = tk.Tk()
root.title("YouTube Downloader")
root.configure(bg="#1e1e1e")
root.geometry("450x250")
root.attributes("-topmost", True)

toggle_var = tk.StringVar(value="MP4-Video")
toggle_frame = tk.Frame(root, bg="#1e1e1e")
toggle_frame.pack(pady=10)

mp3_button = tk.Button(toggle_frame, text="MP3-Audio", command=set_mp3, width=10, bg="#444444", fg="white")
mp3_button.pack(side="left", padx=5)
mp4_button = tk.Button(toggle_frame, text="MP4-Video", command=set_mp4, width=10, bg="green", fg="white")
mp4_button.pack(side="left", padx=5)

url_label = tk.Label(root, text="Enter YouTube Link:", bg="#1e1e1e", fg="white", font=("Arial", 10))
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50, font=("Arial", 10))
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Download", command=start_download, bg="#444444", fg="white", font=("Arial", 10))
download_button.pack(pady=10)

speed_label = tk.Label(root, text="Speed: 0 Mbps", bg="#1e1e1e", fg="white", font=("Arial", 10))
speed_label.pack()

time_label = tk.Label(root, text="ETA: Calculating...", bg="#1e1e1e", fg="white", font=("Arial", 10))
time_label.pack()

fragment_label = tk.Label(root, text="", bg="#1e1e1e", fg="white", font=("Arial", 10))
fragment_label.pack()

root.mainloop()
