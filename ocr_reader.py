import pytesseract
import pyttsx3
import tkinter as tk
from tkinter import messagebox, filedialog
import pyperclip
from PIL import Image

# Optional: set tesseract path (if not in system PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def show_text_options(text):
    def copy_text():
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Text copied to clipboard!")

    def save_text():
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Text saved to {path}")

    def read_aloud():
        speak_text(text)

    # Create UI window
    root = tk.Tk()
    root.title("Extracted Text")
    root.geometry("600x400")

    text_box = tk.Text(root, wrap='word', font=("Arial", 12))
    text_box.insert("1.0", text)
    text_box.pack(expand=True, fill='both')

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="📋 Copy Text", command=copy_text).pack(side='left', padx=10)
    tk.Button(btn_frame, text="💾 Save Text", command=save_text).pack(side='left', padx=10)
    tk.Button(btn_frame, text="🔊 Read Aloud", command=read_aloud).pack(side='left', padx=10)

    root.mainloop()

# ---- Trigger OCR Flow ---- #
image_path = "gesture_capture.png"
print("[🧠] Performing OCR...")
text_result = extract_text(image_path)

if text_result:
    print("[✅] Text extracted successfully!")
    show_text_options(text_result)
else:
    print("[⚠️] No text found in the selected region.")
    tk.messagebox.showinfo("No Text", "No readable text was found in the image.")
