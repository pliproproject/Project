import tkinter as tk
from tkinter import ttk
from get_questions import *
from high_scores import *
from play import *

appname = "doYouKnow?"


def start_game():
    print("game started")
    frame_main.place_forget()
    get_name(frame_top)
    get_category(frame_top)
    get_difficulty(frame_top)


def play_trivial():
    qa = get_questions(1, 1)
    play(qa, frame_main)


# ----------------- main --------------------------
if __name__ == '__main__':
    # create main form
    root = tk.Tk()
    root.title(appname)
    window_width = 1024
    window_height = 768
    min_width = 200
    max_width = window_width
    min_height = 200
    max_height = window_height
    root.minsize(min_width, min_height)
    root.maxsize(max_width, max_height)
    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    # transparency
    # root.attributes('-alpha', 0.5)  # transparency
    # root.resizable(False, False)

    frame_top = tk.Frame(root, bg='grey')
    frame_top.place(y=1, height=100, width=window_width)
    frame_top.pack

    frame_main = tk.Frame(root, bg='white')
    frame_main.place(y=100, height=window_height - 160, width=window_width)
    frame_main.pack

    frame_bottom = tk.Frame(root, bg='grey')
    frame_bottom.place(y=708, height=60, width=window_width)
    frame_bottom.pack

    title = ttk.Label(frame_top, text=appname, font='Arial 18 bold')
    title.place(x=20, y=1)
    # Show splash screen for a couple of seconds or destroy on click
    show_splash_screen(frame_main)
    # Show high scores
    show_high_scores(frame_main)

    # start button
    btn_start = ttk.Button(frame_bottom, text="Enter name, category, difficulty", command=start_game)
    btn_start.place(x=20, y=20)

    # play button
    btn_play = ttk.Button(frame_bottom, text="Start Game", command=play_trivial)
    btn_play.place(x=200, y=20)

    # exit button
    btn_exit = ttk.Button(frame_bottom, text='Exit', command=lambda: root.quit())
    btn_exit.place(x=window_width - 100, y=20)
    root.mainloop()
