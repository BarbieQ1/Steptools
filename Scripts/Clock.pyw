import tkinter as tk
from tkinter import Canvas, simpledialog, Toplevel
from math import cos, sin, radians
from datetime import datetime, timedelta

class AnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Analoge Uhr mit Timer")
        self.root.geometry("300x600")
        self.root.configure(bg="#1e1e1e")  # Dark Mode Hintergrundfarbe
        self.root.attributes("-topmost", True)  # Immer im Vordergrund

        self.alert_minutes = tk.IntVar(value=10)  # Standardwert: 10 Minuten

        # Eingabefeld für Alert-Minuten
        alert_frame = tk.Frame(root, bg="#1e1e1e")
        alert_frame.pack(pady=5)

        tk.Label(alert_frame, text="Alert (Minuten):", bg="#1e1e1e", fg="white").pack(side="left")
        alert_entry = tk.Entry(alert_frame, textvariable=self.alert_minutes, bg="#333333", fg="white", width=5, insertbackground="white")
        alert_entry.pack(side="left", padx=5)

        self.canvas = Canvas(root, width=300, height=300, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.timer_marks = []  # Liste der Timer-Markierungen
        self.timer_times = []  # Liste der Timer-Zeiten
        self.timer_notes = []  # Liste der Timer-Notizen
        self.center_x = 150
        self.center_y = 150
        self.clock_radius = 140
        self.blink_state = False  # Für den Blink-Effekt

        self.add_button = tk.Button(root, text="Add", command=self.open_add_timer_dialog, bg="#333333", fg="white")
        self.add_button.pack(pady=10)

        self.timer_list_frame = tk.Frame(root, bg="#1e1e1e")
        self.timer_list_frame.pack(fill="both", expand=True)

        self.update_timer_list()
        self.update_clock()

    def draw_face(self, ring_color="#555555"):
        """Zeichnet das Zifferblatt der Uhr."""
        self.canvas.create_oval(
            self.center_x - self.clock_radius, self.center_y - self.clock_radius,
            self.center_x + self.clock_radius, self.center_y + self.clock_radius,
            fill="#2e2e2e", outline=ring_color, width=4
        )

    def draw_hands(self, hours, minutes):
        """Zeichnet die Zeiger der Uhr."""
        # Stundenzeiger
        hour_angle = radians((hours % 12) * 30 + minutes * 0.5 - 90)
        hour_x = self.center_x + cos(hour_angle) * (self.clock_radius - 70)
        hour_y = self.center_y + sin(hour_angle) * (self.clock_radius - 70)
        self.canvas.create_line(self.center_x, self.center_y, hour_x, hour_y, fill="white", width=6)

        # Minutenzeiger
        minute_angle = radians(minutes * 6 - 90)
        minute_x = self.center_x + cos(minute_angle) * (self.clock_radius - 40)
        minute_y = self.center_y + sin(minute_angle) * (self.clock_radius - 40)
        self.canvas.create_line(self.center_x, self.center_y, minute_x, minute_y, fill="white", width=4)

    def draw_timer_marks(self):
        """Zeichnet Timer-Markierungen."""
        now = datetime.now()
        highlight_ring = False

        if self.timer_times:
            # Sortiere Timer nach der nächsten Zeit
            sorted_timers = sorted(zip(self.timer_marks, self.timer_times, self.timer_notes), key=lambda x: x[1])
            self.timer_marks, self.timer_times, self.timer_notes = map(list, zip(*sorted_timers))

        for timer_angle, timer_time, note in zip(self.timer_marks, self.timer_times, self.timer_notes):
            time_diff = (timer_time - now).total_seconds()

            if 0 <= time_diff <= self.alert_minutes.get() * 60:
                highlight_ring = True
                fill_color = "green" if self.blink_state else "yellow"
            else:
                fill_color = "yellow"

            # Vergrößerte Markierung
            x1 = self.center_x + cos(timer_angle) * (self.clock_radius - 20)
            y1 = self.center_y + sin(timer_angle) * (self.clock_radius - 20)
            x2 = self.center_x + cos(timer_angle) * (self.clock_radius)
            y2 = self.center_y + sin(timer_angle) * (self.clock_radius)
            self.canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=5)

        # Zifferblatt unabhängig zeichnen
        self.draw_face(ring_color="green" if highlight_ring else "#555555")

    def open_add_timer_dialog(self):
        """Öffnet das Dialogfenster zum Hinzufügen eines Timers."""
        dialog = Toplevel(self.root)
        dialog.title("Neuer Timer")
        dialog.geometry("250x200")
        dialog.configure(bg="#1e1e1e")

        tk.Label(dialog, text="Uhrzeit (HH:MM oder HHMM):", bg="#1e1e1e", fg="white").pack(pady=5)
        time_entry = tk.Entry(dialog, bg="#333333", fg="white", insertbackground="white")
        time_entry.pack(pady=5)

        tk.Label(dialog, text="Notiz:", bg="#1e1e1e", fg="white").pack(pady=5)
        note_entry = tk.Entry(dialog, bg="#333333", fg="white", insertbackground="white")
        note_entry.pack(pady=5)

        def handle_add(event=None):
            self.add_timer(dialog, time_entry.get(), note_entry.get())

        dialog.bind("<Return>", handle_add)

        tk.Button(dialog, text="Hinzufügen", bg="#333333", fg="white", command=handle_add).pack(pady=10)

    def add_timer(self, dialog, timer_time, note):
        """Fügt einen neuen Timer hinzu."""
        if timer_time:
            try:
                if ":" in timer_time:
                    hours, minutes = map(int, timer_time.split(":"))
                else:
                    hours = int(timer_time[:2])
                    minutes = int(timer_time[2:])

                now = datetime.now()
                timer_datetime = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)

                # Wenn die Zeit in der Vergangenheit liegt, füge einen Tag hinzu
                if timer_datetime < now:
                    timer_datetime += timedelta(days=1)

                timer_angle = radians((hours % 12) * 30 + minutes * 0.5 - 90)
                self.timer_marks.append(timer_angle)
                self.timer_times.append(timer_datetime)
                self.timer_notes.append(note)

                self.update_timer_list()
                dialog.destroy()
            except ValueError:
                print("Ungültiges Format. Bitte HH:MM oder HHMM verwenden.")

    def update_timer_list(self):
        """Aktualisiert die Liste der Timer."""
        for widget in self.timer_list_frame.winfo_children():
            widget.destroy()

        if self.timer_times:
            sorted_timers = sorted(zip(self.timer_times, self.timer_notes), key=lambda x: x[0])
            self.timer_times, self.timer_notes = map(list, zip(*sorted_timers))

        for i, (timer_time, note) in enumerate(zip(self.timer_times, self.timer_notes)):
            frame = tk.Frame(self.timer_list_frame, bg="#1e1e1e")
            frame.pack(fill="x", pady=2)

            time_label = tk.Label(frame, text=timer_time.strftime("%H:%M"), bg="#1e1e1e", fg="white")
            time_label.pack(side="left", padx=5)

            note_label = tk.Label(frame, text=note, bg="#1e1e1e", fg="white")
            note_label.pack(side="left", padx=5, expand=True)

            delete_button = tk.Button(frame, text="-", bg="#333333", fg="white", width=2, 
                                       command=lambda index=i: self.delete_timer(index))
            delete_button.pack(side="right", padx=5)

    def delete_timer(self, index):
        """Löscht einen Timer."""
        self.timer_marks.pop(index)
        self.timer_times.pop(index)
        self.timer_notes.pop(index)
        self.update_timer_list()

    def update_clock(self):
        """Aktualisiert die Uhrzeit."""
        self.canvas.delete("all")
        self.draw_face()
        self.draw_timer_marks()
        now = datetime.now()
        self.draw_hands(now.hour, now.minute)

        self.blink_state = not self.blink_state  # Blink-Zustand wechseln
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    clock = AnalogClock(root)
    root.mainloop()
