import tkinter as tk
from tkinter import ttk
from tkinter import ttk, StringVar
import random


def grab_answer(ans, qa, current_que, answerlist):
    print('a/a:', current_que, '--->', ans.get())
    answerlist[current_que] = ans.get()
    qa[current_que]['user_answer'] = ans.get()


#  return answerlist


def show_question(parent, qa, current_que, answerlist):
    current_que++1
    ans = tk.StringVar()
    ttk.Label(parent, text=str(current_que+1) + '.' + ' ' + qa[current_que]['question'],
              font='Arial 16 bold', wraplength=900, justify="left").place(x=100, y=20)
    answerlist = [0, 0]
    answers = [qa[current_que]['correct_answer'], *qa[current_que]['incorrect_answers']]
    random.shuffle(answers)
    radio_count = 0
    radios = []
    for a in answers:
        radio_button = ttk.Radiobutton(parent, text=a, variable=ans, value=a,
                                       command=lambda: grab_answer(ans, qa, current_que, answerlist))
        radio_button.place(x=200, y=100 + (30 * radio_count))
        radio_count += 1
        if a == 0:
            radio_button.invoke()
        radios.append(radio_button)

    return ans.get()


def check_answers(qa, answerlist):
    for current_que in range(0, len(qa)):
        print(current_que, qa[current_que]['question'], answerlist[0], '----', qa[current_que]['user_answer'],
              qa[current_que]['elapsed_time'])
        if qa[current_que]['correct_answer'] == qa[current_que]['user_answer']:
            print(current_que+1, 'correct')
        else:
            print(current_que+1, 'wrong')


def play(qa, parent):
    # Η παρακάτω εντολή ανακατεύει τη σειρά των ερωτήσεων
    random.shuffle(qa)
    for q in qa:
        q['user_answer'] = -1
        q['elapsed_time'] = 0
    ans = tk.IntVar()
    answerlist = [range(2)]
    current_que = -1
    ans = show_question(parent, qa, current_que, answerlist)
    print('ans=', ans, '-->', answerlist)
    ttk.Button(parent, text="check", command=lambda: check_answers(qa, answerlist)).place(x=600, y=500)
    ttk.Button(parent, text="next question", command=lambda: show_question(parent, qa, current_que, answerlist)).place(x=750, y=500)