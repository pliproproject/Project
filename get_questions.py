from tkinter import ttk


def get_name(root):
    player = 'Player'
    lbl_player = ttk.Label(root, text=player, font='Arial 12 bold')
    lbl_player.place(x=950, y=10)
    return 'Player'


def get_category(root):
    return 1


def get_difficulty(root):
    return 1


def get_questions(category, difficulty):
    qa = {'que': 'Which is the capital of Peru?', 'ans': ["Lima", "Paris", "London", "Rome"]}
    return qa

