import time
import keyboard
import tkinter as tk
from threading import Thread, Event
from tkinter import ttk
import pygetwindow as gw
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        self.root.configure(bg='#2e2e2e')
        self.root.attributes("-topmost", True)
        if os.path.exists("lost_ark_icon_249792.ico"):
            self.root.iconbitmap("lost_ark_icon_249792.ico")
        self.main_frame = tk.Frame(root, bg='#2e2e2e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.input_frame = tk.Frame(self.main_frame, bg='#2e2e2e')
        self.input_frame.pack(pady=10)
        self.checkbox_var_r = tk.BooleanVar()
        self.checkbox_var_e = tk.BooleanVar()
        self.label_r = tk.Label(self.input_frame, text="Key 1 (Default: 1):", bg='#2e2e2e', fg='white')
        self.label_r.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_r = tk.Entry(self.input_frame, bg='#444', fg='white')
        self.entry_r.insert(0, '1')
        self.entry_r.grid(row=0, column=1, padx=10, pady=5)
        self.checkbox_doppel_r = tk.Checkbutton(self.input_frame, text="Double Press", bg='#2e2e2e', fg='white', variable=self.checkbox_var_r, selectcolor='#444', activebackground='#2e2e2e')
        self.checkbox_doppel_r.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
        self.label_e = tk.Label(self.input_frame, text="Key 2 (Default: 2):", bg='#2e2e2e', fg='white')
        self.label_e.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_e = tk.Entry(self.input_frame, bg='#444', fg='white')
        self.entry_e.insert(0, '2')
        self.entry_e.grid(row=1, column=1, padx=10, pady=5)
        self.checkbox_doppel_e = tk.Checkbutton(self.input_frame, text="Double Press", bg='#2e2e2e', fg='white', variable=self.checkbox_var_e, selectcolor='#444', activebackground='#2e2e2e')
        self.checkbox_doppel_e.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        self.label_time = tk.Label(self.input_frame, text="Wait Time (seconds, Default: 47):", bg='#2e2e2e', fg='white')
        self.label_time.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_time = tk.Entry(self.input_frame, bg='#444', fg='white')
        self.entry_time.insert(0, '47')
        self.entry_time.grid(row=2, column=1, padx=10, pady=5)
        self.info_label = tk.Label(self.input_frame, text="", bg='#2e2e2e', fg='white', justify=tk.LEFT, anchor=tk.W)
        self.info_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress, maximum=100)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("white.Horizontal.TProgressbar", troughcolor='#444', background='white', thickness=20)
        self.progress_bar.configure(style="white.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, padx=10, pady=20)
        self.time_label = tk.Label(self.main_frame, text="Remaining Time: 0.0s", bg='#2e2e2e', fg='white')
        self.time_label.pack()
        self.start_button = tk.Button(self.main_frame, text="Start", command=self.toggle_script, bg='#444', fg='white')
        self.start_button.pack(pady=10)
        self.running = False
        self.paused = False
        self.stop_event = Event()
        self.update_button_status()

    def toggle_script(self):
        if not self.running:
            self.start_script()
        else:
            self.reset_script()

    def start_script(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.stop_event.clear()
            self.start_button.config(text="Reset")
            self.update_button_status()
            self.set_widgets_state('disabled')
            self.thread = Thread(target=self.run, daemon=True)
            self.thread.start()

    def reset_script(self):
        if self.running or self.paused:
            self.running = False
            self.paused = False
            self.stop_event.set()
            self.reset_progress()
            self.start_button.config(text="Start")
            self.update_button_status()
            self.set_widgets_state('normal')

    def set_widgets_state(self, state):
        self.entry_r.config(state=state)
        self.checkbox_doppel_r.config(state=state)
        self.entry_e.config(state=state)
        self.checkbox_doppel_e.config(state=state)
        self.entry_time.config(state=state)

    def is_window_active(self):
        active_window = gw.getActiveWindow()
        current_window = gw.getWindowsWithTitle(self.root.title())[0] if gw.getWindowsWithTitle(self.root.title()) else None
        return active_window == current_window

    def update_button_status(self):
        if self.running:
            if self.is_window_active():
                self.start_button.config(bg='green')
                self.info_label.config(text="The script will start once you are in the game.")
            else:
                self.start_button.config(bg='#444')
        else:
            self.start_button.config(bg='#444')
        self.root.after(100, self.update_button_status)

    def run(self):
        while self.running:
            if not self.is_window_active():
                key1 = self.entry_r.get().strip()
                key2 = self.entry_e.get().strip()
                double_press_r = self.checkbox_var_r.get()
                double_press_e = self.checkbox_var_e.get()
                wait_time_str = self.entry_time.get().replace(',', '.')
                try:
                    wait_time = float(wait_time_str)
                except ValueError:
                    wait_time = 47
                total_time = 1 + 0.7 + wait_time
                elapsed = 0
                if not self.wait_with_stop_check(1):
                    return
                elapsed += 1
                self.update_progress(elapsed, total_time)
                if not self.running:
                    break
                if key1:
                    self.press_key(key1, double_press_r)
                if not self.running:
                    break
                if not self.wait_with_stop_check(0.7):
                    return
                elapsed += 0.7
                self.update_progress(elapsed, total_time)
                if not self.running:
                    break
                if key2:
                    self.press_key(key2, double_press_e)
                if not self.running:
                    break
                start_wait_time = time.time()
                while (time.time() - start_wait_time) < wait_time:
                    if not self.running:
                        return
                    if self.paused:
                        while self.paused:
                            time.sleep(0.1)
                    elapsed = 1 + 0.7 + (time.time() - start_wait_time)
                    self.update_progress(elapsed, total_time)
                if not self.running:
                    break
                self.reset_progress()

    def wait_with_stop_check(self, duration):
        start_time = time.time()
        while (time.time() - start_time) < duration:
            if self.stop_event.is_set():
                return False
            if self.paused:
                while self.paused:
                    time.sleep(0.1)
        return True

    def press_key(self, key, double_press):
        if double_press:
            keyboard.press_and_release(key)
            time.sleep(0.1)
            keyboard.press_and_release(key)
        else:
            keyboard.press_and_release(key)

    def update_progress(self, elapsed, total_time):
        progress_percentage = (elapsed / total_time) * 100
        self.progress.set(progress_percentage)
        self.time_label.config(text=f"Remaining Time: {max(0, total_time - elapsed):.1f}s")

    def reset_progress(self):
        self.progress.set(0)
        self.time_label.config(text="Remaining Time: 0.0s")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
