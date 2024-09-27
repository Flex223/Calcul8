import tkinter as tk
from tkinter import messagebox
import random
from ctypes import windll

def init(root):
    global entry
    root = root
    root.title("Calcul8")
    root.geometry("400x450")  # Set default resolution to 800x600
    root.configure(bg='#EDEDED')

    # Create a label
    label = tk.Label(root, text="Enter your name:")
    label.pack(pady=10)

    # Create an entry widget
    entry = tk.Entry(root)
    entry.pack(pady=10)

    # Create a button
    button = tk.Button(root, text="Submit", command=name_selected)
    button.pack(pady=10)

def name_selected():
    global entry, name
    name = entry.get()
    if name:
        show_operations()
    else:
        messagebox.showwarning("Input Error", "Please enter your name.")

def show_operations():
        global name, selected_operator
        selected_operator = None  # Initialize the selected operator
        # Clear the first screen widgets
        for widget in root.winfo_children():
            widget.destroy()

        # Display the player's name
        name_label = tk.Label(root, text=f"Player: {name}", font=("Arial", 18))
        name_label.pack(pady=10)

        # Create a frame to center the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(expand=True)

        # Create buttons for operations
        operations = ['+', '-', '*', '/']
        for i, op in enumerate(operations):
            button = tk.Button(button_frame, text=op, font=("Arial", 24), width=5, height=2, command=lambda op=op: select_operator(op))
            button.grid(row=i // 2, column=i % 2, padx=20, pady=20)

def select_operator(op):
    global selected_operator
    selected_operator = op
    show_difficulty()

def select_difficulty(diff):
    global selected_difficulty
    selected_difficulty = diff
    show_exercise()

def show_difficulty():
    # Clear the second screen widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Display the player's name and selected operator
    info_label = tk.Label(root, text=f"Player: {name}, Operator: {selected_operator}", font=("Arial", 18))
    info_label.pack(pady=10)

    # Create a frame to center the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(expand=True)

    # Create buttons for difficulty levels
    difficulties = ['0', '00', '000']
    for i, diff in enumerate(difficulties):
        button = tk.Button(button_frame, text=diff, font=("Arial", 24), width=5, height=2, command=lambda diff=diff: select_difficulty(diff))
        button.grid(row=0, column=i, padx=20, pady=20)

def show_exercise():
    global exercises, selected_operator, selected_difficulty, answer_entries, check_button, show_button, button_frame
    # Clear the previous screen widgets
    for widget in root.winfo_children():
        widget.destroy()

    create_exercise(selected_operator, (lambda s: 1 if s == '0' else 10 if s == '00' else 100)(selected_difficulty), (lambda s: 9 if s == '0' else 99 if s == '00' else 999)(selected_difficulty))
    root.geometry("1000x600")
    # Display the player's name and selected operator
    info_label = tk.Label(root, text=f"Player: {name}, Operator: {selected_operator}, Difficulty: {selected_difficulty}", font=("Arial", 18))
    info_label.pack(pady=10)

    # Create a frame to center the exercises
    exercise_frame = tk.Frame(root)
    exercise_frame.pack(expand=True)

    answer_entries = []

    # Display exercises with entry widgets in a 2x3 grid
    for i, (a, b) in enumerate(exercises):
        exercise_label = tk.Label(exercise_frame, text=f"{a} {selected_operator} {b} =", font=("Arial", 18))
        exercise_label.grid(row=i // 2, column=(i % 2) * 2, padx=10, pady=10)
        answer_entry = tk.Entry(exercise_frame, font=("Arial", 18))
        answer_entry.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=10, pady=10)
        answer_entries.append(answer_entry)


    # Create a frame to center the buttons horizontally
    button_frame = tk.Frame(exercise_frame)
    button_frame.grid(row=3, column=0, columnspan=4)
    # Add Check Answers and Show Answers buttons to the grid
    check_button = tk.Button(button_frame, text="Check Answers", font=("Arial", 18), command=check_answers)
    check_button.grid(row=3, column=0, padx=10, pady=10)
    show_button = tk.Button(button_frame, text="Show Answers", font=("Arial", 18), command=show_answers)
    show_button.grid(row=3, column=1, padx=10, pady=10)

def check_answers():
    global answers, answer_entries
    correct = 0
    for i, entry in enumerate(answer_entries):
        try:
            if float(entry.get()) == answers[i]:
                entry.config(highlightbackground='green', highlightcolor='green', highlightthickness=2)
                correct += 1
            else:
                entry.config(highlightbackground='red', highlightcolor='red', highlightthickness=2)
        except ValueError:
            entry.config(highlightbackground='red', highlightcolor='red', highlightthickness=2)

def show_answers():
    global answers, answer_entries, check_button, show_button, button_frame
    for i, entry in enumerate(answer_entries):
        entry.delete(0, tk.END)
        entry.insert(0, str(answers[i]))
    
    # Destroy Check Answers and Show Answers buttons
    check_button.destroy()
    show_button.destroy()
    
    # Add Back button
    back_button = tk.Button(button_frame, text="Back", font=("Arial", 18), command=show_operations)
    back_button.pack(pady=10)



def create_exercise(operator, min, max):
    global exercises, answers
    exercises = []
    answers = []
    szamlalo = 0

    while szamlalo <=5: 
        a = random.randint(min, max)
        b = random.randint((lambda s: 2 if s == '/' else min)(operator), (lambda s: 9 if s == '/' else max)(operator))
    
        if operator == '/' and a % b == 0 and b != 0 and a  != b:
            answers.append(a / b)
            exercises.append((a,b))
            szamlalo += 1
         
        if operator == '*':
            answers.append(a * b)
            exercises.append((a,b))
            szamlalo += 1 
        
        if operator == '+':
            answers.append(a + b)
            exercises.append((a,b))
            szamlalo += 1

        if operator == '-':
            answers.append(a - b)
            exercises.append((a,b))
            szamlalo += 1 


# Create the main window
root = tk.Tk()
root.title("Calcul8")
root.geometry("800x600")  # Set default resolution to 800x600
root.configure(bg='#EDEDED')

# Set the DPI awareness for the application (Windows specific)
windll.shcore.SetProcessDpiAwareness(1)

# Initialize the first screen
init(root)

# Run the application
root.mainloop()