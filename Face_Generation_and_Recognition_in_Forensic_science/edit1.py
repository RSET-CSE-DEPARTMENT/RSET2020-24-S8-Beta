import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys
from PIL import Image, ImageTk

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display App")

        # Load and display the first image (replace 'image1.jpg' with the path to your image)
        self.image1 = Image.open(r"D:\college\Projects\pythonProject\TediGAN\base\examples\142.jpg")
        self.image1 = self.image1.resize((200, 200))  # Resize the image if needed
        self.photo1 = ImageTk.PhotoImage(self.image1)
        self.image1_label = tk.Label(root, image=self.photo1)
        self.image1_label.pack()

        # Create text entry
        self.entry = tk.Entry(root)
        self.entry.pack()

        # Create button
        self.button = tk.Button(root, text="Edit image", command=self.display_second_image)
        self.button.pack()

        # Placeholder for the second image
        self.image2_label = tk.Label(root)

    def display_second_image(self):
        # Get user input from the text entry
        user_input = self.entry.get()
        file_path = r"D:\college\Projects\pythonProject\TediGAN\base\invert.py"
        if os.path.exists(file_path):
            # Construct the subprocess command
            command = [sys.executable, file_path, "--description", user_input,"--image_path", "D:\\college\\Projects\\pythonProject\\142.jpg"]

            # Execute the subprocess command
            subprocess.Popen(command).wait()

            # Load and display the second image (replace 'image2.jpg' with the path to your image)
            self.image2 = Image.open(r"D:\college\Projects\pythonProject\TediGAN\base\results\inversion\test\142_inv.png")
            self.image2 = self.image2.resize((200, 200))  # Resize the image if needed
            self.photo2 = ImageTk.PhotoImage(self.image2)
            self.image2_label.config(image=self.photo2)
            self.image2_label.image = self.photo2  # Keep a reference to prevent garbage collection
            self.image2_label.pack()  # Display the second image
        else:
            messagebox.showerror("File Not Found", "invert.py not found at the specified location.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
