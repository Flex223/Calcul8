import customtkinter as ctk
import random
from ctypes import windll
from PIL import Image
from tkinter import StringVar

def init(root):
    global entry, divide_icon, plus_icon, neg_icon, multiply_icon
    root.title("Calcul8")
    root.geometry("400x300")  # Set default resolution to 400x300
    root.update_idletasks()  # Update "requested size" from geometry manager
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")  # Center the window on the screen
    root.configure(bg='#EDEDED')

    divide_icon = ctk.CTkImage(Image.open("pics/divide.png"), size=(40, 40))
    plus_icon = ctk.CTkImage(Image.open("pics/plus.png"), size=(40, 40))
    neg_icon = ctk.CTkImage(Image.open("pics/neg.png"), size=(40, 40))
    multiply_icon = ctk.CTkImage(Image.open("pics/multiply.png"), size=(40, 40))

    #windll.shcore.SetProcessDpiAwareness(1)

    # Create a label
    label = ctk.CTkLabel(root, text="Calcul8", font=("Arial", 24), text_color='#212121')
    label.pack(pady=10)

    card = ctk.CTkFrame(root, fg_color="#ffffff", corner_radius=10)
    card.pack(pady=10)

    label = ctk.CTkLabel(card, text="Enter your name", font=("Arial", 20), text_color='#212121')
    label.pack(pady=10, padx=50)

    # Create an entry widget
    entry = ctk.CTkEntry(card, fg_color='#BDBDBD', border_color='#212121', text_color='black')
    entry.pack(pady=10)

    # Create a button
    button = ctk.CTkButton(card, text="Submit", command=name_selected, fg_color='#03A9F4', hover_color='#FFC107')
    button.pack(pady=10)

def name_selected():
    global entry, name
    name = entry.get()
    if name:
        show_operations()
    else:
        entry.configure(border_color="red", border_width=2)

def show_operations():
    global name, selected_operator, divide_icon, plus_icon, neg_icon, multiply_icon
    selected_operator = None  # Initialize the selected operator
    # Clear the first screen widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("400x300")
    
    # Create a frame to center the buttons
    button_frame = ctk.CTkFrame(root,  fg_color='white')
    button_frame.pack(expand=True)

    # Create buttons for operations
    operations = ['+', '-', '*', '/']
    l = (lambda o: divide_icon if o == '/' else plus_icon if o == "+" else neg_icon if o =="-" else multiply_icon)
    for i, op in enumerate(operations):
        button = ctk.CTkButton(button_frame,image=l(op) ,text="", font=("Arial", 24), width=60, height=60, command=lambda op=op: select_operator(op), fg_color='#03A9F4', hover_color='#FFC107')
        button.grid(row=i // 2, column=i % 2, padx=20, pady=20)

def select_operator(op):
    global selected_operator
    selected_operator = op
    show_difficulty()

def show_difficulty():
    # Clear the second screen widgets
    for widget in root.winfo_children():
        widget.destroy()


    # Create a frame to center the buttons
    button_frame = ctk.CTkFrame(root, fg_color="white")
    button_frame.pack(expand=True)

    # Create buttons for difficulty levels with rounded corners
    difficulties = ['0', '00', '000']
    for i, diff in enumerate(difficulties):
        button = ctk.CTkButton(button_frame, text=diff, fg_color='#03A9F4', hover_color='#FFC107', font=("Arial", 24), corner_radius=10, width=50, height=50, command=lambda diff=diff: select_difficulty(diff))
        button.grid(row=0, column=i, padx=15, pady=20)

def select_difficulty(diff):
    global selected_difficulty
    selected_difficulty = diff
    show_exercise()

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

def show_exercise():
    global exercises, selected_operator, selected_difficulty, answer_entries, check_button, show_button, button_frame
    # Clear the previous screen widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    create_exercise(selected_operator, (lambda s: 1 if s == '0' else 10 if s == '00' else 100)(selected_difficulty), (lambda s: 9 if s == '0' else 99 if s == '00' else 999)(selected_difficulty))
    root.geometry("600x300")

    # Create a frame to center the exercises
    exercise_frame = ctk.CTkFrame(root, fg_color='white')
    exercise_frame.pack(expand=True)

    answer_entries = []
    
    # Display exercises with entry widgets in a 2x3 grid
    for i, (a, b) in enumerate(exercises):
        exercise_label = ctk.CTkLabel(exercise_frame, text=f"{a} {selected_operator} {b} =", font=("Arial", 18), text_color='#212121')
        exercise_label.grid(row=i // 2, column=(i % 2) * 2, padx=10, pady=10)
        
        sv = StringVar()
        sv.trace_add("write", lambda name, index, mode, sv=sv: answer_entry_event(sv))
        
        answer_entry = ctk.CTkEntry(exercise_frame, textvariable=sv, font=("Arial", 18), text_color='#0288D1', fg_color='#BDBDBD', border_color='#212121')
        answer_entry.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=10, pady=10)
        answer_entries.append(answer_entry)

    # Create a frame to center the buttons horizontally
    button_frame = ctk.CTkFrame(exercise_frame, fg_color='white')
    button_frame.grid(row=3, column=0, columnspan=4)
    
    # Add Check Answers and Show Answers buttons to the grid
    check_button = ctk.CTkButton(button_frame, text="Check Answers", font=("Arial", 18), command=check_answers, fg_color='#03A9F4', hover_color='#FFC107')
    check_button.grid(row=3, column=0, padx=10, pady=10)
    
    show_button = ctk.CTkButton(button_frame, text="Show Answers", font=("Arial", 18), command=show_answers, fg_color='#03A9F4', hover_color='#FFC107')
    show_button.grid(row=3, column=1, padx=10, pady=10)

def answer_entry_event(sv):
    for entry in answer_entries:
        if entry.get() == sv.get():
            entry.configure(text_color='#0288D1', border_color='#212121')


def check_answers():
    global answers, answer_entries
    correct = 0
    for i, entry in enumerate(answer_entries):
        try:
            if float(entry.get()) == answers[i]:
                entry.configure(border_color="green", text_color="green", border_width=2)
                correct += 1
            else:
                entry.configure(border_color="red", text_color="red", border_width=2)
        except ValueError:
            entry.configure(border_color="red", border_width=2)

def show_answers():
    global answers, answer_entries, check_button, show_button, button_frame
    for i, entry in enumerate(answer_entries):
        entry.delete(0, ctk.END)
        entry.insert(0, str(int(answers[i])))
        entry.configure(state='readonly')
    
    # Destroy Check Answers and Show Answers buttons
    check_button.destroy()
    show_button.destroy()
    
    # Add Back button
    back_button = ctk.CTkButton(button_frame, text="Back", font=("Arial", 18), command=show_operations, fg_color='#03A9F4', hover_color='#FFC107')
    back_button.pack(pady=10, padx=10)

# Create the main window
root = ctk.CTk(fg_color='#B3E5FC')
init(root)

# Run the application
root.mainloop()