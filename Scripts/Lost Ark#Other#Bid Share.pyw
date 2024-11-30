import tkinter as tk
import math
from tkinter import messagebox
import os

def calculate_bid(*args):
    try:
        ah_price = float(ah_price_entry.get())
        if player_count.get() == 0:
            result_label.config(text="Bid: ")
            return
        
        player_count_value = player_count.get()
        bid = ah_price / player_count_value
        bid -= bid * 0.05
        bid -= 1
        
        final_bid = bid * player_count_value - bid
        # Round down to the nearest whole number
        final_bid = math.floor(final_bid)
        result_label.config(text=f"Bid: {final_bid}")
    except ValueError:
        result_label.config(text="Bid: ")

def update_calculation(*args):
    calculate_bid()

def set_player_count(value):
    player_count.set(value)
    update_calculation()

def copy_bid():
    try:
        text = result_label.cget("text").split(": ")
        if len(text) > 1:
            bid_value = text[1]
            root.clipboard_clear()  # Clear the clipboard
            root.clipboard_append(bid_value)  # Copy the bid value to clipboard
            root.update()  # Ensure the clipboard update
            messagebox.showinfo("Copied", f"Bid value {bid_value} copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy bid value: {str(e)}")

root = tk.Tk()
root.title("Bid Calculator")
root.attributes('-topmost', True)

# Set icon
icon_path = "lost_ark_icon_249792.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

root.configure(bg='#2e2e2e')
root.geometry("300x250")  # Adjust the window size

player_count = tk.IntVar()
player_count.set(0)

tk.Label(root, text="Select Player Count:", bg='#2e2e2e', fg='#ffffff').pack(pady=5)

frame = tk.Frame(root, bg='#2e2e2e')
frame.pack(pady=5)

player_counts = [4, 8, 16]
for count in player_counts:
    tk.Radiobutton(frame, text=f"{count}", variable=player_count, value=count, bg='#2e2e2e', fg='#ffffff', selectcolor='#555555', command=lambda c=count: set_player_count(c)).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="AH Price:", bg='#2e2e2e', fg='#ffffff').pack(pady=5)

ah_price_entry = tk.Entry(root, bg='#555555', fg='#ffffff', insertbackground='white')
ah_price_entry.pack(pady=5)
ah_price_entry.bind('<KeyRelease>', calculate_bid)

result_label = tk.Label(root, text="Bid: ", bg='#2e2e2e', fg='#ffffff', font=('Arial', 14, 'bold'))
result_label.pack(pady=10)

copy_button = tk.Button(root, text="Copy", command=copy_bid, bg='#555555', fg='#ffffff')
copy_button.pack(pady=10)

root.mainloop()
