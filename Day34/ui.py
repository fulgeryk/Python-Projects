from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady= 20, bg=THEME_COLOR)
        self.window.geometry("400x500")
        self.window.grid_rowconfigure(0,weight=1)
        self.window.grid_rowconfigure(1,weight=1)
        self.window.grid_rowconfigure(2,weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.canvas = Canvas(width=300, height=250, highlightthickness=0, bg="white")
        self.text_on_canvas=self.canvas.create_text(150, 125, width=290, text="Vedem daca e in mijloc", fill="black", font=("Ariel", 20, "italic"))
        self.canvas.grid(column=0, row=1, columnspan=2)
        self.score=0
        self.score_label=Label(text=f"Score: {self.score}", font=("Ariel", 10, "bold"), bg=THEME_COLOR, pady = 20, fg="white")
        self.score_label.grid(column=1, row=0)
        self.correct_image = PhotoImage(file="./images/true.png")
        self.incorrect_image = PhotoImage(file="./images/false.png")
        self.correct_button = Button(image=self.correct_image, highlightthickness=0, command=self.press_correct_button)
        self.correct_button.grid(row=2, column=0, pady=(30, 0))
        self.incorrect_button = Button(image=self.incorrect_image, highlightthickness=0, command=self.press_incorrect_button)
        self.incorrect_button.grid(row=2, column=1, pady=(30, 0))
        self.get_next_question()
        self.window.mainloop()


    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.text_on_canvas, text=q_text)
        else:
            self.canvas.itemconfig(self.text_on_canvas, text="You've reached the end of the quiz.")
            self.correct_button.config(state="disabled")
            self.incorrect_button.config(state="disabled")


    def press_correct_button(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def press_incorrect_button(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def increase_score(self):
        self.score +=1
        self.score_label.config(text=f"Score:{self.score}")

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
            self.increase_score()
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, func=self.get_next_question)

