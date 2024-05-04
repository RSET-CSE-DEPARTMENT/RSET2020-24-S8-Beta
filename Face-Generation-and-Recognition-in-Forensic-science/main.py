import os
import subprocess
import sys
import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
import spacy
import speech_recognition as sr

r = sr.Recognizer()
# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "user" and password == "pass":
        show_login_page()
        hide_main_page_widgets()
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")

def show_login_page():
    global search_button  # Make search_button global
    global mic_button  # Make mic_button global
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    global entry
    entry = tk.Entry(canvas)
    entry.place(relx=0.79, rely=0.2, anchor="center")
    search_button = tk.Button(canvas, text="Search", command=search, font=("Arial", 14), bg="white", fg="black")
    search_button.place(relx=0.8, rely=0.35, anchor="center")
    # Example using an image for the microphone button
    mic_image = PhotoImage(file="D:\\college\\Projects\\Main Project\\pythonProject\\micro.png")
    mic_image_resized = mic_image.subsample(30, 30)

    # Replace the emoji with a text representation for the microphone button

    mic_button = tk.Button(canvas, image=mic_image_resized, command=run_audio, bg="white", bd=0)
    mic_button.image = mic_image_resized  # to prevent garbage collection
    mic_button.place(x=590, y=77)
    global result_label
    result_label = tk.Label(canvas, text="", font=("Arial", 12), bg="white", fg="black", bd=0)
    result_label.place(relx=0.8, rely=0.5, anchor="center")

def hide_main_page_widgets():
    login_button.place_forget()
    username_entry.place_forget()
    password_entry.place_forget()

def hide_main_page_wid():
    search_button.place_forget()
    mic_button.place_forget()
    entry.place_forget()
    result_label.place_forget()

def search():
    try:
        new_bg_color = "royalblue"  # Set the desired background color
    except Exception as e:
        print("Error loading background color:", e)
        return

    hide_main_page_wid()  # Hide existing widgets
    canvas.delete("all")  # Clear the canvas

    # Create a rectangle with the specified background color
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=new_bg_color)

    search_image = PhotoImage(file="img12.png")
    canvas.search_image = search_image  # Keep a reference to avoid garbage collection
    canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=search_image)

    # Create "Edit" button
    edit_button = tk.Button(canvas, text="Edit", command=edit, font=("Arial", 14), bg="white", fg="black")
    edit_button.place(relx=0.8, rely=0.35, anchor="center")

    # Create "Match" button
    match_button = tk.Button(canvas, text="Match", command=match, font=("Arial", 14), bg="white", fg="black")
    match_button.place(relx=0.8, rely=0.45, anchor="center")

def edit():
    file_path = "D:\college\Projects\pythonProject\edit.py"
    if os.path.exists(file_path):
        # Execute the edit.py script
        subprocess.Popen([sys.executable, file_path])
    else:
        messagebox.showerror("File Not Found", "edit.py not found at the specified location.")
    # if file_path:
    #     # Execute the selected Python file
    #     with open(file_path, 'r') as file:
    #         code = file.read()
    #         exec(code, {"os": os})
    # # Add functionality for the "Edit" button here
pass
def match():
    file_path ="D:\college\Projects\pythonProject\match.py"
    if file_path:
        # Execute the selected Python file
        with open(file_path, 'r') as file:
            code = file.read()
            exec(code, {"os": os})

def run_audio():
    with sr.Microphone() as source:
        try:
            # Listen for audio input
            audio_data = r.listen(source, timeout=15)  # Record audio for 15 seconds

            # Recognize speech
            text = r.recognize_google(audio_data)
            entry.insert(tk.END, text)
        except sr.UnknownValueError:
            result_label.config(text="Sorry, could not understand audio.")
        except sr.RequestError as e:
            result_label.config(text="Could not request results; {0}".format(e))

root = tk.Tk()
root.title("Forensic Face Generation")

bg_image = PhotoImage(file="D:\college\Projects\Main Project\\background.png")

frame = tk.Frame(root)
frame.pack()

canvas = tk.Canvas(frame, bd=2, highlightthickness=0, width=650, height=435)
canvas.create_image(0, 0, image=bg_image, anchor="nw")
canvas.pack(fill="both", expand=True)

canvas.create_text(550, 50, text="LOGIN", fill="white", font=('CalistoMT 18 bold'))

canvas.create_text(450, 115, text="Username:", fill="white", )
username_entry = tk.Entry(canvas)
username_entry.place(x=490, y=106)

canvas.create_text(450, 145, text="Password: ", fill="white", )
password_entry = tk.Entry(canvas, show="*")
password_entry.place(x=490, y=136)

login_button = tk.Button(canvas, text="Login", fg="white", bg="midnight blue", command=login)
login_button.place(x=535, y=175)

root.minsize(650, 435)
root.mainloop()