import os
import subprocess

# Install required modules
try:
    import requests
    from bs4 import BeautifulSoup
    
    import tkinter as tk
    from tkinter import ttk

    from datetime import datetime
    import locale
    
    locale.setlocale(locale.LC_ALL, 'en_US')
    
    import webbrowser
    running = False 
    cb1value = 2;
    languageflag=[["fr-fr","de-de","en-us"],
    ["Notes de mise à jour","S'inscrire","Lire plus", "Notes de mise à jour", "Présentation", "Actualités"],
    ["Versionshinweise","Anmelden","Mehr lesen", "Versionshinweise", "Vorgestellt", "Aktuelles"],
    ["Release Notes","Sign Up","Read More", "Release Notes", "Showcase", "Updates"]]
    
    dateformate=["%d %B %Y","%d. %B %Y","%B %d, %Y"]
    dateformat = "%B %d, %Y"

except ImportError:
    subprocess.check_call(["pip", "install", "requests", "beautifulsoup4"])
    import requests
    from bs4 import BeautifulSoup
    import tkinter as tk
    import locale
    locale.setlocale(locale.LC_TIME,'')
    from datetime import datetime
    import webbrowser
    

def get_filtered_news_content():


    
    current_dateTime = datetime.now()
    url = "https://www.playlostark.com/" + languageflag[0][cb1value] + "/news"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text(separator='\n', strip=True)
        start_index = content.find(languageflag[cb1value+1][0])
        end_index = content.find(languageflag[cb1value+1][1])
        if start_index != -1 and end_index != -1:
            filtered_content = content[start_index:end_index].strip()
            return [
                line for line in filtered_content.split('\n')
                if not any(keyword in line for keyword in [languageflag[cb1value+1][2], languageflag[cb1value+1][3], languageflag[cb1value+1][4], languageflag[cb1value+1][5]])
                and not (line.split()[0].isdigit() and line.endswith("KB"))
                
            ]
    return []

def parse_date(line):
    global dateformat
    try:
        return datetime.strptime(line, dateformat)
    except ValueError:
        return None

def refresh_content(text_widget, previous_content, notify_var, notification_label, confirm_button):


    text_widget.delete(1.0, tk.END)
    filtered_lines = get_filtered_news_content()
    entries, current_date, current_details = [], None, []
    for line in filtered_lines:
        date = parse_date(line)
        if date:
            if current_date:
                entries.append((current_date, current_details))
            current_date, current_details = line, []
        else:
            current_details.append(line)
    if current_date:
        entries.append((current_date, current_details))
    entries.sort(key=lambda x: parse_date(x[0]), reverse=True)
    new_content = []
    for date, details in entries:
        text_widget.insert(tk.END, "------------------------------\n", "separator")
        text_widget.insert(tk.END, f"{date}\n", "date")
        for detail in details:
            text_widget.insert(tk.END, f"{detail}\n", "detail")
        text_widget.insert(tk.END, "\n")
        new_content.append(f"{date}\n" + "\n".join(details))
    text_widget.yview_moveto(0)
    if notify_var.get() and new_content != previous_content:
        notification_label.config(text="New content is available!", fg="#FF6347")
        previous_content.clear()
        previous_content.extend(new_content)
        confirm_button.pack()
    else:
        confirm_button.pack_forget()

def start_auto_refresh(text_widget, interval_entry, notify_var, previous_content, notification_label, confirm_button,auto_refresh_button):
    try:
        interval = int(interval_entry.get())
        global running
        if interval > 0 and running == False:
            running = True
            def auto_refresh():
                global running
                if running:
                    auto_refresh_button.config(bg = 'red',text='Stop Auto Refresh')
                    refresh_content(text_widget, previous_content, notify_var, notification_label, confirm_button)
                    window.after(interval * 1000, auto_refresh)
            auto_refresh()
        else:
            running = False
            auto_refresh_button.config(bg="#444444",text='Start Auto Refresh')
            
    except ValueError:
        pass


def display_selection(event):
    global cb1value
    global dateformat
    global dateformate
    cb1value = event.widget.current()
    locale.setlocale(locale.LC_ALL, event.widget.get())
    dateformat = dateformate[cb1value]
    event.widget.selection_clear()



    
def display_news():
    global window
    global running
    window = tk.Tk()
    window.title("Lost Ark News Content")
    window.geometry("600x800")
    window.configure(bg="#2E2E2E")
    scrollbar = tk.Scrollbar(window, bg="#444444", troughcolor="#2E2E2E", highlightbackground="#444444")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget = tk.Text(window, wrap=tk.WORD, yscrollcommand=scrollbar.set, width=80, height=30, bg="#1E1E1E", fg="#FFFFFF", insertbackground="#FFFFFF", highlightthickness=0)
    text_widget.tag_configure("date", foreground="#FFD700", font=("Helvetica", 12, "bold"))
    text_widget.tag_configure("separator", foreground="#888888")
    text_widget.tag_configure("detail", foreground="#FFFFFF")
    text_widget.pack()
    scrollbar.config(command=text_widget.yview)
    previous_content = []
    notify_var = tk.BooleanVar()
    notification_label = tk.Label(window, text="", bg="#2E2E2E", fg="#FF6347")
    notification_label.pack()
    confirm_button = tk.Button(window, text="✔ Acknowledge Update", command=lambda: notification_label.config(text=""), bg="#444444", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF")
    confirm_button.pack_forget()
    
    refresh_content(text_widget, previous_content, notify_var, notification_label, confirm_button)
    refresh_button = tk.Button(window, text="Refresh", command=lambda: refresh_content(text_widget, previous_content, notify_var, notification_label, confirm_button), bg="#444444", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF")
    refresh_button.pack()
    auto_refresh_button = tk.Button(window, text="Start Auto-refresh", command=lambda: start_auto_refresh(text_widget, interval_entry, notify_var, previous_content, notification_label, confirm_button,auto_refresh_button), bg="#444444", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF")
    auto_refresh_button.pack()
    interval_label = tk.Label(window, text="Auto-refresh interval (seconds):", bg="#2E2E2E", fg="#FFFFFF" )
    interval_label.pack()
    interval_entry = tk.Entry(window, bg="#3C3C3C", fg="#FFFFFF", insertbackground="#FFFFFF")
    interval_entry.pack()
    notify_checkbox = tk.Checkbutton(window, text="Notify on Update", variable=notify_var, bg="#2E2E2E", fg="#FFFFFF", selectcolor="#444444", activebackground="#2E2E2E", activeforeground="#FFFFFF")
    notify_checkbox.pack()

    # style= ttk.Style()
    # style.theme_use('clam')
    # style.configure("TCombobox", selectbackground= "red", background= "white")
    # window.option_add("*TCombobox*Listbox*Background", 'green',*selectbackground, "red")
    
    
    style = ttk.Style()
    style.theme_use('alt')
    ebg = '#2E2E2E'
    fg = '#FFFFFF'
    window.option_add('*TCombobox*Listbox*Background', ebg)
    window.option_add('*TCombobox*Listbox*Foreground', fg)
    window.option_add('*TCombobox*Listbox*selectBackground', fg)
    window.option_add('*TCombobox*Listbox*selectForeground', ebg)

    lang=['fr_FR','de_DE','en_US'] # options
    cb1 = ttk.Combobox(window, state="readonly", values=lang,width=6, justify='center') # Combobox
    cb1.current(2)
    # cb1.bind("<FocusIn>", Defocus)
    cb1.bind("<<ComboboxSelected>>", display_selection)
    cb1.pack()


    
    
    def open_news_page():
        webbrowser.open("https://www.playlostark.com/en-us/news")
    hyperlink_button = tk.Button(window, text="Open Lost Ark News Page", command=open_news_page, bg="#444444", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF")
    hyperlink_button.pack(pady=10)
    window.mainloop()
    

display_news()

