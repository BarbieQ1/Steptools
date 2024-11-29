import tkinter as tk
from tkinter import messagebox, filedialog
import os
import yt_dlp

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a TikTok link!")
        return
    
    try:
        save_path = filedialog.askdirectory()
        if not save_path:
            return
        
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'format': 'best'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        messagebox.showinfo("Success", "The video has been downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("TikTok Video Downloader")
root.configure(bg="#2e2e2e")

root.geometry("400x200")

url_label = tk.Label(root, text="Enter TikTok link:", fg="white", bg="#2e2e2e")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50, bg="#1e1e1e", fg="white", insertbackground="white")
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Download", command=download_video, bg="#4a4a4a", fg="white")
download_button.pack(pady=20)

root.mainloop()
