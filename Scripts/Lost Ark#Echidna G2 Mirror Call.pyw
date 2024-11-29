import tkinter as tk
from math import sin, cos, pi, sqrt

def decrease_num1(event=None):
    global current_value
    current_value -= 1
    update_result_display()
    update_circle_colors()

def increase_num2(event=None):
    global current_value
    current_value += 1
    update_result_display()
    update_circle_colors()

def reset(event=None):
    global current_value, start_position
    current_value = 0
    start_position = None
    update_result_display()
    update_circle_colors()

def update_result_display():
    result_label.config(text=str(current_value))

def update_circle_colors():
    for i, circle in enumerate(circles):
        canvas.itemconfig(circle, fill=circle_fill_color)
        canvas.itemconfig(texts[i], text="")
    if start_position is not None:
        canvas.itemconfig(circles[start_position], fill="red")
        canvas.itemconfig(texts[start_position], text="Start")
    if start_position is not None:
        if current_value == 0:
            index = start_position
        elif current_value > 0:
            index = (start_position + current_value) % 8
        else:
            index = (start_position + current_value + 8) % 8
        canvas.itemconfig(circles[index], fill="green")
        canvas.itemconfig(texts[index], text="HERE")

def on_canvas_click(event):
    click_x, click_y = event.x, event.y
    min_distance = float('inf')
    closest_index = None

    for i, (circle_x, circle_y) in enumerate(circle_centers):
        distance = sqrt((click_x - circle_x) ** 2 + (click_y - circle_y) ** 2)
        if distance < min_distance and distance <= click_radius:
            min_distance = distance
            closest_index = i

    if closest_index is not None:
        on_circle_click(closest_index)

def on_circle_click(index):
    global start_position
    start_position = index
    update_circle_colors()

root = tk.Tk()
root.title("Echidna x50")
root.attributes("-topmost", True)
root.geometry("200x250")

# Set Dark Mode colors
bg_color = "#2e2e2e"
fg_color = "#f5f5f5"
circle_fill_color = "#3b3b3b"  # Dark color for the circles
circle_outline_color = fg_color  # Light outline for the circles
text_color = "#f5f5f5"

root.configure(bg=bg_color)
current_value = 0
start_position = None
click_radius = 25  # Increased radius within which a click will be registered for the closest circle

canvas = tk.Canvas(root, width=200, height=180, bg=bg_color, highlightthickness=0)
canvas.pack()

circle_radius = 8
center_x, center_y = 100, 90
distance = 45
angles = [(i * 2 * pi / 8) for i in range(8)]
circles = []
texts = []
circle_centers = []

for angle in angles:
    x = center_x + distance * cos(angle)
    y = center_y + distance * sin(angle)
    circle = canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, fill=circle_fill_color, outline=circle_outline_color)
    circles.append(circle)
    circle_centers.append((x, y))
    text = canvas.create_text(x, y - 10, text="", font=("Arial", 7), fill=text_color)
    texts.append(text)

canvas.bind('<Button-1>', on_canvas_click)

result_label = tk.Label(root, text=str(current_value), font=("Arial", 14), justify="center", bg=bg_color, fg=fg_color)
result_label.place(relx=0.5, rely=0.4, anchor="center")

# Adding the bottom label for controls
controls_label = tk.Label(root, text="Q = -1 | E = +1 | R = Reset", font=("Arial", 7), bg=bg_color, fg=fg_color)
controls_label.pack(side="bottom", pady=2)

# Adding the instruction label
instruction_label = tk.Label(root, text="Click in the circle to mark the start position", font=("Arial", 7), bg=bg_color, fg=fg_color)
instruction_label.pack(side="bottom", pady=2)

root.bind('q', decrease_num1)
root.bind('e', increase_num2)
root.bind('r', reset)

root.mainloop()
