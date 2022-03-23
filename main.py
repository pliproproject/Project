import tkinter as tk
from tkinter import ttk
from get_questions import *
from high_scores import *
from play import *

appname = "doYouKnow?"


def start_game():
    print("game started")
    get_name(root)
    get_category(root)
    get_difficulty(root)


def play_trivial():
    qa = get_questions(1, 1)
    print(qa['que'])
    play(qa, root)


# ----------------- main --------------------------
if __name__ == '__main__':
    # create main form
    root = tk.Tk()
    root.title('doYouKnow?')
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

    title = ttk.Label(root, text=appname, font='Arial 18 bold')#.pack
    title.place(x=20, y=1)
    show_splash_screen(root)
    show_high_scores(root)

    # start button
    btn_start = ttk.Button(root, text="Enter name, category, difficulty", command=start_game)
    btn_start.place(x=20, y=window_height - 50)

    # play button
    btn_play = ttk.Button(root, text="Start Game", command=play_trivial)
    btn_play.place(x=200, y=window_height - 50)

    # exit button
    btn_exit = ttk.Button(root, text='Exit', command=lambda: root.quit())
    btn_exit.place(x=window_width - 100, y=window_height - 50)
    root.mainloop()
