import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
import math, pyperclip

base_url = "https://raw.githubusercontent.com/BarbieQ1/Steptools/main/Scripts/AegirG1-pictures"
names = ["eye.png", "hea.png", "horn.png", "sick.png"]
colormap = {"eye.png": "red", "hea.png": "green", "horn.png": "blue", "sick.png": "black"}
posmap = {1: 12, 2: 1, 3: 3, 4: 5, 5: 6, 6: 7, 7: 9, 8: 11}
sel_color, circle_colors, active_label = None, {}, None
img_frames, chk_imgs, imgs = {}, {}, []

def set_color(name, lbl):
    global sel_color, active_label
    sel_color = colormap[name]
    if active_label:
        active_label.config(bg="#3a3a3a")
    lbl.config(bg="#6a6a6a")
    active_label = lbl

def on_click(circ, pos):
    global sel_color, circle_colors
    if sel_color:
        for c, val in circle_colors.items():
            if val and val[0] == sel_color:
                c.itemconfig(c.find_all()[0], fill="#5a5a5a")
                circle_colors[c] = None
                update_check(sel_color, False)
        circ.itemconfig(circ.find_all()[0], fill=sel_color)
        circle_colors[circ] = (sel_color, pos)
        update_check(sel_color, True)

def update_check(color, chk):
    for n, col in colormap.items():
        if col == color:
            f = img_frames[n]
            if chk:
                chk_lbl = tk.Label(f, image=chk_imgs[n], bg="#3a3a3a")
                chk_lbl.place(relx=0.7, rely=0.7)
                f.chk_lbl = chk_lbl
            elif hasattr(f, 'chk_lbl'):
                f.chk_lbl.destroy()
            break

def rm_color(name):
    col = colormap[name]
    for circ, val in circle_colors.items():
        if val and val[0] == col:
            circ.itemconfig(circ.find_all()[0], fill="#5a5a5a")
            circle_colors[circ] = None
    update_check(col, False)

def copy_clip():
    labelmap = {
        "green": "Heart",
        "red": "Eye",
        "blue": "Horn",
        "black": "Scythe"
    }
    ord_col = ["green", "red", "blue", "black"]
    parts = []
    for col in ord_col:
        for c, v in circle_colors.items():
            if v and v[0] == col:
                parts.append(f"{posmap[v[1]]} {labelmap[col]}")
                break
    pyperclip.copy("  ||  ".join(parts))
def reset():
    global circle_colors, active_label
    for c in circle_colors:
        c.itemconfig(c.find_all()[0], fill="#5a5a5a")
    circle_colors = {c: None for c in circle_colors}
    for f in img_frames.values():
        if hasattr(f, 'chk_lbl'):
            f.chk_lbl.destroy()
    if active_label:
        active_label.config(bg="#3a3a3a")
    active_label = None

root = tk.Tk()
root.configure(bg="#2e2e2e")
root.title("Aegir Gate 1")
root.attributes('-topmost', True)
root.geometry("200x250")

frame = tk.Frame(root, bg="#2e2e2e", width=140, height=120)
frame.pack_propagate(False)
frame.pack(side="top", pady=10)
rad, dia, cx, cy = 40, 20, 70, 60
positions = [(0, -rad), (math.cos(math.radians(45)) * rad, -math.sin(math.radians(45)) * rad), 
             (rad, 0), (math.cos(math.radians(45)) * rad, math.sin(math.radians(45)) * rad), 
             (0, rad), (-math.cos(math.radians(45)) * rad, math.sin(math.radians(45)) * rad), 
             (-rad, 0), (-math.cos(math.radians(45)) * rad, -math.sin(math.radians(45)) * rad)]

for i, (x, y) in enumerate(positions):
    circ = tk.Canvas(frame, width=dia, height=dia, bg="#2e2e2e", highlightthickness=0)
    circ.create_oval(2, 2, dia - 2, dia - 2, fill="#5a5a5a", outline="#5a5a5a")
    circ.bind("<Button-1>", lambda e, c=circ, pos=i + 1: on_click(c, pos))
    circ.place(x=cx + x, y=cy + y, anchor="center")
    circle_colors[circ] = None

icon_frame = tk.Frame(root, bg="#2e2e2e")
icon_frame.pack(side="bottom", fill="x", pady=5)

def make_chk():
    img = Image.new("RGBA", (15, 15), (0, 0, 0, 0))
    ImageDraw.Draw(img).polygon([(3, 8), (7, 12), (12, 3)], fill="green")
    return ImageTk.PhotoImage(img)

for n in names:
    img_url = f"{base_url}/{n}"
    response = requests.get(img_url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).resize((30, 30), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    chk_imgs[n] = make_chk()
    imgs.append(img_tk)

    f = tk.Frame(icon_frame, bg="#3a3a3a", width=40, height=40)
    f.pack_propagate(False)
    f.pack(side="left", padx=5)
    img_frames[n] = f

    lbl = tk.Label(f, image=img_tk, bg="#3a3a3a")
    lbl.bind("<Button-1>", lambda e, name=n, l=lbl: set_color(name, l))
    lbl.bind("<Button-3>", lambda e, name=n: rm_color(name))
    lbl.pack(fill="both", expand=True)

tk.Button(root, text="Copy", command=copy_clip, bg="#5a5a5a", fg="white").pack(side="bottom", pady=5)
tk.Label(root, text="R = Reset", bg="#2e2e2e", fg="white").pack(side="bottom", pady=1)
root.bind("r", lambda e: reset())
root.mainloop()
