BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
from tkinter import messagebox
import pandas,random,os
import pygame

pygame.mixer.init()# initialise the pygame

if os.path.exists("data/to_learn.csv"):
    data=pandas.read_csv("data/to_learn.csv")
else:
    data = pandas.read_csv("data/german_words.csv")

to_learn=data.to_dict(orient="records")

word=""
en_of_word=""
random_number=None

window = Tk()
window.minsize()
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

tick_image = PhotoImage(file="images/right.png")
x_image = PhotoImage(file="images/wrong.png")
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")

def play_correct():
    pygame.mixer.music.load('sounds/correct.mp3')
    pygame.mixer.music.play(loops=0)

def play_wrong():
    pygame.mixer.music.load('sounds/wrong.mp3')
    pygame.mixer.music.play(loops=0)

def change_side():
    tick_button.config(state=NORMAL)
    x_button.config(state=NORMAL)
    canvas.itemconfig(card_image,image=back_card)
    canvas.itemconfig(word_text,text=en_of_word,fill="white")
    canvas.itemconfig(language,text="English",fill="white")
    window.after_cancel(bg_changer)
def random_word():
    global word, en_of_word,bg_changer
    random_number = random.randint(0, len(to_learn)-1)
    random_generated_word = to_learn[random_number]["German"]
    word = random_generated_word
    en_of_word = to_learn[random_number]["English"]
    bg_changer=window.after(3000,change_side)
def clicked_right():
    play_correct()
    tick_button.config(state=DISABLED)
    x_button.config(state=DISABLED)
    global word, en_of_word
    canvas.itemconfig(card_image,image=front_card)
    random_word()
    canvas.itemconfig(language, text="German",fill="black")
    canvas.itemconfig(word_text, text=word,fill="black")
    for index, item in enumerate(to_learn):
        if item['German'] == word:
            index_to_remove = index
            if index_to_remove != -1:
                del to_learn[index_to_remove]
                break
def clicked_wrong():
    play_wrong()
    tick_button.config(state=DISABLED)
    x_button.config(state=DISABLED)
    canvas.itemconfig(card_image,image=front_card)
    global word,en_of_word
    random_word()
    canvas.itemconfig(language, text="German", fill="black")
    canvas.itemconfig(word_text, text=word, fill="black")

random_word()

card_image=canvas.create_image(400, 270, image=front_card)
language = canvas.create_text(400, 125, text="German", fill="black",font=("Ariel",35,"italic"))
word_text = canvas.create_text(400, 260, text=word, fill="black",font=("Ariel",60,"bold"))

canvas.grid(row=0, column=0,columnspan=2)

tick_button = Button(image=tick_image,highlightthickness=0,command=clicked_right,state="disabled")
tick_button.grid(row=1, column=1)

x_button = Button(image=x_image,highlightthickness=0,command=clicked_wrong,state="disabled")
x_button.grid(row=1, column=0)

def on_closing():
    global to_learn
    if messagebox.askokcancel("Close", "Are you sure?"):
        to_learn=pandas.DataFrame(to_learn)
        to_learn.to_csv("data/to_learn.csv",index=False)

        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
