from tkinter import ttk


def get_questions(category, difficulty):
    qa = {'que': 'Which is the capital of Peru?', 'ans': ["Lima", "Paris", "London", "Rome"]}
    return qa


def get_user_data(parent):
    player = 'Player'
    lbl_player = ttk.Label(parent, text='get user name, category, difficulty frame', font='Arial 12 bold')
    lbl_player.place(x=10, y=10)
    category = 'category 1'
    difficulty = 'difficulty 1'
    return [player, category, difficulty]

