import tkinter as tk
from tkinter import ttk
from quiz_data import questions

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.user_answers = []
        master.title("Python Quiz")
        
        ttk.Style().theme_use('vista')

        self.welcome_screen = ttk.Frame(master)
        self.welcome_label = ttk.Label(self.welcome_screen, text="Welcome to the Python Quiz!", font=("Arial", 18))
        self.welcome_label.pack(pady=20)

        self.name_entry = ttk.Entry(self.welcome_screen, width=20)
        self.name_label = ttk.Label(self.welcome_screen, text="Enter your name (optional):")
        self.name_label.pack()
        self.name_entry.pack(pady=10)

        self.start_button = ttk.Button(self.welcome_screen, text="Start Quiz", command=self.show_quiz_screen)
        self.start_button.pack()
        self.welcome_screen.pack()
        
        self.quiz_screen = ttk.Frame(master)

        self.question_label = ttk.Label(self.quiz_screen, text="Question", font=("Arial", 16))
        self.question_label.pack(pady=10)

        self.image_label = ttk.Label(self.quiz_screen)  
        self.image_label.pack()

        self.selected_answer = tk.StringVar()

        self.answer_buttons = []
        for i in range(4):  
            self.answer_buttons.append(ttk.Radiobutton(self.quiz_screen, text=f"Option {i+1}", value=f"option{i+1}", variable=self.selected_answer, command=self.check_answer))
            self.answer_buttons[i].pack()

        self.feedback_label = ttk.Label(self.quiz_screen, text="", font=("Arial", 12))
        self.feedback_label.pack()

        self.progress_bar = ttk.Progressbar(self.quiz_screen, orient="horizontal", mode="determinate", maximum=len(questions))
        self.progress_bar.pack()

        self.next_button = ttk.Button(self.quiz_screen, text="Next Question", state="disabled", command=self.next_question)
        self.next_button.pack()

        self.submit_button = ttk.Button(self.quiz_screen, text="Submit Quiz", state="disabled", command=self.show_results)
        self.submit_button.pack()

        self.current_question = 0
        self.score = 0
        self.user_name = self.name_entry.get()  

    def save_answers(self):


        with open("user_answers.txt", "a") as file:
            for answer in self.user_answers:
                file.write(f"{answer}\n")

    def next_question(self):    
        
        self.current_question += 1

        if self.current_question < len(questions):
            
            question = questions[self.current_question]
            self.question_label.config(text=question["question"])
            for i in range(4):
                self.answer_buttons[i].config(text=question["options"][i], state="normal")
            
            self.selected_answer.set("")

        else:
            self.question_label.config(text=f"Quiz finished! Your score is {self.score}.")

            for button in self.answer_buttons:
                button.config(state="disabled")

            self.next_button.config(state="disabled")

            self.user_answers.append(self.selected_answer.get())
            self.save_answers()

        self.feedback_label.config(text="")

    def show_quiz_screen(self):
        
        self.welcome_screen.pack_forget()
        self.quiz_screen.pack()

        self.display_question()

    def display_question(self):
        
        question = questions[self.current_question]

        self.question_label.config(text=question["question"])
        for i in range(4):
            self.answer_buttons[i].config(text=question["options"][i], state="normal")
            
            self.selected_answer.set("")

    def check_answer(self):
    
        selected_answer = self.selected_answer.get()
  
        selected_answer_text = questions[self.current_question]["options"][int(selected_answer[-1]) - 1]
        
        if selected_answer_text == questions[self.current_question]["correct"]:
            self.score += 1
            self.feedback_label.config(text="Correct!", foreground="green")

        else:
            self.feedback_label.config(text="Incorrect.", foreground="red")
 
        for button in self.answer_buttons:
            button.config(state="disabled")

    def check_answer(self):
        selected_answer = self.selected_answer.get()

        selected_answer_text = questions[self.current_question]["options"][int(selected_answer[-1]) - 1]

        if selected_answer_text == questions[self.current_question]["correct"]:
            self.score += 1
            self.feedback_label.config(text="Correct!", foreground="green")

        else:
            self.feedback_label.config(text="Incorrect.", foreground="red")
        
        for button in self.answer_buttons:
            button.config(state="disabled")

        self.next_button.config(state="normal")

    def show_results(self):
        
        self.quiz_screen.pack_forget()
        
        self.results_screen = ttk.Frame(self.master)
        self.results_screen.pack()
       
        self.results_label = ttk.Label(self.results_screen, text=f"{self.user_name}, your score is {self.score} out of {len(questions)}!", font=("Arial", 18))
        self.results_label.pack(pady=20)

        self.restart_button = ttk.Button(self.results_screen, text="Restart Quiz", command=self.restart_quiz)
        self.restart_button.pack()

root = tk.Tk()
root.geometry("800x600")

quiz_app = QuizApp(root)

root.mainloop()