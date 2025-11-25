import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Get the base directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_img(name, size):
    """Load and resize an image from the base directory"""
    path = os.path.join(BASE_DIR, name)
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))

# Original student data that will be written to the file on reset
ORIGINAL_DATA = """10
1345,John Curry,8,15,7,45
2345,Sam Sturtivant,14,15,14,77
9876,Lee Scott,17,11,16,99
3724,Matt Thompson,19,11,15,81
1212,Ron Herrema,14,17,18,66
8439,Jake Hobbs,10,11,10,43
2344,Jo Hyde,6,15,10,55
9384,Gareth Southgate,5,6,8,33
8327,Alan Shearer,20,20,20,100
2983,Les Ferdinand,15,17,18,92
"""

def reset_data_file():
    """Reset the student data file to its original state"""
    path = os.path.join(BASE_DIR, "studentMarks.txt")
    with open(path, "w") as f:
        f.write(ORIGINAL_DATA)

def calculate_grade(percent):
    """Calculate letter grade based on percentage score"""
    if percent >= 70: return "A"
    elif percent >= 60: return "B"
    elif percent >= 50: return "C"
    elif percent >= 40: return "D"
    return "F"

class StudentApp(tk.Tk):
    """Main application class for Student Management System"""
    
    def __init__(self):
        super().__init__()
        # Reset data file to ensure we start with clean data
        reset_data_file()
        
        # Configure main window
        self.title("Student Manager")
        self.geometry("900x600")
        self.resizable(False, False)

        # Window Icon
        icon_path = os.path.join(BASE_DIR, "Student Manager.ico")
        self.iconbitmap(icon_path)
        
        # Initialize instance variables
        self.selected_student_id = None  # Currently selected student ID
        self.selected_label = None       # Reference to selected student label
        self.highest_name_label = None   # Label for highest/lowest student display
        
        # Load background images for different screens
        self.bg1 = load_img("1.png", (900, 600))  # Main menu
        self.bg2 = load_img("2.png", (900, 600))  # View all students
        self.bg3 = load_img("3.png", (900, 600))  # Add student
        self.bg4 = load_img("4.png", (900, 600))  # Update student
        self.bg5 = load_img("5.png", (900, 600))  # Highest scoring student
        self.bg6 = load_img("6.png", (900, 600))  # Lowest scoring student
        
        # Create background label
        self.bg_label = tk.Label(self, image=self.bg1)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create header for student list display
        header = f"{'ID':<6}{'NAME':<16}{'COURSEWORK':<13}{'EXAM':<9}{'%':<6}{'GRADE':<4}"
        self.header_text = tk.Label(self, text=header, font=("Courier New", 12, "bold"),
                                  fg="white", bg="#213159", anchor="w")
        
        # Initialize lists to track UI elements
        self.data_labels = []     # Labels for student data rows
        self.summary_label = None # Label for summary statistics
        self.add_widgets = []     # Widgets for add/update forms
        
        # Create the main navigation buttons
        self.create_buttons()

    def _vc_id(self, proposed):
        """Validation function for Student ID field"""
        if proposed == "": return True  # Allow empty field during typing
        return proposed.isdigit() and len(proposed) <= 4  # Must be digits and max 4 chars

    def _vc_cw(self, proposed):
        """Validation function for Coursework marks (0-20)"""
        if proposed == "": return True  # Allow empty field during typing
        if not proposed.isdigit(): return False  # Must be numeric
        if len(proposed) > 2: return False  # Max 2 digits
        try: 
            return 0 <= int(proposed) <= 20  # Must be between 0-20
        except: 
            return False

    def _vc_exam(self, proposed):
        """Validation function for Exam marks (0-100)"""
        if proposed == "": return True  # Allow empty field during typing
        if not proposed.isdigit(): return False  # Must be numeric
        if len(proposed) > 3: return False  # Max 3 digits
        try: 
            return 0 <= int(proposed) <= 100  # Must be between 0-100
        except: 
            return False

    def read_student_file(self):
        """Read and parse student data from file"""
        path = os.path.join(BASE_DIR, "studentMarks.txt")
        students = []
        try:
            with open(path, "r") as f:
                lines = f.readlines()
            if not lines: return students  # Return empty list if file is empty
            
            # Skip first line if it's just a count
            first_line = lines[0].strip()
            if first_line.isdigit(): lines = lines[1:]
            
            # Parse each student record
            for line in lines:
                line = line.strip()
                if not line: continue  # Skip empty lines
                parts = line.split(",")
                if len(parts) >= 6:
                    # Ensure we have exactly 6 fields per student
                    while len(parts) < 6: parts.append("0")
                    students.append(parts[:6])
        except FileNotFoundError:
            messagebox.showerror("Error", "studentMarks.txt file not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {str(e)}")
        return students

    def write_student_file(self, students):
        """Write student data back to file"""
        path = os.path.join(BASE_DIR, "studentMarks.txt")
        try:
            with open(path, "w") as f:
                f.write(str(len(students)) + "\n")  # Write count on first line
                for student in students:
                    f.write(",".join(student) + "\n")  # Write each student record
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")
            return False

    def create_buttons(self):
        """Create the main navigation buttons"""
        btn_style = {
            "font": ("Arial", 13), "bg": "#213159", "fg": "white",
            "relief": "flat", "borderwidth": 0, "highlightthickness": 0,
            "activebackground": "#213159", "activeforeground": "white"
        }
        
        # Create all navigation buttons with their commands and positions
        tk.Button(self, text="View All Students", command=self.show_all_students, **btn_style).place(x=50, y=158, width=170, height=45)
        tk.Button(self, text="Add Student Record", command=lambda: self.switch(self.bg3), **btn_style).place(x=49, y=225, width=170, height=45)
        tk.Button(self, text="Update Student", command=self.open_update_page, **btn_style).place(x=50, y=293, width=170, height=45)
        tk.Button(self, text="Highest Scoring Student", command=self.show_highest_student, **btn_style).place(x=36, y=360, width=190, height=45)
        tk.Button(self, text="Lowest Scoring Student", command=self.show_lowest_student, **btn_style).place(x=36, y=428, width=190, height=45)
        
        # Quit button with different styling
        tk.Button(self, text="Quit", command=self.quit, font=("Arial", 13), bg="#cc0000", fg="white",
                relief="flat", borderwidth=0, highlightthickness=0,
                activebackground="#cc0000", activeforeground="white").place(x=77, y=519, width=110, height=42)

    def open_sort_dropdown(self):
        """Open the sorting options dropdown menu"""
        # Toggle dropdown visibility
        if hasattr(self, "sort_dropdown") and self.sort_dropdown.winfo_exists():
            self.sort_dropdown.destroy()
            return

        # Position dropdown below the sort button
        btn_x, btn_y = self.sort_btn.winfo_x(), self.sort_btn.winfo_y()
        btn_h = self.sort_btn.winfo_height()
        self.sort_dropdown = tk.Frame(self, bg="#1c4a7f", relief="flat", borderwidth=0)
        self.sort_dropdown.place(x=btn_x, y=btn_y + btn_h, width=120)

        # Style for dropdown options
        opt = {
            "font": ("Arial", 12), "bg": "#1c4a7f", "fg": "white",
            "relief": "flat", "borderwidth": 0, "activebackground": "#163b66",
            "activeforeground": "white", "anchor": "w"
        }

        # Create sort option buttons
        tk.Button(self.sort_dropdown, text="Sort Name (A-Z)", command=lambda: self.sort_students("name_asc"), **opt).pack(fill="x")
        tk.Button(self.sort_dropdown, text="Sort Name (Z-A)", command=lambda: self.sort_students("name_desc"), **opt).pack(fill="x")

    def sort_students(self, sort_type):
        """Sort students by specified criteria and refresh display"""
        rows = self.read_student_file()
        if sort_type == "name_asc":
            rows.sort(key=lambda x: x[1].lower())  # Sort A-Z by name
        elif sort_type == "name_desc":
            rows.sort(key=lambda x: x[1].lower(), reverse=True)  # Sort Z-A by name
        
        # Save sorted data and refresh display
        if self.write_student_file(rows):
            try: 
                self.sort_dropdown.destroy()  # Close dropdown
            except: 
                pass
            self.show_all_students()  # Refresh the view

    def show_all_students(self):
        """Display the 'View All Students' screen"""
        self.switch(self.bg2)  # Switch to appropriate background
        self.header_text.place(x=315, y=230)  # Position header
        self.selected_student_id = None  # Reset selection
        self.selected_label = None

        # Clear existing data labels
        for lbl in self.data_labels: 
            lbl.destroy()
        self.data_labels.clear()
        if self.summary_label: 
            self.summary_label.destroy()

        # Create search entry field
        self.search_entry = tk.Entry(self, font=("Arial", 16), width=16, relief="flat", borderwidth=0)
        self.search_entry.place(x=371, y=155, height=30)
        self.search_entry.bind("<Return>", self.search_student)  # Search on Enter key

        # Create delete button for selected student
        self.delete_btn = tk.Button(self, text="Delete", font=("Arial", 12), bg="#cc0000", fg="white",
                                  relief="flat", borderwidth=0, activebackground="#cc0000",
                                  activeforeground="white", command=self.delete_selected_student)
        self.delete_btn.place(x=630, y=156, width=60, height=32)

        # Create sort button
        self.sort_btn = tk.Button(self, text="Sort Students", font=("Arial", 12), bg="#051d40", fg="white",
                                relief="flat", borderwidth=0, activebackground="#051d40",
                                activeforeground="white", command=self.open_sort_dropdown)
        self.sort_btn.place(x=720, y=155, width=120, height=32)

        # Display all students
        self.display_all_students()

    def display_all_students(self):
        """Display all student records in a formatted list"""
        rows = self.read_student_file()
        y_offset, percentages = 275, []  # Starting Y position and list for calculating average

        # Process and display each student
        for row in rows:
            sid, name, cw1, cw2, cw3, exam = row[0], row[1], *map(int, row[2:6])
            coursework = cw1 + cw2 + cw3  # Calculate total coursework
            percent = round(((coursework + exam) / 160) * 100, 2)  # Calculate percentage
            percentages.append(percent)  # Store for average calculation
            grade = calculate_grade(percent)  # Get letter grade

            # Format the student data line
            line = f"{sid:<6}{name:<20}{coursework:<10}{exam:<7}{percent:<9}{grade:<4}"
            lbl = tk.Label(self, text=line, font=("Courier New", 12), fg="white", bg="#051d40", anchor="w")
            # Make label clickable for selection
            lbl.bind("<Button-1>", lambda e, sid=sid, lbl=lbl: self.select_student(sid, lbl))
            lbl.place(x=315, y=y_offset)
            self.data_labels.append(lbl)
            y_offset += 22  # Move down for next student

        # Calculate and display summary statistics
        avg_percent = round(sum(percentages) / len(rows), 2) if rows else 0
        self.summary_label = tk.Label(self, text=f"Total Students: {len(rows)}        Average Percentage: {avg_percent}%",
                                    font=("Courier New", 12, "bold"), fg="white", bg="#051d40", anchor="w")
        self.summary_label.place(x=315, y=y_offset + 20)

    def select_student(self, sid, lbl):
        """Handle student selection by clicking on their row"""
        self.selected_student_id = sid
        # Update visual selection
        if self.selected_label: 
            self.selected_label.config(bg="#051d40")  # Deselect previous
        lbl.config(bg="#1c4a7f")  # Highlight selected
        self.selected_label = lbl  # Store reference

    def delete_selected_student(self):
        """Delete the currently selected student"""
        if not self.selected_student_id:
            messagebox.showerror("Error", "No student selected.")
            return

        rows = self.read_student_file()
        # Filter out the selected student
        new_rows = [r for r in rows if r[0] != self.selected_student_id]

        # Check if student was actually found and removed
        if len(new_rows) == len(rows):
            messagebox.showerror("Error", "Student not found.")
            return

        # Save updated data and refresh display
        if self.write_student_file(new_rows):
            self.show_all_students()

    def search_student(self, event):
        """Search for a student by ID and display results"""
        search_id = self.search_entry.get().strip()
        # Clear existing display
        for lbl in self.data_labels: 
            lbl.destroy()
        self.data_labels.clear()
        if self.summary_label: 
            self.summary_label.destroy()

        rows = self.read_student_file()
        found = None
        # Search for student with matching ID
        for row in rows:
            if row[0] == search_id:
                found = row
                break

        if not found:
            # Display not found message
            lbl = tk.Label(self, text="Student not found", font=("Courier New", 14), fg="white", bg="#051d40")
            lbl.place(x=315, y=275)
            self.data_labels.append(lbl)
            return

        # Display found student
        sid, name, cw1, cw2, cw3, exam = found[0], found[1], *map(int, found[2:6])
        coursework = cw1 + cw2 + cw3
        percent = round(((coursework + exam) / 160) * 100, 2)
        grade = calculate_grade(percent)

        result = f"{sid:<6}{name:<20}{coursework:<10}{exam:<7}{percent:<9}{grade:<5}"
        lbl = tk.Label(self, text=result, font=("Courier New", 12), fg="white", bg="#051d40", anchor="w")
        lbl.place(x=315, y=275)
        self.data_labels.append(lbl)

    def switch(self, bg_image):
        """Switch between different screens/backgrounds"""
        self.bg_label.config(image=bg_image)
        self.bg_label.image = bg_image
        self.header_text.place_forget()  # Hide header

        # Clear various UI elements
        if self.highest_name_label: 
            self.highest_name_label.destroy()
        for lbl in self.data_labels: 
            lbl.destroy()
        self.data_labels.clear()
        if self.summary_label: 
            self.summary_label.destroy()
        for w in self.add_widgets: 
            w.destroy()
        self.add_widgets = []

        # Clean up specific widgets that might exist
        try: 
            self.search_entry.destroy()
        except: 
            pass
        try: 
            self.delete_btn.destroy()
        except: 
            pass
        try: 
            self.sort_btn.destroy()
        except: 
            pass
        try: 
            self.sort_dropdown.destroy()
        except: 
            pass

        # If switching to add student screen, create the form
        if bg_image == self.bg3: 
            self.add_student_form()

    def add_student_form(self):
        """Create the form for adding new students"""
        # Define form fields and their positions
        fields = [("ID", 550, 162), ("NAME", 550, 220), ("CW1", 550, 275), 
                 ("CW2", 550, 332), ("CW3", 550, 389), ("EXAM", 550, 445)]
        
        self.add_entries = {}  # Dictionary to store entry widgets
        # Register validation commands
        vcmd_id = (self.register(self._vc_id), '%P')
        vcmd_cw = (self.register(self._vc_cw), '%P')
        vcmd_exam = (self.register(self._vc_exam), '%P')

        # Create each form field
        for name, x, y in fields:
            e = tk.Entry(self, font=("Arial", 18), relief="flat", borderwidth=0)
            # Apply appropriate validation based on field type
            if name == "ID": 
                e.config(validate="key", validatecommand=vcmd_id)
            elif name in ("CW1", "CW2", "CW3"): 
                e.config(validate="key", validatecommand=vcmd_cw)
            elif name == "EXAM": 
                e.config(validate="key", validatecommand=vcmd_exam)
            e.place(x=x, y=y, width=295, height=35)
            self.add_widgets.append(e)
            self.add_entries[name] = e

        # Create add button
        add_btn = tk.Button(self, text="Add", font=("Arial", 14), bg="#f6c03e", fg="#051d40",
                          relief="flat", borderwidth=0, highlightthickness=0,
                          activebackground="#f6c03e", activeforeground="#051d40",
                          command=self.save_new_student)
        add_btn.place(x=650, y=520, width=80, height=40)
        self.add_widgets.append(add_btn)

    def save_new_student(self):
        """Save a new student record from the add form"""
        # Get data from form fields
        sid = self.add_entries["ID"].get().strip()
        name = self.add_entries["NAME"].get().strip()
        cw1 = self.add_entries["CW1"].get().strip()
        cw2 = self.add_entries["CW2"].get().strip()
        cw3 = self.add_entries["CW3"].get().strip()
        exam = self.add_entries["EXAM"].get().strip()

        # Validate that all fields are filled
        if not all([sid, name, cw1, cw2, cw3, exam]):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        # Validate Student ID format
        if not (sid.isdigit() and len(sid) == 4):
            messagebox.showerror("Error", "Student ID must be exactly 4 digits.")
            return

        # Validate and convert marks to integers
        try:
            cw1_i, cw2_i, cw3_i = int(cw1), int(cw2), int(cw3)
            exam_i = int(exam)
            # Validate coursework marks range
            if not all(0 <= x <= 20 for x in [cw1_i, cw2_i, cw3_i]):
                messagebox.showerror("Error", "Coursework marks must be between 0 and 20.")
                return
            # Validate exam mark range
            if not 0 <= exam_i <= 100:
                messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                return
        except:
            messagebox.showerror("Error", "Marks must be numeric.")
            return

        # Check for duplicate Student ID
        rows = self.read_student_file()
        for r in rows:
            if r[0] == sid:
                messagebox.showerror("Error", "Student ID already exists.")
                return

        # Add new student and save
        rows.append([sid, name, str(cw1_i), str(cw2_i), str(cw3_i), str(exam_i)])
        if self.write_student_file(rows):
            self.show_all_students()  # Switch to view all students

    def open_update_page(self):
        """Open the update student form"""
        self.switch(self.bg4)
        self.update_student_form()

    def update_student_form(self):
        """Create the form for updating an existing student"""
        rows = self.read_student_file()
        selected = None
        # Find the currently selected student
        for r in rows:
            if r[0] == self.selected_student_id:
                selected = r
                break

        # Get current values or empty strings if no student selected
        if selected: 
            sid, name, cw1, cw2, cw3, exam = selected
        else: 
            sid = name = cw1 = cw2 = cw3 = exam = ""

        # Define form fields with current values
        fields = [("ID", 550, 162, sid), ("NAME", 550, 220, name), 
                 ("CW1", 550, 275, cw1), ("CW2", 550, 332, cw2),
                 ("CW3", 550, 389, cw3), ("EXAM", 550, 445, exam)]
        
        self.update_entries = {}  # Dictionary to store entry widgets
        # Register validation commands
        vcmd_id = (self.register(self._vc_id), '%P')
        vcmd_cw = (self.register(self._vc_cw), '%P')
        vcmd_exam = (self.register(self._vc_exam), '%P')

        # Create each form field with current values
        for name, x, y, value in fields:
            e = tk.Entry(self, font=("Arial", 18), relief="flat", borderwidth=0)
            e.insert(0, value)  # Pre-populate with current value
            # Apply appropriate validation
            if name == "ID": 
                e.config(validate="key", validatecommand=vcmd_id)
            elif name in ("CW1", "CW2", "CW3"): 
                e.config(validate="key", validatecommand=vcmd_cw)
            elif name == "EXAM": 
                e.config(validate="key", validatecommand=vcmd_exam)
            e.place(x=x, y=y, width=295, height=35)
            self.add_widgets.append(e)
            self.update_entries[name] = e

        # Create update button
        update_btn = tk.Button(self, text="Update", font=("Arial", 14), bg="#f6c03e", fg="#051d40",
                             relief="flat", borderwidth=0, highlightthickness=0,
                             activebackground="#f6c03e", activeforeground="#051d40",
                             command=self.save_updated_student)
        update_btn.place(x=650, y=520, width=80, height=40)
        self.add_widgets.append(update_btn)

    def save_updated_student(self):
        """Save updated student information"""
        # Get data from form fields
        sid = self.update_entries["ID"].get().strip()
        name = self.update_entries["NAME"].get().strip()
        cw1 = self.update_entries["CW1"].get().strip()
        cw2 = self.update_entries["CW2"].get().strip()
        cw3 = self.update_entries["CW3"].get().strip()
        exam = self.update_entries["EXAM"].get().strip()

        # Validate that all fields are filled
        if not all([sid, name, cw1, cw2, cw3, exam]):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        # Validate Student ID format
        if not (sid.isdigit() and len(sid) == 4):
            messagebox.showerror("Error", "Student ID must be exactly 4 digits.")
            return

        # Validate and convert marks to integers
        try:
            cw1_i, cw2_i, cw3_i = int(cw1), int(cw2), int(cw3)
            exam_i = int(exam)
            # Validate coursework marks range
            if not all(0 <= x <= 20 for x in [cw1_i, cw2_i, cw3_i]):
                messagebox.showerror("Error", "Coursework marks must be between 0 and 20.")
                return
            # Validate exam mark range
            if not 0 <= exam_i <= 100:
                messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                return
        except:
            messagebox.showerror("Error", "Marks must be numeric.")
            return

        # Check if new ID conflicts with existing students (excluding current student)
        rows = self.read_student_file()
        for r in rows:
            if r[0] == sid and r[0] != self.selected_student_id:
                messagebox.showerror("Error", "Another student already has that ID.")
                return

        # Update student data
        new_rows = []
        for r in rows:
            if r[0] == self.selected_student_id:
                # Replace with updated data
                new_rows.append([sid, name, str(cw1_i), str(cw2_i), str(cw3_i), str(exam_i)])
            else: 
                new_rows.append(r)  # Keep existing student

        # Save updated data and refresh display
        if self.write_student_file(new_rows):
            self.show_all_students()

    def show_highest_student(self):
        """Display the highest scoring student"""
        self.switch(self.bg5)
        self.after(50, self._draw_highest_student)  # Small delay to ensure UI is ready

    def _draw_highest_student(self):
        """Draw the highest scoring student details"""
        # Clear existing display
        for lbl in self.data_labels: 
            lbl.destroy()
        self.data_labels.clear()
        if self.summary_label: 
            self.summary_label.destroy()

        rows = self.read_student_file()
        if not rows: 
            return  # No students to display

        # Process student data and calculate percentages
        processed = []
        for row in rows:
            try:
                sid, name, cw1, cw2, cw3, exam = row[0], row[1], *map(int, row[2:6])
                coursework = cw1 + cw2 + cw3
                percent = round(((coursework + exam) / 160) * 100, 2)
                grade = calculate_grade(percent)
                processed.append((sid, name, coursework, exam, percent, grade))
            except: 
                continue  # Skip invalid records

        # Find student with highest percentage
        highest = max(processed, key=lambda x: x[4])
        if self.highest_name_label: 
            self.highest_name_label.destroy()

        # Display student name prominently
        self.highest_name_label = tk.Label(self, text=highest[1], font=("Arial", 25, "bold"),
                                         fg="#051d40", bg="#f6c03e")
        self.highest_name_label.place(x=350, y=160)

        # Display header and student details
        header = f"{'ID':<6}{'NAME':<16}{'COURSEWORK':<13}{'EXAM':<9}{'%':<6}{'GRADE':<4}"
        self.header_text.config(text=header)
        self.header_text.place(x=315, y=249)

        line = f"{highest[0]:<6}{highest[1]:<20}{highest[2]:<10}{highest[3]:<7}{highest[4]:<9}{highest[5]:<4}"
        lbl = tk.Label(self, text=line, font=("Courier New", 12), fg="white", bg="#051d40", anchor="w")
        lbl.place(x=315, y=290)
        self.data_labels.append(lbl)

    def show_lowest_student(self):
        """Display the lowest scoring student"""
        self.switch(self.bg6)
        self.after(50, self._draw_lowest_student)  # Small delay to ensure UI is ready

    def _draw_lowest_student(self):
        """Draw the lowest scoring student details"""
        # Clear existing display
        for lbl in self.data_labels: 
            lbl.destroy()
        self.data_labels.clear()
        if self.summary_label: 
            self.summary_label.destroy()

        rows = self.read_student_file()
        if not rows: 
            return  # No students to display

        # Process student data and calculate percentages
        processed = []
        for row in rows:
            try:
                sid, name, cw1, cw2, cw3, exam = row[0], row[1], *map(int, row[2:6])
                coursework = cw1 + cw2 + cw3
                percent = round(((coursework + exam) / 160) * 100, 2)
                grade = calculate_grade(percent)
                processed.append((sid, name, coursework, exam, percent, grade))
            except: 
                continue  # Skip invalid records

        # Find student with lowest percentage
        lowest = min(processed, key=lambda x: x[4])
        if self.highest_name_label: 
            self.highest_name_label.destroy()

        # Display student name prominently
        self.highest_name_label = tk.Label(self, text=lowest[1], font=("Arial", 25, "bold"),
                                         fg="#051d40", bg="#f6c03e")
        self.highest_name_label.place(x=350, y=160)

        # Display header and student details
        header = f"{'ID':<6}{'NAME':<16}{'COURSEWORK':<13}{'EXAM':<9}{'%':<6}{'GRADE':<4}"
        self.header_text.config(text=header)
        self.header_text.place(x=315, y=249)

        line = f"{lowest[0]:<6}{lowest[1]:<20}{lowest[2]:<10}{lowest[3]:<7}{lowest[4]:<9}{lowest[5]:<4}"
        lbl = tk.Label(self, text=line, font=("Courier New", 12), fg="white", bg="#051d40", anchor="w")
        lbl.place(x=315, y=290)
        self.data_labels.append(lbl)

if __name__ == "__main__":
    # Create and run the application
    app = StudentApp()
    app.mainloop()