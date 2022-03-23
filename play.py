from tkinter import ttk


def play(qa, root):
    ttk.Label(root, text=qa['que']).pack()
    for answer in qa['ans']:
        ttk.Label(root, text=answer).pack()
