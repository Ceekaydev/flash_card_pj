import tkinter as tk
import csv
import random
from PIL import Image, ImageTk

BACKGROUND_COLOR = "#B1DDC6"

def next_card():
    global random_dict, timer
    # Cancel any running timer
    if timer is not None:
        window.after_cancel(timer)

    # Pick a new card
    random_dict = random.choice(data_list)

    # Show front page
    canvas.itemconfig(front_img, image=front_page)
    canvas.itemconfig(front_titles, text="French", fill="black", font=("Arial", 40, "italic"))
    canvas.itemconfig(front_words, text=(random_dict["french"]).title(), fill="black", font=("Arial", 60, "bold"))

    # Restart countdown
    count_down(5)
    
# ---------- Countdown ----------- #
def count_down(count):
    global timer
    if count >= 0:
        canvas.itemconfig(count_text, text=str(count))
        timer = window.after(1000, count_down, count - 1)
    else:
        flip_card()


def flip_card():
    canvas.itemconfig(front_img, image=back_page)
    canvas.itemconfig(front_titles, text="English", fill="black", font=("Arial", 40, "italic"))
    canvas.itemconfig(front_words, text=(random_dict["english"]).title(), fill="black", font=("Arial", 60, "bold"))

def correct_button():
    global random_dict
    if random_dict in data_list:
        with open("../flash-card-project-start/data/correct_guess.csv", mode="a") as data:
            data.write(str(random_dict) + "\n")
    data_list.remove(random_dict)  # remove learned word


    if len(data_list) == 0:
        canvas.itemconfig(front_titles, text="", fill="black")
        canvas.itemconfig(front_words, text="Done! 🎉", fill="black")
        return
    next_card()

def wrong_button():
    next_card()





# ---------- Access csv ----------- #
data_list = []
with open("../flash-card-project-start/data/french_words.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data_list.append({
            "french" : row["French"],
            "english" : row["English"]
        })

random_dict = {}

# ---------- UI ----------- #

window = tk.Tk()
window.title("My flashcard Project")
window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(width=800, height=526, bd=0, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(row=0, column=0, columnspan=2)



front_page = tk.PhotoImage(file="../flash-card-project-start/images/card_front.png")
front_img = canvas.create_image(400, 263, image=front_page)

back_page = tk.PhotoImage(file="../flash-card-project-start/images/card_back.png")

front_titles = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
front_words = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))

# title_label = tk.Label(text="Title", font=("Arial", 40, "italic"), bg=BACKGROUND_COLOR, fg="white")
# title_label.place(x=400, y=150)

correct_img = tk.PhotoImage(file="../flash-card-project-start/images/right.png")
wrong_img = tk.PhotoImage(file="../flash-card-project-start/images/wrong.png")

correct_button = tk.Button(window, image=correct_img, highlightthickness=0, bd=0, command=correct_button)
correct_button.grid(row=1, column=1, pady=(20,0))

wrong_button = tk.Button(window, image=wrong_img, highlightthickness=0, bd=0, command=wrong_button)
wrong_button.grid(row=1, column=0, pady=(20,0))

reset_button = tk.Button(window, text="Reset", width=10)
reset_button.grid(row=2, column=0, columnspan=2,pady=(10,0))

count_text = canvas.create_text(700,50, text="0", fill="black", font=("Arial", 60, "bold"))

timer = None
next_card()
window.mainloop()


# print(random_dict)
# key_list = list(random_dict)
# print(key_list[0])
# print(key_list[1])
# print(random_dict["french"])
# print(random_dict["english"])