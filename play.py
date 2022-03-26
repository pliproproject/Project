import tkinter as tk
from tkinter import ttk
from tkinter import ttk, StringVar
import random


def grab_answer(ans, qa, current_que, answerlist):
    print('a/a:', current_que, '--->', ans.get())
    answerlist[current_que] = ans.get()


#  return answerlist


def show_question(parent, qa, current_que, answerlist):
    ans = tk.IntVar()
    ttk.Label(parent, text=qa['que'], font='Arial 16 bold').place(x=100, y=20)
    answers = [qa['correct'], *qa['ans']]
    random.shuffle(answers)
    radio_count = 0
    radios = []
    for a in answers:
        radio_button = ttk.Radiobutton(parent, text=a, variable=ans, value=radio_count,
                                       command=lambda: grab_answer(ans, qa, current_que, answerlist, ))
        radio_button.place(x=200, y=100 + (30 * radio_count))
        radio_count += 1
        if a == 0:
            radio_button.invoke()
        radios.append(radio_button)

    return ans.get()


def check_answers(qa, answerlist):
    for current_que in range(0, len(qa)):
        #        if qa[current_que]['correct'] == answerlist[k - 1]:
        #            pass
        #        else:
        print(current_que, qa[current_que]['que'], answerlist[0])


def play(qa, parent):

    ans = tk.IntVar()
    answerlist = [range(2)]
    current_que = 0
    ans = show_question(parent, qa[current_que], current_que, answerlist)
    print('ans=', ans, '-->', answerlist)
    ttk.Button(parent, text="check", command=lambda: check_answers(qa, answerlist)).place(x=600, y=20)


"""
    for current_que in range(0, len(qa)):
        # Δημιουργεί το label με την ερώτηση
        ttk.Label(parent, text=qa[current_que]['que'], font='Arial 16 bold').place(x=100, y=20)
        # Η σωστή και οι υπόλοιπες απαντήσεις της τρέχουσας ερώτησης εκχωρούνται στη λίστα answers
        answers = [qa[current_que]['correct'], *qa[current_que]['ans']]
        # Ανακάτεμα των απαντήσεων
        random.shuffle(answers)
        j = 0
        # με το παρακάτω loop φτιάχνει τα radio buttons των απαντήσεων
        for a in answers:
            ttk.Radiobutton(parent, text=a, variable=ans, value=j).place(x=200, y=100 + (30 * j))
            j += 1
        k = 1
        if qa[current_que]['correct'] == answers[k - 1]:
            pass
        else:
            pass
"""
