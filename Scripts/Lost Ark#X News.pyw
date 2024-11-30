import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import tkinter as tk
from tkinter import scrolledtext, simpledialog, ttk
from datetime import datetime

refresh_interval = None
refreshing = False
root = None
text_area = None
progress_bar = None
button_frame = None
progress_frame = None
last_updated_label = None

def get_last_three_posts(username):
    global progress_bar, progress_frame, last_updated_label
    url = f"https://x.com/{username}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    output = []

    try:
        driver.get(url)
        time.sleep(5)

        posts = driver.find_elements(By.TAG_NAME, 'article')[:3]

        if posts:
            sorted_posts = []
            for post in posts:
                try:
                    time_tag = post.find_element(By.TAG_NAME, 'time')
                    content_tag = post.find_element(By.XPATH, ".//div[@data-testid='tweetText']")

                    post_date = time_tag.get_attribute('datetime')
                    post_date_formatted = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y %H:%M")
                    content = content_tag.text if content_tag else "No content found"
                    sorted_posts.append((datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S.%fZ"), f"{post_date_formatted}\n{content}\n-------------------------------\n"))
                except Exception as e:
                    sorted_posts.append((None, f"Error fetching post: {e}\n-------------------------------\n"))

            sorted_posts.sort(key=lambda x: x[0] if x[0] is not None else datetime.min, reverse=True)
            output = [post[1] for post in sorted_posts]
        else:
            output.append(f"No posts found for @{username}.\n")

    except Exception as e:
        output.append(f"Error fetching the webpage: {e}\n")
    finally:
        driver.quit()
        if progress_bar:
            root.after(0, lambda: progress_bar.stop() if progress_bar.winfo_exists() else None)
        if progress_frame:
            root.after(0, lambda: progress_frame.destroy() if progress_frame.winfo_exists() else None)
        root.after(0, lambda: update_output_in_window(output))
        last_updated = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        root.after(0, lambda: update_last_updated_label(last_updated))

def update_output_in_window(output):
    global text_area
    if text_area:
        text_area.configure(state='normal')
        text_area.delete(1.0, tk.END)
        for line in output:
            if line.startswith("\n") and line.endswith("\n"):
                text_area.insert(tk.END, line, ("date",))
            else:
                text_area.insert(tk.END, line, ("content",))
        text_area.configure(state='disabled')

def update_last_updated_label(last_updated):
    global last_updated_label
    if last_updated_label:
        last_updated_label.config(text=f"Last updated: {last_updated}")

def display_loading_bar_in_window(parent):
    progress_frame = tk.Frame(parent, bg="#2E2E2E")
    progress_frame.pack(side=tk.TOP, padx=10, pady=(0, 10))

    label = tk.Label(progress_frame, text="Loading data...", fg="#FFFFFF", bg="#2E2E2E", font=("Helvetica", 12))
    label.pack(pady=5)

    progress = ttk.Progressbar(progress_frame, mode='indeterminate')
    progress.pack(pady=5)
    progress.start()

    return progress_frame, progress

def fetch_posts_in_thread(show_loading=True):
    global progress_bar, progress_frame
    if show_loading and not progress_bar:
        progress_frame, progress_bar = display_loading_bar_in_window(button_frame)

    def task():
        get_last_three_posts("playlostark")

    thread = threading.Thread(target=task)
    thread.start()

def display_output_in_darkmode_window(output):
    global refresh_interval, refreshing, root, text_area, progress_bar, button_frame, last_updated_label

    root = tk.Tk()
    root.title("X Posts Display")
    root.configure(bg="#2E2E2E")
    root.geometry("800x450")

    last_updated_label = tk.Label(root, text="Last updated: Not yet updated", fg="#A9A9A9", bg="#2E2E2E", font=("Helvetica", 8))
    last_updated_label.pack(anchor='w', padx=10, pady=(5, 5))

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20, fg="#A9A9A9", bg="#1E1E1E", font=("Helvetica", 10))
    text_area.pack(padx=10, pady=10)

    button_frame = tk.Frame(root, bg="#2E2E2E")
    button_frame.pack(pady=5)

    def auto_refresh():
        global refreshing
        if refresh_interval:
            refreshing = True
            stop_button.configure(bg="#8B0000")
            if refreshing:
                root.after(refresh_interval * 60000, lambda: fetch_posts_in_thread(show_loading=False))
                root.after(refresh_interval * 60000, auto_refresh)

    def stop_refresh():
        global refreshing
        refreshing = False
        stop_button.configure(bg="#444")

    def set_refresh_interval():
        global refresh_interval
        interval = simpledialog.askinteger("Auto-Refresh Interval", "Enter the number of minutes:")
        if interval:
            refresh_interval = interval
            if not refreshing:
                auto_refresh()

    auto_refresh_button = tk.Button(button_frame, text="Auto-Refresh", command=set_refresh_interval, bg="#444", fg="#FFF")
    auto_refresh_button.pack(side=tk.LEFT, padx=5)

    stop_button = tk.Button(button_frame, text="Stop", command=stop_refresh, bg="#444", fg="#FFF")
    stop_button.pack(side=tk.LEFT, padx=5)

    fetch_posts_in_thread()

    root.mainloop()

display_output_in_darkmode_window([])
