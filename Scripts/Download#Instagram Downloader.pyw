import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import instaloader
from pathlib import Path
import pickle
import re

download_folder = os.path.join(Path.home(), "Downloads")
credentials_file = os.path.join(Path.home(), "insta_credentials.pkl")

def save_credentials(username, password):
    with open(credentials_file, 'wb') as f:
        pickle.dump({'username': username, 'password': password}, f)

def load_credentials():
    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as f:
            return pickle.load(f)
    return None

def sanitize_url(url):
    sanitized_url = re.sub(r'\?.*$', '', url)
    return sanitized_url

def download_content():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a valid Instagram link.")
        return

    sanitized_url = sanitize_url(url)
    credentials = load_credentials()
    if credentials:
        username, password = credentials['username'], credentials['password']
    else:
        username = simpledialog.askstring("Login Required", "Enter your Instagram username:")
        password = simpledialog.askstring("Login Required", "Enter your Instagram password:", show="*")
        save_credentials(username, password)

    try:
        loader = instaloader.Instaloader(dirname_pattern=download_folder, save_metadata=False)
        loader.login(username, password)

        if "/stories/" in sanitized_url:
            user = re.search(r"stories/([^/]+)/", sanitized_url)
            if user:
                username = user.group(1)
                profile = instaloader.Profile.from_username(loader.context, username)
                loader.download_stories(userids=[profile.userid], filename_target=download_folder)
                messagebox.showinfo("Success", f"All stories from {username} have been saved in the Download folder.")
            else:
                messagebox.showerror("Error", "Invalid story URL format.")
        else:
            shortcode = sanitized_url.rstrip('/').split('/')[-1]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            
            content_type = []
            if post.is_video:
                content_type.append("video")
            if post.typename == "GraphImage":
                content_type.append("image")

            loader.download_post(post, target=download_folder)
            
            if post.owner_profile.has_viewable_story:
                loader.download_stories(userids=[post.owner_profile.userid], filename_target=download_folder)
                content_type.append("story")

            if content_type:
                content_desc = " and ".join(content_type)
                messagebox.showinfo("Success", f"The {content_desc} has been saved in the Download folder.")
            else:
                messagebox.showinfo("Success", "Content has been saved in the Download folder.")
            
    except instaloader.exceptions.BadCredentialsException:
        messagebox.showerror("Error", "Invalid username or password.")
        os.remove(credentials_file)
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {e}")

def handle_enter(event):
    download_content()

root = tk.Tk()
root.title("Instagram Content Downloader")
root.configure(bg="#333333")
root.attributes("-topmost", True)

tk.Label(root, text="Enter Instagram Link:", bg="#333333", fg="white").pack(pady=5)
url_entry = tk.Entry(root, width=50, bg="#555555", fg="white", insertbackground="white")
url_entry.pack(padx=10, pady=5)
url_entry.bind("<Return>", handle_enter)

download_button = tk.Button(root, text="Download", command=download_content, bg="#444444", fg="white")
download_button.pack(pady=10)

root.mainloop()
