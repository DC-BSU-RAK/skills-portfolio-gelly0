import tkinter as tk
from tkinter import PhotoImage
import random
import pyttsx3
import winsound
import os

# Always locate files relative to this .py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Tell Me A Joke!")
        
        # Window Icon
        icon_path = os.path.join(BASE_DIR, "Alexa tell me a Joke.ico")
        self.root.iconbitmap(icon_path)

        # Window size
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Safe paths for images
        img1_path = os.path.join(BASE_DIR, "img_1.png")
        img2_path = os.path.join(BASE_DIR, "img_2.png")

        # Load and resize background images
        self.start_bg = PhotoImage(file=img1_path).subsample(
            1024 // 900 if 1024 > 900 else 1,
            768 // 600 if 768 > 600 else 1
        )

        self.joke_bg = PhotoImage(file=img2_path).subsample(
            1024 // 900 if 1024 > 900 else 1,
            768 // 600 if 768 > 600 else 1
        )

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
            font=("Arial", 16, "bold"),
            fg="white", bg="#6b3b12",
            activeforeground="white", activebackground="#6b3b12",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.go_to_joke_screen
        )
        self.start_button.place(x=170, y=400, width=160, height=60)

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
        self.ask_button.place(x=165, y=115, width=280, height=60)

        self.quit_button = tk.Button(
            self.joke_frame, text="Quit",
            font=("Arial", 16, "bold"),
            fg="white", bg="#cc0000",
            activeforeground="white", activebackground="#cc0000",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.root.quit
        )
        self.quit_button.place(x=535, y=115, width=140, height=60)

        self.setup_label = tk.Label(
            self.joke_frame, text="", bg="white",
            font=("Arial", 16), wraplength=500, justify="center"
        )
        self.setup_label.place(x=150, y=210, width=600, height=80)

        self.punchline_label = tk.Label(
            self.joke_frame, text="", bg="white",
            font=("Arial", 15, "italic"), wraplength=500, justify="center"
        )
        self.punchline_label.place(x=150, y=310, width=600, height=80)

        self.next_button = tk.Button(
            self.joke_frame, text="Next Joke",
            font=("Arial", 16, "bold"),
            fg="white", bg="#6c3b18",
            activeforeground="white", activebackground="#6c3b18",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.show_random_joke
        )
        self.next_button.place(x=235, y=425, width=140, height=60)

        self.punchline_button = tk.Button(
            self.joke_frame, text="Show Punchline",
            font=("Arial", 14, "bold"),
            fg="white", bg="#6c3b18",
            activeforeground="white", activebackground="#6c3b18",
            relief="flat", borderwidth=0, highlightthickness=0, cursor="hand2",
            command=self.show_punchline
        )
        self.punchline_button.place(x=505, y=425, width=255, height=60)

    # BACKGROUND MUSIC
    def play_background_music(self):
        """Loop background music forever."""
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
        winsound.PlaySound(self.laugh_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.root.after(3200, self.play_background_music)

    # NAVIGATION
    def go_to_joke_screen(self):
        self.start_frame.pack_forget()
        self.joke_frame.pack()

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
        with open(joke_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "?" in line:
                    q, p = line.split("?", 1)
                    jokes.append((q + "?", p.strip()))
        return jokes


if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()