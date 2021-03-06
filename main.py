import tkinter as tk
from tkinter import ttk
from time import sleep
from game_start import *
from high_scores import *
from play import *
import webbrowser  # για το github link

appname = "didYouKnow?"


# ------------------------- frame show/hide functions-----------------------------

def show_about_frame():
    frame_about.place(x=183, y=100, height=470, width=657)


# ----------------------------------------------------------------------------------
def exit_splash():
    frame_hi_scores.place(y=100, height=window_height - 160, width=window_width)
    show_high_scores(frame_hi_scores)


def start_new_game():
    btn_start["state"] = DISABLED
    frame_hi_scores.place_forget()
    frame_user_data.place(y=100, height=window_height - 160, width=window_width)
    get_user_data(frame_user_data, frame_play, frame_top, frame_bottom, frame_game_score, frame_hi_scores, btn_start)


def create_splash_screen():
    # εδώ δημιουργεί τη splash screen
    splash_root = tk.Toplevel()
    splash_root.title("Splash")
    splash_width = 1024
    splash_height = 568
    min_width = 200
    max_width = window_width
    min_height = 200
    max_height = splash_height
    splash_root.minsize(min_width, min_height)
    splash_root.maxsize(max_width, max_height)
    # get the screen dimension
    splash_screen_width = splash_root.winfo_screenwidth()
    splash_screen_height = splash_root.winfo_screenheight()
    # find the center point
    center_x = int(splash_screen_width / 2 - splash_width / 2)
    center_y = int(splash_screen_height / 2 - splash_height / 2)
    splash_root.geometry(f"{splash_width}x{splash_height}+{center_x}+{center_y}")
    # για να μην εχει τον τιτλο
    splash_root.overrideredirect(True)

    show_splash_screen(splash_root)
    ## required to make window show before the program gets to the mainloop
    splash_root.update()

    ## μετά από 5 secs τη σκοτώνει
    time.sleep(5)
    ## σκοτώνει τη splash
    splash_root.destroy()


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

    root.withdraw()
    create_splash_screen()
    # show window again
    root.deiconify()
    # προσθηκη fav icon
    root.iconbitmap('favicon.ico')

    # δημιουργια των απαραιτητων frames
    frame_top = tk.Frame(root, bg='lightgray')
    frame_top.place(y=1, height=100, width=window_width)
    frame_hi_scores = tk.Frame(root, bg='gainsboro')
    frame_user_data = tk.Frame(root, bg='whitesmoke')
    frame_play = tk.Frame(root, bg='white')
    frame_game_score = tk.Frame(root, bg='#f0f0f0')
    frame_bottom = tk.Frame(root, bg='lightgrey')
    frame_bottom.place(y=708, height=60, width=window_width)
    # Δημιουργεί το about frame για να είναι έτοιμο
    frame_about = tk.Frame(root, bg='white')
    aboutimg = ImageTk.PhotoImage(Image.open("about.png"))
    lbl_aboutimg = Label(frame_about, image=aboutimg)
    lbl_aboutimg.pack()
    lbl_githublink = Label(frame_about, text="github link", fg="blue", bg="white", cursor="hand2")
    lbl_githublink.place(x=35, y=440)
    lbl_githublink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/pliproproject/Project"))
    # Εικονίδιο GitHub
    githubimg = ImageTk.PhotoImage(Image.open("GitHub-Mark.png"))
    lbl_GitHubImg = Label(frame_about, image = githubimg,borderwidth=0, cursor="hand2")
    lbl_GitHubImg.pack(padx=0, side=tk.LEFT)
    lbl_GitHubImg.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/pliproproject/Project"))
    btn_exit_about = ttk.Button(frame_about, text='OK', command=lambda: frame_about.place_forget())
    btn_exit_about.place(x=570, y=440)

    # exit button
    btn_exit = ttk.Button(frame_bottom, text='Exit', command=root.destroy)
    btn_exit.place(x=window_width - 100, y=20)
    # start new game button (ask username etc.)
    btn_start = ttk.Button(frame_bottom, text="Start New Game", command=start_new_game, state=NORMAL)
    btn_start.place(x=30, y=20)

    btn_about = ttk.Button(frame_bottom, text="About", command=lambda: show_about_frame())
    btn_about.place(x=800, y=20)

    exit_splash()

    root.mainloop()