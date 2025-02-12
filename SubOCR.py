import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
import easyocr
import pyscreenshot as ss
from pynput import keyboard
import threading


text_field_value = ""  
reader = easyocr.Reader(['en']) 
active=False
click_count = 0


def ss_active():
 global active
 active=True
 print(active)

 
def capture_screenshot(filename):
    image = ss.grab()   
    image.save(filename)


def change_language():
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    EN = tk.Button(new_window, text="En", command=lambda: set_language('en'))
    EN.pack(pady=10)
    TR = tk.Button(new_window, text="Tr", command=lambda: set_language('tr'))
    TR.pack(pady=10)
    DE = tk.Button(new_window, text="De", command=lambda: set_language('de'))
    DE.pack(pady=10)
    BS = tk.Button(new_window, text="Bs", command=lambda: set_language('bs'))
    BS.pack(pady=10)



def show_menu(event):
    x = button.winfo_rootx()
    y = button.winfo_rooty() + button.winfo_height()
    menu.post(x, y)









def set_language(language):
    global selected_language, reader
    selected_language = language
    reader = easyocr.Reader([selected_language])
    print(f"Language set to {selected_language}")


     
def filename():
    global text_field_value
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    
    text_field = tk.Entry(new_window, width=50)
    text_field.pack(pady=20)

    label = tk.Label(new_window, text="Enter file name:")
    label.pack(pady=10)
    
    save = tk.Button(new_window, text="Save file", command=lambda: update_global_text(text_field))
    save.pack(pady=10)


  
def update_global_text(entry_widget):
    global text_field_value
    text_field_value = entry_widget.get()  # Update the global text_field_value variable
    print(f"File name set to: {text_field_value}")






    
def on_press(key):
    global text_field_value
    if (key == keyboard.KeyCode(char='b') or key == keyboard.KeyCode(char='B')) and active:
        if text_field_value:  # Ensure text_field_value is not empty
            capture_screenshot("a.png")
            print("Screenshot captured.")
            image_path = 'a.png'
            results = reader.readtext(image_path)
            fulltext = ' '.join([result[1] for result in results])
            file_path = f"{text_field_value}.txt"
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(fulltext)
            print(f"Text extracted and saved to {file_path}:")
            print(fulltext)
        else:
            print("No file name provided.")


root = tk.Tk()
root.title("File Downloader")


menu = tk.Menu(root, tearoff=0)
menu.add_command(label="En", command=lambda:set_language('en'))
menu.add_command(label="Bs", command=lambda: set_language('bs'))
menu.add_command(label="Tr", command=lambda: set_language('tr'))
menu.add_command(label="De", command=lambda: set_language('de'))












download_button = tk.Button(root, text="START OCR", command=ss_active)
download_button.pack(pady=10)
change_language_button=tk.Button(root, text="CHANGE LANGUAGE", command=change_language)
change_language_button.pack(pady=10)
filesettings_button = tk.Button(root, text="set file name", command=filename)
filesettings_button.pack(pady=10)
entry_var = tk.StringVar()
entry_var.trace_add("write", filename)
button = tk.Button(root, text="Hover over me")
button.pack(pady=20)
button.bind("<Enter>", show_menu)



def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

keyboard_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
keyboard_thread.start()

root.mainloop()


