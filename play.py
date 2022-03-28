import tkinter as tk
from tkinter import ttk
from tkinter import ttk, StringVar
import random
import time
import threading
from tkinter import messagebox
from multiprocessing import Process

def keep_answer(answer, qa, current_que):
    print('a/a:', current_que, '--->', answer.get())
    qa[current_que[0]]['user_answer'] = answer.get()


def next_question(parent, qa, current_que):
    print('a/a=', current_que, '---len(qa)=', len(qa))
    if current_que[0] < len(qa) - 1:
        current_que[0] = current_que[0] + 1
        show_question(parent, qa, current_que)


def prev_question(parent, qa, current_que):
    if current_que[0] > 0:
        current_que[0] = current_que[0] - 1
        show_question(parent, qa, current_que)


def first_question(parent, qa, current_que):
    current_que[0] = 0
    show_question(parent, qa, current_que)


def last_question(parent, qa, current_que):
    current_que[0] = len(qa) - 1
    show_question(parent, qa, current_que)


def show_question(parent, qa, current_que):
    # διαγράφει όλα τα controls του frame για να εμφανίσει την επόμενη ερώτηση
    for widgets in parent.winfo_children():
        widgets.destroy()
    # current_que[0] = current_que[0] + 1
    print('current question=', current_que[0])
    answer = tk.StringVar()
    label_que = ttk.Label(parent, text=str(current_que[0] + 1) + '.' + ' ' + qa[current_que[0]]['question'],
                          font='Arial 16 bold', wraplength=900, justify="left")
    label_que.place(x=100, y=20)
    # answers = [qa[current_que[0]]['correct_answer'], *qa[current_que[0]]['incorrect_answers']]
    # random.shuffle(answers)
    radio_count = 0
    radios = []
    for a in qa[current_que[0]]['all_answers']:
        radio_button = ttk.Radiobutton(parent, text=a, variable=answer, value=a,
                                       command=lambda: keep_answer(answer, qa, current_que))
        radio_button.place(x=200, y=100 + (30 * radio_count))
        radio_count += 1
        # Αν ο παίκτης έχει απαντήσει προηγουμένως αυτή την ερώτηση, θα κάνει selected το συγκεκριμένο radio
        # print("a=", a, "---user answer=", qa[current_que]['user_answer'])
        if qa[current_que[0]]['user_answer'] == a:
            print('already answered')
            radio_button.invoke()

        #      if a == 0:
        #          radio_button.invoke()
        radios.append(radio_button)
    return


def check_answers(qa):
    for que in range(0, len(qa)):
        print(que + 1, qa[que]['question'], '-user answer=', qa[que]['user_answer'], '-time=',
              qa[que]['elapsed_time'])
        if qa[que]['correct_answer'] == qa[que]['user_answer']:
            print(que + 1, 'correct')
        else:
            print(que + 1, 'wrong')


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1




def play(qa, parent, frame_top, frame_bottom):
   # thread = threading.Thread(target=submit(frame_top, hour, minute, second))
   # thread.start()
 #   p1 = Process(target=submit(frame_top, hour, minute, second))
 #   p1.start()
    # countdown(180)
    # Η παρακάτω εντολή ανακατεύει τη σειρά των ερωτήσεων
    random.shuffle(qa)
    # φτιάχνει 2 κλειδιά στο λεξικό κάθε ερώτησης, την απάντηση του παίκτη με τιμή -1 και το χρόνο με τιμή 0
    for q in qa:
        # καταχωρεί τη σωστή και τις λανθασμένες απαντήσεις κάθε ερώτησης στη λίστα answers
        answers = [q['correct_answer'], *q['incorrect_answers']]
        # ανακατεύει τις απαντήσεις
        random.shuffle(answers)
        # τις ανακατεμένες απαντήσεις τις καταχωρεί στο λεξικό κάθε ερώτησης
        q['all_answers'] = answers
        q['user_answer'] = -1
        q['elapsed_time'] = 0
    # ans = tk.IntVar()
    # Η τρέχουσα ερώτηση (current_que) ορίζεται σαν λίστα για να μπορεί να αλλάξει τιμή μέσα από άλλη συνάρτηση
    current_que = [0]
 #   p2 = Process(target=show_question(parent, qa, current_que))
 #   p2.start()
    show_question(parent, qa, current_que)
    ttk.Button(frame_bottom, text="check", command=lambda: check_answers(qa)).place(x=800, y=20)
    ttk.Button(frame_bottom, text="next question", command=lambda: next_question(parent, qa, current_que)).place(x=550,
                                                                                                                 y=1)
    ttk.Button(frame_bottom, text="prev question", command=lambda: prev_question(parent, qa, current_que)).place(x=550,
                                                                                                                 y=30)
    ttk.Button(frame_bottom, text="1st question", command=lambda: first_question(parent, qa, current_que)).place(x=650,
                                                                                                                 y=1)
    ttk.Button(frame_bottom, text="last question", command=lambda: last_question(parent, qa, current_que)).place(x=650,
                                                                                                                 y=30)
