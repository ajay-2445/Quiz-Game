import tkinter as tk
from tkinter import filedialog, messagebox
import json
import random


def check_answer(user_answer, correct_answer, question_number):
    if user_answer.lower() == correct_answer.lower():
        messagebox.showinfo("Correct!", "Your answer is correct!")
        return 1
    else:
        messagebox.showinfo("Wrong!", f"Wrong! The Correct answer is {correct_answer}")
        return 0


def load_questions(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            questions = data.get('questions')
            if questions is not None:
                return questions
            else:
                messagebox.showinfo("Error", "Invalid question format in file")
                return []
    except FileNotFoundError:
        messagebox.showinfo("Error", f"File not found: {filepath}")
        return []
    except json.JSONDecodeError:
        messagebox.showinfo("Error", f"Invalid JSON format in file: {filepath}")
        return []


def next_question():
    global question_index
    global source

    if questions and question_index < len(questions):
        question = questions[question_index]
        question_text.set(f"Question {question_index + 1}: {question['question']}")
        option_text.set("\n".join([f"{i}. {option} " for i, option in enumerate(question['options'], start=1)]))
        question_index += 1
        submit_button.config(state=tk.NORMAL)
    else:
        messagebox.showinfo("Quiz over", f"Your final score is {score}")
        question_index = 0
        submit_button.config(state=tk.DISABLED)
        root.destroy()


def submit_answer():
    global score
    user_answer = answer_entry.get().strip()
    if user_answer:
        correct_answer = questions[question_index - 1]['correctAnswer']
        score += check_answer(user_answer, correct_answer, question_index)
        next_question()
        answer_entry.config(state="normal")
        answer_entry.delete(0, 'end')
    else:
        messagebox.showinfo("Warning", "Please enter an answer.")
        answer_entry.config(state="normal")


domain_file_paths = {
    "Science": "science.json",
    "General Knowledge": "gk.json",
    "Computer Science": "cs.json"
}


def start_quiz(selected_domain):
    global questions
    global question_index
    global score

    filepath = domain_file_paths.get(selected_domain)

    if not filepath:
        messagebox.showinfo("Error", f"No file path found for {selected_domain}")
        return

    questions = load_questions(filepath)

    if not questions:
        print("No questions loaded. Check your JSON file format.")
        return

    random.shuffle(questions)

    # print("Loaded questions:", questions)

    question_index = 0
    score = 0
    next_question()



root = tk.Tk()
root.title("Basic Quiz Game")
root.config(bg="#3333FD")  
root.geometry("650x500")
root.resizable(0, 0)

# Domain selection
domain_label = tk.Label(root, text="Select Domain:", bg="#3333FD", fg="white", font="Helvetica 19 bold")
domain_label.pack(pady=(10, 0))

domain_options = ["General Knowledge", "Science", "Computer Science"]
selected_domain = tk.StringVar(root)
selected_domain.set(domain_options[0])

domain_menu = tk.OptionMenu(root, selected_domain, *domain_options)
domain_menu.config(bg="#FF79C6", fg="white", font="Helvetica 13 bold italic", relief="flat")
domain_menu.pack(pady=5)

# Question & options
question_text = tk.StringVar()
option_text = tk.StringVar()

question_label = tk.Label(root, textvariable=question_text, bg="#3333FD", fg="#0B0E4F", font="Helvetica 16 bold")
question_label.config(wraplength=500, justify="center")
question_label.pack(pady=10)

option_label = tk.Label(root, textvariable=option_text, bg="#3333FD", fg="#DDFF01", font="Helvetica 14 bold")
option_label.config(wraplength=500, justify="center")
option_label.pack(pady=5)

# Entry
answer_label = tk.Label(root, text="Enter Your Answer:", bg="#3333FD", fg="white", font="Helvetica 12 bold")
answer_label.place(x=50, y=260)

answer_entry = tk.Entry(root, font="Helvetica 15 bold", bg="#BDE6ED", fg="black", insertbackground="black")
answer_entry.place(x=50, y=290, width=250)

# Buttons
start_button = tk.Button(root, text="Start", bg="#6272A4", fg="white", font="Verdana 15 bold italic",
                         command=lambda: start_quiz(selected_domain.get()))
start_button.place(x=180, y=350, width=100)

next_button = tk.Button(root, text="Next", bg="#50FA7B", fg="black", font="Verdana 15 bold italic",
                        command=next_question)
next_button.place(x=300, y=350, width=100)

exit_button = tk.Button(root, text="Exit", bg="#FF5555", fg="white", font="Verdana 15 bold italic",
                        command=root.destroy)
exit_button.place(x=420, y=350, width=100)

submit_button = tk.Button(root, text="Submit", bg="#BD93F9", fg="black", font="Verdana 15 bold italic",
                          command=submit_answer, state=tk.DISABLED)
submit_button.place(x=320, y=280, width=120)

root.mainloop()
