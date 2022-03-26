import tkinter as tk
from tkinter import ttk
from tkinter import ttk, StringVar
import random


def check_answer(v):
    print('--->', v.get())


def show_question(parent, qa):
    ans = tk.IntVar()
    ttk.Label(parent, text=qa['que'], font='Arial 16 bold').place(x=100, y=20)
    answers = [qa['correct'], *qa['ans']]
    random.shuffle(answers)
    j = 0
    for a in answers:
        ttk.Radiobutton(parent, text=a, variable=ans, value=j).place(x=200, y=100 + (30 * j))
        j += 1
    return ans


def play(qa, parent):
    qa = [{'que': 'which is the capital of Peru', 'correct': 'Peru', 'ans': ['London', 'Paris', 'Rome']},
          {'que': 'which is the capital of France', 'correct': 'Paris', 'ans': ['Madrid', 'Amsterdam', 'Brussels']}]
    v = tk.IntVar()
    for current_que in range(0, len(qa)):
        ttk.Label(parent, text=qa[current_que]['que'], font='Arial 16 bold').place(x=100, y=20)
        answers = [qa[current_que]['correct'], *qa[current_que]['ans']]
        random.shuffle(answers)
        j = 0
        for a in answers:
            ttk.Radiobutton(parent, text=a, variable=v, value=j).place(x=200, y=100 + (30 * j))
            j += 1
        k = 1
        if qa[current_que]['correct'] == answers[k - 1]:
            pass
        else:
            pass
    ttk.Button(parent, text="check", command=lambda: check_answer(v)).place(x=600, y=20)
