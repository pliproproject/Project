import tkinter as tk
from tkinter import ttk
from get_questions import *
from high_scores import *
from play import *

appname = "doYouKnow?"


def start_game():
    print("game started")
    get_name()
    get_category()
    get_difficulty()


def play_trivial():
    qa = get_questions(1, 1)
    print(qa['que'])
    ttk.Label(root, text=qa['que']).pack()
    for answer in qa['ans']:
        ttk.Label(root, text=answer).pack()


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
    ttk.Label(root, text=appname).pack()

    show_splash_screen()
    show_high_scores()

    # exit button
    exit_button = ttk.Button(root, text='Exit', command=lambda: root.quit())
    exit_button.pack(ipadx=5, ipady=10, expand=True)

    demo_button = ttk.Button(root, text="Give name, category, difficulty", command=start_game())
    demo_button.pack(ipadx=10, ipady=10, expand=True)

    demo_button = ttk.Button(root, text="Start Game", command=play_trivial())
    demo_button.pack(ipadx=10, ipady=10, expand=True)
    root.mainloop()
