import tkinter
from tkinter import *
import math
import sys
import os
import winsound
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
# ---------------------------- AUXILIARY FUN ------------------------------- #


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


tomato_path = resource_path("tomato.png")

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps, timer
    window.after_cancel(timer)
    reps = 0
    title_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    checkmark_label.config(text="")
    start_button.config(state=ACTIVE)


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    start_button.config(state=DISABLED)
    reps += 1
    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(WORK_MIN * 60)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        window.state(newstate="normal")
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)
        winsound.PlaySound("SystemNotification", winsound.SND_ASYNC)
        if reps % 2 == 0:
            work_sessions = math.floor(reps/2)
            marks = "✔" * work_sessions
            checkmark_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
window.iconphoto(False, tkinter.PhotoImage(file=tomato_path))


canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=tomato_path)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 135, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
canvas.grid(row=2, column=2)

title_label = Label(text="Timer", font=(FONT_NAME, 35, "bold"), fg=GREEN, background=YELLOW)
title_label.config(padx=5, pady=5)
title_label.grid(row=1, column=2)

credits_label = Label(text="by Catxa \nVersion 1.0",font=(FONT_NAME, 8, "bold"), fg=GREEN, background=YELLOW)
credits_label.config(padx=0, pady=0)
credits_label.grid(row=6, column=2)

checkmark_label = Label(font=(FONT_NAME, 10, "bold"), fg=GREEN, background=YELLOW)
checkmark_label.config(padx=5, pady=5)
checkmark_label.grid(row=4, column=2)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(row=3, column=1)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(row=3, column=3)

tkinter.mainloop()

