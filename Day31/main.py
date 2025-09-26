from tkinter import *
from data_manager import DataManager

BACKGROUND_COLOR = "#B1DDC6"
current_card={}

def show_new_word():
    global current_card
    current_card = data.choice_word()
    if current_card != None:
        canvas.itemconfig(word_text, text=current_card["French"], fill="black")
        canvas.itemconfig(canvas_image, image=card_front)
        canvas.itemconfig(language_text, text="French", fill="black")
        window.after(3000, flip)
    else:
        canvas.itemconfig(word_text, text="All Words learned 🎉", fill="black")
        canvas.itemconfig(language_text, text="", fill="black")

def flip():
    try:
        english_card = current_card["English"]
        canvas.itemconfig(canvas_image, image=card_back)
        canvas.itemconfig(language_text, text="English", fill="white")
        canvas.itemconfig(word_text, text=english_card, fill="white")
    except TypeError:
        print("No more words")


def right_button_click():
    try:
        data.remove_word()
    except ValueError:
        print("No more words")
    show_new_word()
    data.save_progress()

def wrong_button_click():
    show_new_word()

window = Tk()
data = DataManager()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
window.geometry("900x726")

window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0,weight=1)
window.grid_columnconfigure(1,weight=1)

canvas = Canvas(width=800, height=526, highlightthickness = 0, bg= BACKGROUND_COLOR)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image= canvas.create_image(400, 263, image = card_front)
language_text= canvas.create_text(400, 150 ,text="French", font=("Ariel",40, "italic"))
word_text= canvas.create_text(400, 263 ,text="Word", font=("Ariel",60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness = 0, command=wrong_button_click)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness = 0, command=right_button_click)
right_button.grid(row=1, column=1)

show_new_word()

window.mainloop()