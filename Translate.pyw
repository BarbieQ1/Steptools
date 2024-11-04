import tkinter as tk
from googletrans import Translator, LANGUAGES

class TranslatorApp:
    def __init__(self, root):
        self.translator = Translator()
        root.title("Sprachübersetzer")
        root.geometry("400x250")
        root.configure(bg="#1c1c1c")
        root.attributes("-topmost", True)

        self.input_label = tk.Label(root, text="Text eingeben:", bg="#1c1c1c", fg="white")
        self.input_label.pack(pady=(10, 0))

        self.input_text = tk.Text(root, height=3, width=40, bg="#333333", fg="white", wrap="word")
        self.input_text.pack(pady=5)

        self.translate_button = tk.Button(root, text="Übersetzen", command=self.translate_text, bg="#444444", fg="white")
        self.translate_button.pack(pady=5)

        self.output_label = tk.Label(root, text="Übersetzung:", bg="#1c1c1c", fg="white")
        self.output_label.pack(pady=(10, 0))

        self.output_text = tk.Text(root, height=3, width=40, bg="#333333", fg="white", wrap="word", state="disabled")
        self.output_text.pack(pady=5)

    def translate_text(self):
        input_text = self.input_text.get("1.0", "end-1c")
        if input_text.strip():
            detected_lang = self.translator.detect(input_text).lang
            target_lang = "en" if detected_lang == "de" else "de"
            
            translated = self.translator.translate(input_text, src=detected_lang, dest=target_lang)
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", translated.text)
            self.output_text.config(state="disabled")

root = tk.Tk()
app = TranslatorApp(root)
root.mainloop()
