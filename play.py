from tkinter import ttk


def play(qa, parent):
    ttk.Label(parent, text=qa['que']).pack()
    for answer in qa['ans']:
        ttk.Label(parent, text=answer).pack()
