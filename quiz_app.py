import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from quiz_data import questions
import random
import datetime
from datetime import datetime

class TransparentCanvas(tk.Canvas):
    def __init__(self, master, alpha=0.5, **kwargs):
        super().__init__(master, **kwargs)
        self.itemconfig(self.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), fill='white', outline='white'), stipple='gray12')
        self.alpha = alpha
        self.bind('<Configure>', self._on_configure)

    def _on_configure(self, event):
        self.itemconfig(self.find_withtag(tk.CURRENT), stipple='gray%d' % int(255 * self.alpha))


class QuizApp:
    def __init__(self, master):
        self.master = master
        self.user_answers = []
        self.questions = random.sample(questions, 10)
        self.welcome_screen = TransparentCanvas(master, width=800, height=600, alpha=0.7)

        self.welcome_label = ttk.Label(self.welcome_screen, text="Welcome to the Quiz!", font=("Arial", 24))
        self.welcome_label.place(relx=0.5, rely=0.1, anchor="center")

        self.name_label = ttk.Label(self.welcome_screen, text="Zadajte svoje meno:", font=("Arial", 16))
        self.name_label.place(relx=0.5, rely=0.3, anchor="center")
        self.name_entry = ttk.Entry(self.welcome_screen, width=20)
        self.name_entry.place(relx=0.5, rely=0.35, anchor="center")

        self.num_questions_label = ttk.Label(self.welcome_screen, text="Zadajte počet otázok:", font=("Arial", 16))
        self.num_questions_label.place(relx=0.5, rely=0.45, anchor="center")
        self.num_questions_entry = ttk.Entry(self.welcome_screen, width=20)
        self.num_questions_entry.place(relx=0.5, rely=0.5, anchor="center")

        self.start_button = ttk.Button(self.welcome_screen, text="Začať", command=self.show_quiz_screen)
        self.start_button.place(relx=0.5, rely=0.6, anchor="center")
        self.welcome_screen.pack()
        self.quiz_screen = TransparentCanvas(master, width=800, height=600, alpha=0.7)
        self.quiz_screen.pack_forget()

        self.question_label = ttk.Label(self.quiz_screen, text="Question", font=("Arial", 16))
        self.question_label.grid(row=0, column=0, pady=10)

        self.image_label = ttk.Label(self.quiz_screen)  
        self.image_label.grid(row=1, column=0, pady=10)

        self.selected_answer = tk.StringVar()
        self.answer_buttons = []
        for i in range(4):  
            self.answer_buttons.append(ttk.Radiobutton(self.quiz_screen, text=f"Option {i+1}", value=f"option{i+1}", variable=self.selected_answer, command=self.check_answer))
            self.answer_buttons[i].grid(row=2+i, column=0, pady=10)

        self.feedback_label = ttk.Label(self.quiz_screen, text="", font=("Arial", 12))
        self.feedback_label.grid(row=7, column=0, pady=10)

        self.progress_bar = ttk.Progressbar(self.quiz_screen, orient="horizontal", mode="determinate", maximum=len(questions))
        self.progress_bar.grid(row=10, column=0, pady=10)

        self.next_button = ttk.Button(self.quiz_screen, text="Ďaľšia otázka", state="disabled", command=self.next_question)
        self.next_button.grid(row=8, column=0, pady=10)

        self.submit_button = ttk.Button(self.quiz_screen, text="Ukončit", state="disabled", command=self.show_results)
        self.submit_button.grid(row=9, column=0, pady=10)
        self.current_question = 0
        self.score = 0
        self.user_name = self.name_entry.get()  

    def save_answers(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"./user_answers_{timestamp}.txt", "w") as file:
            for answer in self.user_answers:
                file.write(f"{answer}\n")
            file.write(f"\nScore: {self.score} z {len(self.questions)}\n")

    def show_end_screen(self):
        self.quiz_screen.pack_forget()

        self.end_screen = tk.Frame(self.master)
        self.end_screen.pack()

        tk.Label(self.end_screen, text=f"Koniec! Tvoje skóre je {self.score}.", font=("Arial", 24)).pack()
        tk.Label(self.end_screen, text="Ďakujeme za hranie!", font=("Arial", 24)).pack()

        self.save_answers()

        self.restart_button = ttk.Button(self.end_screen, text="Začať znova", command=self.restart_quiz)

    def restart_quiz(self):
        self.end_screen.pack_forget()
        self.current_question = 0
        self.score = 0
        self.user_answers = []
        self.qestions = random.sample(questions, 10)
        self.welcome_screen.pack()


    def next_question(self):    
        self.current_question += 1

        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.config(text=question["question"])
            for i in range(4):
                self.answer_buttons[i].config(text=question["options"][i], state="normal")
            self.selected_answer.set("")
        else:
            """ self.question_label.config(text=f"Quiz finished! Your score is {self.score}.")
            for button in self.answer_buttons:
                button.config(state="disabled")
            self.next_button.config(state="disabled") """
            self.show_end_screen()

        self.feedback_label.config(text="")

    def show_quiz_screen(self):
        num_questions = self.num_questions_entry.get()

        if num_questions.isdigit() and int(num_questions) > 0 and int(num_questions) <= len(questions):
            num_questions = int(num_questions)
        else:
            messagebox.showerror("Chyba", "Pocet otazok musi byt vacsi ako 0 a mensi ako pocet otazok v databaze.")
            return

        self.welcome_screen.pack_forget()
        self.quiz_screen.pack()
        self.questions = random.sample(questions, num_questions)

        self.display_question()

    def display_question(self):
        
        question = questions[self.current_question]

        self.question_label.config(text=question["question"])
        for i in range(4):
            self.answer_buttons[i].config(text=question["options"][i], state="normal")
            
            self.selected_answer.set("")


    def check_answer(self):
        selected_answer = self.selected_answer.get()
        selected_answer_text = self.questions[self.current_question]["options"][int(selected_answer[-1]) - 1]
        
        if selected_answer_text == self.questions[self.current_question]["correct"]:
            self.score += 1
            self.feedback_label.config(text="Správne!", foreground="green")
        else:
            self.feedback_label.config(text="Nesprávne!", foreground="red")

        for button in self.answer_buttons:
            button.config(state="disabled")

        self.user_answers.append(selected_answer_text)
        self.next_button.config(state="normal")
        self.next_button.grid(row=8, column=0, pady=10)

        self.submit_button.config(state="normal")
        self.submit_button.grid(row=9, column=0, pady=10)

        self.feedback_label.grid(row=7, column=0, pady=10)
        self.progress_bar.grid(row=10, column=0, pady=10)

    

    def show_results(self):
    
        self.quiz_screen.pack_forget()
        
        self.results_screen = ttk.Frame(self.master)
        self.results_screen.pack()
    
        self.results_label = ttk.Label(self.results_screen, text=f"{self.user_name}, your score is {self.score} out of {len(questions)}!", font=("Arial", 18))
        self.results_label.pack(pady=20)

        self.restart_button = ttk.Button(self.results_screen, text="Restart Quiz", command=self.restart_quiz)
        self.restart_button.pack()

        self.save_answers()

root = tk.Tk()
root.geometry("800x600")

quiz_app = QuizApp(root)

root.mainloop()