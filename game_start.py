from tkinter import *
import tkinter
from tkinter.ttk import *
from play import play
import pygame
username = ""
level = ""


def get_user_data(parent, frame_play, frame_top, frame_bottom, frame_game_score, frame_hi_scores, btn_start):
    # σταματαω οποιαδηποτε αλλη μουσικη παιζει
    pygame.mixer.music.stop()
    #  αρχικοποιηση του mixer module
    pygame.mixer.init()
    #  φορτωνω την μουσικη
    pygame.mixer.music.load("user_info.mp3")
    # και του λεω ποσες φορες να παιξει το αρχειο της μουσικης
    pygame.mixer.music.play(loops=1)
    # λήψη ονόματος παίκτη
    lbl = Label(parent, text="Please type a username:")
    # lbl.grid(column=0, row=0)
    lbl.place(x=150, y=30)
    txt = Entry(parent, width=10)
    txt.place(x=300, y=30)
    # txt.grid(column=1, row=0)

    # επιλογή επιπέδου δυσκολίας
    var = StringVar()
    var.set(None)

    def selected():
        nlevel = int(var.get())
        if (nlevel == 1):
            level = "easy"
        if (nlevel == 2):
            level = "medium"
        if (nlevel == 3):
            level = "hard"

    Label(parent, text="select level:").place(x=150, y=70)
    rad1 = Radiobutton(parent, text='Easy   ', value=1, variable=var, command=selected)
    rad2 = Radiobutton(parent, text='Medium', value=2, variable=var, command=selected)
    rad3 = Radiobutton(parent, text='Hard   ', value=3, variable=var, command=selected)

    rad1.place(x=300, y=70)
    rad2.place(x=300, y=90)
    rad3.place(x=300, y=110)
    # rad1.grid(column=1, row=1)
    # rad2.grid(column=1, row=2)
    # rad3.grid(column=1, row=3)

    # επιλογή κατηγορίας ερωτήσεων
    lbl = Label(parent, text="Please select a category:")
    # lbl.grid(column=0, row=0)
    lbl.place(x=150, y=140)
    cat = StringVar()
    cat_cb = Combobox(parent, textvariable=cat)

    # prevent typing a value
    cat_cb['state'] = 'readonly'
    cat_cb['values'] = ('Any Category',
                        'General Knowledge',
                        'Entertainment: Books',
                        'Entertainment: Film',
                        'Entertainment: Music',
                        'Entertainment: Musicals & Theatres',
                        'Entertainment: Television',
                        'Entertainment: Video Games',
                        'Entertainment: Board Games',
                        'Science & Nature',
                        'Science: Computers',
                        'Science: Mathematics',
                        'Mythology',
                        'Sports',
                        'Geography',
                        'History',
                        'Politics',
                        'Art',
                        'Celebrities',
                        'Animals',
                        'Vehicles',
                        'Entertainment: Comics',
                        'Science: Gadgets',
                        'Entertainment: Japanese Anime & Manga',
                        'Entertainment: Cartoon & Animations')

    cat_cb.current(0)
    cat_cb.place(x=300, y=140)

    # cat_cb.grid(column=0, row=2)

    def clicked3():
        username = txt.get()
        # print('user=',username)
        nlevel = int(var.get())
        # print('category=',cat_cb.current())
        if (nlevel == 1):
            level = "easy"
        if (nlevel == 2):
            level = "medium"
        if (nlevel == 3):
            level = "hard"
        print('level=', level)
        if (cat_cb.current() != 0):
            what_category = 8 + cat_cb.current()
        else:
            what_category = "any"
        if (what_category == "any"):
            params = dict(
                amount='9',
                difficulty=level
            )
        else:
            params = dict(
                amount='9',
                category=what_category,
                difficulty=level
            )
        # καλεί την play για να αρχίσει το παιχνίδι
        category = cat.get()
        play(frame_play, frame_top, frame_bottom, frame_game_score, parent, frame_hi_scores, params, username, category, btn_start)

    btn3 = Button(parent, text="Continue", command=clicked3)
    btn3.place(x=350, y=200)
    # btn3.grid(column=0, row=5)
