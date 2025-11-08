import tkinter as tk
from tkinter import messagebox
import random

class MathsQuizGame:
    def __init__(self, root):
        # Initialize main game window with fullscreen and dark theme
        self.root = root
        self.root.title("Math Quest Adventure")  # Set window title
        self.root.attributes('-fullscreen', True)  # Start in fullscreen mode
        self.root.configure(bg='#0a0a1a')  # Set dark blue background color
        self.root.bind('<Escape>', self.toggle_fullscreen)  # Bind ESC key to toggle fullscreen
        
        # Initialize game state variables
        self.difficulty = None  # Store current difficulty level
        self.score = 0  # Player's current score
        self.current_question = 0  # Track current question number
        self.total_questions = 10  # Total questions per game
        self.current_attempt = 1  # Track attempt count per question (1 or 2)
        self.num1 = 0  # First number in math problem
        self.num2 = 0  # Second number in math problem
        self.operation = ''  # Math operation (+ or -)
        self.correct_answer = 0  # Store correct answer for current problem
        self.combo = 0  # Track consecutive correct answers
        self.max_combo = 0  # Track highest combo achieved
        
        # Initialize UI elements
        self.attempt_label = None  # Label to show current attempt
        
        # Define color scheme for consistent styling
        self.colors = {
            'bg': '#0a0a1a',        # Dark blue background
            'primary': '#00ff88',   # Green for primary elements
            'secondary': '#0088ff', # Blue for secondary elements
            'accent': '#ff0088',    # Pink for accents
            'danger': '#ff4444',    # Red for dangerous actions
            'warning': '#ffaa00',   # Orange for warnings
            'text': '#ffffff'       # White for text
        }
        
        # Create main container frame
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Display the main menu
        self.displayMenu()

    def toggle_fullscreen(self, event=None):
        # Toggle fullscreen mode with ESC key
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def exit_fullscreen(self, event=None):
        # Exit fullscreen mode
        self.root.attributes('-fullscreen', False)
    
    def create_game_button(self, parent, text, command, color='primary', width=20, font_size=12):
        # Create styled buttons with consistent appearance
        bg_color = self.colors[color]  # Get background color from scheme
        return tk.Button(parent, text=text, font=('Arial', font_size, 'bold'), width=width, height=2,
            bg=bg_color, fg=self.colors['text'], activebackground=self.colors['accent'],
            activeforeground=self.colors['text'], relief='raised', borderwidth=3, cursor='hand2', command=command)
    
    def create_game_label(self, parent, text, font_size=12, is_title=False, color='text'):
        # Create styled labels with consistent appearance
        font_style = ('Arial', font_size, 'bold') if is_title else ('Arial', font_size)
        return tk.Label(parent, text=text, font=font_style, bg=self.colors['bg'], fg=self.colors[color], wraplength=500)
    
    def displayMenu(self):
        # Display main menu with game options and stats
        self.clear_frame()  # Clear any existing widgets
        
        # Create and pack title label
        title_label = self.create_game_label(self.main_frame, "🏰 MATH QUEST ADVENTURE", 36, True, 'primary')
        title_label.pack(pady=30)
        
        # Create and pack subtitle label
        subtitle_label = self.create_game_label(self.main_frame, "Embark on a Mathematical Journey!", 18, False, 'secondary')
        subtitle_label.pack(pady=5)
        
        # Create and pack screen info label
        screen_info = self.create_game_label(self.main_frame, "Press ESC to exit full screen", 12, False, 'secondary')
        screen_info.pack(pady=5)
        
        # Create menu buttons frame
        menu_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        menu_frame.pack(pady=40)
        
        # Create and pack difficulty selection button
        difficulty_btn = self.create_game_button(menu_frame, "🎯 DIFFICULTY LEVEL", self.showDifficultyLevel, 'primary', 25, 14)
        difficulty_btn.pack(pady=15)
        
        # Create and pack instructions button
        instructions_btn = self.create_game_button(menu_frame, "📖 INSTRUCTIONS", self.showInstructions, 'warning', 25, 14)
        instructions_btn.pack(pady=15)
        
        # Create and pack exit game button
        exit_btn = self.create_game_button(menu_frame, "🚪 EXIT GAME", self.confirm_quit, 'danger', 25, 14)
        exit_btn.pack(pady=15)
        
        # Create stats display frame
        stats_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        stats_frame.pack(pady=20)
        
        # Create and pack stats label with high score and max combo
        stats_text = f"🏆 High Score: {self.get_high_score()} | 🔥 Max Combo: {self.max_combo}"
        stats_label = self.create_game_label(stats_frame, stats_text, 12, False, 'secondary')
        stats_label.pack()
    
    def showDifficultyLevel(self):
        # Show difficulty selection screen with three options
        self.clear_frame()  # Clear existing widgets
        
        # Create back button to return to main menu
        back_btn = self.create_game_button(self.main_frame, "← Back to Menu", self.displayMenu, 'accent', 15, 12)
        back_btn.pack(anchor='nw', pady=10)
        
        # Create and pack difficulty selection title
        title_label = self.create_game_label(self.main_frame, "DIFFICULTY LEVEL", 28, True, 'primary')
        title_label.pack(pady=20)
        
        # Create and pack difficulty selection subtitle
        subtitle_label = self.create_game_label(self.main_frame, "Choose Your Challenge Level!", 16, False, 'secondary')
        subtitle_label.pack(pady=10)
        
        # Define difficulty levels with names, descriptions, values and colors
        difficulties = [
            ("🌱 Easy", "Single Digit Numbers (0-9)", "easy", "primary"),
            ("⚡ Moderate", "Double Digit Numbers (10-99)", "moderate", "warning"), 
            ("🔥 Advanced", "Four Digit Numbers (1000-9999)", "advanced", "danger")
        ]
        
        # Create buttons for each difficulty level
        for diff_name, diff_desc, diff_value, color in difficulties:
            # Create frame for each difficulty option
            diff_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
            diff_frame.pack(pady=15)
            
            # Create difficulty selection button
            diff_btn = self.create_game_button(diff_frame, diff_name, lambda d=diff_value: self.start_quiz(d), color, 25, 14)
            diff_btn.pack(pady=5)
            
            # Create description label for difficulty level
            desc_label = self.create_game_label(diff_frame, diff_desc, 12, False, 'text')
            desc_label.pack()
    
    def showInstructions(self):
        # Display game instructions and rules
        self.clear_frame()  # Clear existing widgets
        
        # Create back button to return to main menu
        back_btn = self.create_game_button(self.main_frame, "← Back to Menu", self.displayMenu, 'accent', 15)
        back_btn.pack(anchor='nw', pady=10)
        
        # Create and pack instructions title
        title_label = self.create_game_label(self.main_frame, "📖 GAME INSTRUCTIONS", 24, True, 'primary')
        title_label.pack(pady=20)
        
        # Define instruction text with sections
        instructions = [
            "🎯 HOW TO PLAY:", "• Select a difficulty level to start your math adventure",
            "• Answer 10 arithmetic questions (addition or subtraction)", "• You get 2 attempts per question", "",
            "💰 SCORING SYSTEM:", "• First attempt correct: 10 points", "• Second attempt correct: 5 points", 
            "• Wrong answer: 0 points", "", "🔥 COMBO SYSTEM:", "• Correct answers build your combo streak",
            "• Higher combos = more excitement!", "", "🏆 DIFFICULTY LEVELS:", "• Easy: Single digit numbers (0-9)",
            "• Moderate: Double digit numbers (10-99)", "• Advanced: Four digit numbers (1000-9999)", "",
            "💡 TIP: Practice makes perfect! Start with Easy and work your way up!", "", "🖥️ CONTROLS:",
            "• Press ESC to toggle full screen mode", "• Use Enter key to submit answers quickly"
        ]
        
        # Create frame for instructions content
        instructions_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        instructions_frame.pack(pady=20)
        
        # Create labels for each instruction line
        for instruction in instructions:
            # Check for section headers and style them differently
            if instruction.startswith("🎯") or instruction.startswith("💰") or instruction.startswith("🔥") or instruction.startswith("🏆") or instruction.startswith("💡") or instruction.startswith("🖥️"):
                label = self.create_game_label(instructions_frame, instruction, 12, True, 'warning')
            elif instruction == "":  # Empty line for spacing
                label = self.create_game_label(instructions_frame, " ", 8, False, 'text')
            else:  # Regular instruction text
                label = self.create_game_label(instructions_frame, instruction, 10, False, 'text')
            label.pack(pady=2)
    
    def randomInt(self, difficulty):
        # Generate random numbers based on selected difficulty
        if difficulty == "easy": 
            return random.randint(0, 9)  # Single digit numbers
        elif difficulty == "moderate": 
            return random.randint(10, 99)  # Double digit numbers
        else: 
            return random.randint(1000, 9999)  # Four digit numbers
    
    def decideOperation(self):
        # Randomly choose between addition and subtraction
        return random.choice(['+', '-'])
    
    def clear_frame(self):
        # Clear all widgets from the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()  # Remove each widget
        self.attempt_label = None  # Reset attempt label reference
    
    def get_high_score(self):
        # Placeholder for high score functionality
        return max(self.score, 100)  # Temporary implementation
    
    def start_quiz(self, difficulty):
        # Start new quiz with selected difficulty
        self.difficulty = difficulty  # Set difficulty level
        self.score = 0  # Reset score
        self.current_question = 0  # Reset question counter
        self.combo = 0  # Reset combo counter
        self.next_question()  # Start first question
    
    def next_question(self):
        # Generate and display next question or show results
        if self.current_question >= self.total_questions:
            self.displayResults()  # Show results if all questions completed
            return
        
        self.current_question += 1  # Increment question counter
        self.current_attempt = 1  # Reset attempts for new question
        
        # Generate random numbers and operation
        self.num1 = self.randomInt(self.difficulty)
        self.num2 = self.randomInt(self.difficulty)
        self.operation = self.decideOperation()
        
        # Ensure subtraction problems don't yield negative results
        if self.operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1  # Swap numbers
        
        # Calculate correct answer based on operation
        if self.operation == '+':
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2
        
        # Display the generated problem
        self.displayProblem()
    
    def displayProblem(self):
        # Display current math problem with input field
        self.clear_frame()  # Clear previous widgets
        
        # Create header frame for difficulty and score display
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=20)
        
        # Define difficulty display names and icons
        diff_names = {"easy": "Easy", "moderate": "Moderate", "advanced": "Advanced"}
        diff_icons = {"easy": "🌱", "moderate": "⚡", "advanced": "🔥"}
        
        # Create and pack difficulty label on left side
        diff_label = self.create_game_label(header_frame, 
            f"{diff_icons[self.difficulty]} {diff_names[self.difficulty]} - Question {self.current_question}/10", 
            16, True, 'primary')
        diff_label.pack(side=tk.LEFT)
        
        # Create and pack score label on right side
        score_label = self.create_game_label(header_frame, f"💰 Score: {self.score}", 16, True, 'warning')
        score_label.pack(side=tk.RIGHT)
        
        # Display combo streak if active
        if self.combo > 1:
            combo_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
            combo_frame.pack(pady=10)
            combo_label = self.create_game_label(combo_frame, f"🔥 COMBO x{self.combo}!", 18, True, 'accent')
            combo_label.pack()
        
        # Create frame for the math problem display
        question_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        question_frame.pack(pady=40)
        
        # Format and display the math problem
        question_text = f"{self.num1} {self.operation} {self.num2} = ?"
        question_label = tk.Label(question_frame, text=question_text, font=('Arial', 48, 'bold'),
            bg=self.colors['primary'], fg=self.colors['bg'], padx=50, pady=30, relief='ridge', borderwidth=6)
        question_label.pack()
        
        # Create frame for answer input
        input_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        input_frame.pack(pady=30)
        
        # Create and pack input prompt label
        input_label = self.create_game_label(input_frame, "Your Answer:", 16, False, 'text')
        input_label.pack(side=tk.LEFT, padx=20)
        
        # Create and pack answer entry field
        self.answer_entry = tk.Entry(input_frame, font=('Arial', 24, 'bold'), width=15, justify='center',
            relief='solid', borderwidth=4)
        self.answer_entry.pack(side=tk.LEFT, padx=20)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())  # Bind Enter key to submit
        self.answer_entry.focus()  # Set focus to entry field
        
        # Create and pack submit button
        submit_btn = self.create_game_button(self.main_frame, "⚔️ Submit Answer", self.check_answer, 'secondary', 20, 16)
        submit_btn.pack(pady=20)
        
        # Create and pack attempt counter label
        attempt_text = "First Attempt" if self.current_attempt == 1 else "Second Attempt"
        self.attempt_label = self.create_game_label(self.main_frame, attempt_text, 14, False, 'secondary')
        self.attempt_label.pack(pady=10)
        
        # Create and pack menu return button
        menu_btn = self.create_game_button(self.main_frame, "← Back to Menu", self.confirm_quit_to_difficulty, 'accent', 15, 12)
        menu_btn.pack(pady=10)
    
    def confirm_quit_to_difficulty(self):
        # Confirm before quitting to difficulty selection
        if messagebox.askyesno("Quit to Difficulty Selection?", "Are you sure you want to return to difficulty selection? Your current progress will be lost."):
            self.showDifficultyLevel()  # Return to difficulty selection
    
    def update_attempt_display(self):
        # Update attempt counter display
        if self.attempt_label:
            attempt_text = "First Attempt" if self.current_attempt == 1 else "Second Attempt"
            self.attempt_label.config(text=attempt_text)  # Update label text
    
    def check_answer(self):
        # Validate and check user's answer
        try:
            user_answer = int(self.answer_entry.get())  # Convert input to integer
        except ValueError:
            messagebox.showerror("Invalid Input", "🚫 Please enter a valid number!")  # Show error for invalid input
            return
        
        # Check if answer is correct
        self.isCorrect(user_answer == self.correct_answer)
    
    def isCorrect(self, correct):
        # Handle correct/incorrect answers with scoring
        if correct:
            # Calculate points based on attempt number
            points = 10 if self.current_attempt == 1 else 5
            self.score += points  # Add points to score
            self.combo += 1  # Increment combo counter
            self.max_combo = max(self.max_combo, self.combo)  # Update max combo
            
            # Show appropriate success message
            if self.current_attempt == 1:
                if self.combo > 3:
                    messagebox.showinfo("Perfect! 🎯", f"🔥 COMBO x{self.combo}! +{points} points")
                else:
                    messagebox.showinfo("Excellent! 🎉", f"Perfect! +{points} points")
            else:
                messagebox.showinfo("Good! 👍", f"Nice recovery! +{points} points")
            
            # Move to next question
            self.next_question()
        else:
            self.combo = 0  # Reset combo on incorrect answer
            
            if self.current_attempt == 1:
                # Allow second attempt
                self.current_attempt = 2
                messagebox.showerror("Wrong! ❌", "💥 Incorrect! You have one more try!")
                self.answer_entry.delete(0, tk.END)  # Clear entry field
                self.answer_entry.focus()  # Refocus on entry field
                self.update_attempt_display()  # Update attempt display
            else:
                # Show correct answer and move to next question
                messagebox.showerror("Failed! 💀", f"❌ The correct answer was {self.correct_answer}\nKeep going adventurer!")
                self.next_question()
    
    def displayResults(self):
        # Show final results with score and achievements
        self.clear_frame()  # Clear previous widgets
        
        # Create and pack results title
        title_label = self.create_game_label(self.main_frame, "🏆 QUEST COMPLETE!", 28, True, 'primary')
        title_label.pack(pady=30)
        
        # Create frame for score display
        score_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        score_frame.pack(pady=20)
        
        # Create and pack final score display
        score_text = f"Final Score: {self.score}/100"
        score_label = tk.Label(score_frame, text=score_text, font=('Arial', 24, 'bold'),
            bg=self.colors['accent'], fg=self.colors['text'], padx=30, pady=20, relief='ridge', borderwidth=6)
        score_label.pack()
        
        # Calculate and display grade
        grade = self.calculate_grade()
        grade_colors = {"A+": "#FFD700", "A": "#FFD700", "B": "#C0C0C0", "C": "#CD7F32", "D": "#8B4513", "F": "#8B0000"}
        grade_label = tk.Label(self.main_frame, text=f"Rank: {grade}", font=('Arial', 20, 'bold'),
            bg=self.colors['bg'], fg=grade_colors.get(grade.split()[0], "#FFFFFF"))
        grade_label.pack(pady=15)
        
        # Create and pack statistics display
        stats_text = f"🔥 Max Combo: x{self.max_combo}\n⚔️ Questions: {self.total_questions}\n💰 Total Points: {self.score}"
        stats_label = self.create_game_label(self.main_frame, stats_text, 16, False, 'secondary')
        stats_label.pack(pady=15)
        
        # Get and display achievement message
        achievement = self.get_achievement_message(self.score)
        achievement_label = self.create_game_label(self.main_frame, achievement, 16, True, 'warning')
        achievement_label.pack(pady=15)
        
        # Create frame for action buttons
        button_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        button_frame.pack(pady=25)
        
        # Create and pack play again button
        play_again_btn = self.create_game_button(button_frame, "🔄 Play Again", self.prompt_play_again, 'primary', 20, 14)
        play_again_btn.pack(side=tk.LEFT, padx=15)
        
        # Create and pack exit game button
        quit_btn = self.create_game_button(button_frame, "🚪 Exit Game", self.confirm_quit, 'danger', 20, 14)
        quit_btn.pack(side=tk.LEFT, padx=15)
        
        # Prompt to play again after a short delay
        self.root.after(100, self.prompt_play_again)
    
    def prompt_play_again(self):
        # Ask user if they want to play another game
        play_again = messagebox.askyesno("Play Again?", f"Your final score is {self.score}/100!\n\nWould you like to play again?")
        if play_again:
            self.displayMenu()  # Return to main menu
    
    def calculate_grade(self):
        # Calculate letter grade based on final score
        if self.score > 90: 
            return "A+ ⭐⭐⭐"
        elif self.score >= 80: 
            return "A ⭐⭐"
        elif self.score >= 70: 
            return "B ⭐"
        elif self.score >= 60: 
            return "C 🛡️"
        elif self.score >= 50: 
            return "D ⚔️"
        else: 
            return "F 💀"
    
    def get_achievement_message(self, score):
        # Generate achievement message based on performance
        if score > 90: 
            return "🎖️ LEGENDARY MATH HERO! 🎖️"
        elif score >= 80: 
            return "🏅 EPIC ADVENTURER! 🏅"
        elif score >= 70: 
            return "⭐ BRAVE WARRIOR! ⭐"
        elif score >= 60: 
            return "🛡️ NOBLE KNIGHT! 🛡️"
        elif score >= 50: 
            return "⚔️ COURAGEOUS TRAVELER! ⚔️"
        else: 
            return "💪 KEEP PRACTICING, YOUNG APPRENTICE! 💪"
    
    def confirm_quit(self):
        # Confirm before exiting the game
        if messagebox.askyesno("Exit Game?", "Are you sure you want to exit the Math Quest Adventure?"):
            self.root.quit()  # Close the application

def main():
    # Initialize and run the game application
    root = tk.Tk()  # Create main Tkinter window
    app = MathsQuizGame(root)  # Create game instance
    root.mainloop()  # Start the GUI event loop

if __name__ == "__main__":
    main()  