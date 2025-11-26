import tkinter as tk
from tkinter import PhotoImage
import random
import pyttsx3
import winsound
import os
from PIL import Image, ImageTk

# Always locate files relative to this .py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Tell Me A Joke!")
        
        # Window Icon
        icon_path = os.path.join(BASE_DIR, "Alexa tell me a Joke.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        # Window size
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Safe paths for images
        img1_path = os.path.join(BASE_DIR, "img_1.png")
        img2_path = os.path.join(BASE_DIR, "img_2.png")
        instructions_path = os.path.join(BASE_DIR, "Instructions.png")

        # Load and resize background images to fit 900x600
        self.start_bg = self.load_and_resize_image(img1_path, 900, 600)
        self.joke_bg = self.load_and_resize_image(img2_path, 900, 600)
        self.instructions_bg = self.load_and_resize_image(instructions_path, 900, 600)

        # Sound paths (safe)
        self.laugh_sound = os.path.join(BASE_DIR, "laugh.wav")
        self.bg_music = os.path.join(BASE_DIR, "bg_music.wav")

        # Start background music immediately
        self.play_background_music()

        # Load jokes safely
        self.jokes = self.load_jokes()
        self.current_setup = ""
        self.current_punchline = ""

        # START SCREEN
        self.start_frame = tk.Frame(self.root, width=900, height=600)
        self.start_frame.pack()

        self.start_bg_label = tk.Label(self.start_frame, image=self.start_bg)
        self.start_bg_label.place(x=0, y=0, width=900, height=600)

        self.start_button = tk.Button(
            self.start_frame, text="Start",
            font=("Arial", 20, "bold"),
            fg="white", bg="#6c3b18",
            activeforeground="white", activebackground="#6c3b18",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.go_to_joke_screen
        )
        self.start_button.place(x=200, y=377, width=145, height=50)

        # INSTRUCTIONS BUTTON ON START SCREEN
        self.instructions_button = tk.Button(
            self.start_frame, text="Instructions",
            font=("Arial", 20, "bold"),
            fg="white", bg="#6c3b18",
            activeforeground="white", activebackground="#6c3b18",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.show_instructions
        )
        self.instructions_button.place(x=225, y=438, width=195, height=50)

        # JOKE SCREEN
        self.joke_frame = tk.Frame(self.root, width=900, height=600)

        self.joke_bg_label = tk.Label(self.joke_frame, image=self.joke_bg)
        self.joke_bg_label.place(x=0, y=0, width=900, height=600)

        self.ask_button = tk.Button(
            self.joke_frame, text="Alexa tell me a joke",
            font=("Arial", 14, "bold"),
            fg="white", bg="#6c3b18",
            activeforeground="white", activebackground="#6c3b18",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.show_random_joke
        )
        self.ask_button.place(x=201, y=156, width=237, height=45)

        self.quit_button = tk.Button(
            self.joke_frame, text="Quit",
            font=("Arial", 16, "bold"),
            fg="white", bg="#cc0000",
            activeforeground="white", activebackground="#cc0000",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.root.quit
        )
        self.quit_button.place(x=515, y=156, width=140, height=45)

        self.setup_label = tk.Label(
            self.joke_frame, text="", bg="white",
            font=("Arial", 16), wraplength=500, justify="center"
        )
        self.setup_label.place(x=150, y=221, width=590, height=70)

        self.punchline_label = tk.Label(
            self.joke_frame, text="", bg="white",
            font=("Arial", 15, "italic"), wraplength=500, justify="center"
        )
        self.punchline_label.place(x=150, y=306, width=590, height=70)

        self.next_button = tk.Button(
            self.joke_frame, text="Next Joke",
            font=("Arial", 16, "bold"),
            fg="white", bg="#6c3b18",
            activeforeground="white", activebackground="#6c3b18",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.show_random_joke
        )
        self.next_button.place(x=250, y=399, width=140, height=45)

        self.punchline_button = tk.Button(
            self.joke_frame, text="Show Punchline",
            font=("Arial", 14, "bold"),
            fg="white", bg="#6c3b18",
            activeforeground="white", activebackground="#6c3b18",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.show_punchline
        )
        self.punchline_button.place(x=485, y=399, width=237, height=45)

        # INSTRUCTIONS SCREEN
        self.instructions_frame = tk.Frame(self.root, width=900, height=600)
        
        self.instructions_bg_label = tk.Label(self.instructions_frame, image=self.instructions_bg)
        self.instructions_bg_label.place(x=0, y=0, width=900, height=600)
        
        # Back button on instructions screen
        self.back_button = tk.Button(
            self.instructions_frame, text="Back",
            font=("Arial", 16, "bold"),
            fg="white", bg="#6c3b18",
            activeforeground="white", activebackground="#6c3b18",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.go_to_start_screen
        )
        self.back_button.place(x=630, y=463, width=145, height=45)

    def load_and_resize_image(self, image_path, width, height):
        """Load and resize image to fit the specified dimensions"""
        try:
            # Try using PIL for better image resizing
            from PIL import Image, ImageTk
            image = Image.open(image_path)
            image = image.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except ImportError:
            # Fallback to tkinter if PIL is not available
            print("PIL not available, using tkinter subsampling")
            photo = PhotoImage(file=image_path)
            # Calculate subsample factors
            orig_width = photo.width()
            orig_height = photo.height()
            
            x_ratio = orig_width // width
            y_ratio = orig_height // height
            
            # Use the larger ratio to maintain aspect ratio
            ratio = max(x_ratio, y_ratio)
            
            if ratio > 1:
                return photo.subsample(ratio, ratio)
            else:
                return photo

    # BACKGROUND MUSIC
    def play_background_music(self):
        """Loop background music forever."""
        if os.path.exists(self.bg_music):
            winsound.PlaySound(self.bg_music, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

    # SPEECH FUNCTION
    def speak(self, text):
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty('voices')
        for v in voices:
            if "Zira" in v.name:
                engine.setProperty('voice', v.id)
                break

        engine.say(text)
        engine.runAndWait()

    # LAUGH EFFECT (LONGER + NO CUT)
    def play_laugh(self):
        """Play laugh fully, then resume background music."""
        if os.path.exists(self.laugh_sound):
            winsound.PlaySound(self.laugh_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.root.after(3200, self.play_background_music)

    # NAVIGATION
    def go_to_joke_screen(self):
        self.start_frame.pack_forget()
        self.joke_frame.pack()

    def go_to_start_screen(self):
        self.instructions_frame.pack_forget()
        self.start_frame.pack()

    def show_instructions(self):
        self.start_frame.pack_forget()
        self.instructions_frame.pack()

    def show_random_joke(self):
        if self.jokes:
            setup, punchline = random.choice(self.jokes)
            self.current_setup = setup
            self.current_punchline = punchline

            self.setup_label.config(text=setup)
            self.punchline_label.config(text="")

            # Update UI BEFORE speaking
            self.root.update_idletasks()
            self.root.update()

            self.speak(setup)

    def show_punchline(self):
        self.punchline_label.config(text=self.current_punchline)

        self.root.update_idletasks()
        self.root.update()

        self.speak(self.current_punchline)

        self.play_laugh()

    # LOAD JOKES
    def load_jokes(self):
        joke_file = os.path.join(BASE_DIR, "randomJokes.txt")
        jokes = []
        try:
            with open(joke_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "?" in line:
                        q, p = line.split("?", 1)
                        jokes.append((q + "?", p.strip()))
        except FileNotFoundError:
            print(f"Joke file not found: {joke_file}")
        return jokes


if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()