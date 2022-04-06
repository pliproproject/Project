import tkinter as tk
from tkinter import ttk
from tkinter import ttk, StringVar
from tkinter import messagebox
import random
import time
import threading
from time import perf_counter

from get_questions import get_questions

time_start = 0
game_duration = 180
stop_threads = False
# game_score = [{'name': '', 'category': '', 'difficulty': 0, 'score': 0, 'correct': 0, 'wrong': 0,'not_answered': 0, 'time': 0,'game_sets': 0}]
game_score = []
game_number = 0


def viewing_time():
    global time_start
    return int((perf_counter() - time_start) * 100)


def keep_answer(answer, qa, current_que):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    print('a/a:', current_que, '--->', answer.get(), '-time=', qa[current_que[0]]['viewing_time'])
    qa[current_que[0]]['user_answer'] = answer.get()
    # επιλέγοντας μια απάντηση ο χρόνο που εμφανίζεται η ερώτηση στον παίχτη γίνεται και ο χρόνος που απαιτήθηκε
    # για να απαντηθεί
    qa[current_que[0]]['time_to_answer'] = qa[current_que[0]]['viewing_time']


def next_question(parent, qa, current_que):
    global time_start
    print('a/a=', current_que[0], '---len(qa)=', len(qa), "start time=", time_start, "endtime=", perf_counter(), '----',
          perf_counter() - time_start)
    qa[current_que[0]]['viewing_time'] += viewing_time()
    if current_que[0] < len(qa) - 1:
        current_que[0] = current_que[0] + 1
        show_question(parent, qa, current_que)


def prev_question(parent, qa, current_que):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    if current_que[0] > 0:
        current_que[0] = current_que[0] - 1
        show_question(parent, qa, current_que)


def first_question(parent, qa, current_que):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    current_que[0] = 0
    show_question(parent, qa, current_que)


def last_question(parent, qa, current_que):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    current_que[0] = len(qa) - 1
    show_question(parent, qa, current_que)


def show_question(parent, qa, current_que):
    global time_start
    time_start = perf_counter()
    print("start time=", time_start)
    # διαγράφει όλα τα controls του frame για να εμφανίσει την επόμενη ερώτηση
    for widgets in parent.winfo_children():
        widgets.destroy()
    answer = tk.StringVar()
    label_que = ttk.Label(parent, text=str(current_que[0] + 1) + '.' + ' ' + qa[current_que[0]]['question'],
                          font='Arial 16 bold', wraplength=900, justify="left")
    label_que.place(x=100, y=20)
    radio_count = 0
    radios = []
    for a in qa[current_que[0]]['all_answers']:
        radio_button = ttk.Radiobutton(parent, text=a, variable=answer, value=a,
                                       command=lambda: keep_answer(answer, qa, current_que))
        radio_button.place(x=200, y=100 + (30 * radio_count))
        radio_count += 1
        # Αν ο παίκτης έχει απαντήσει προηγουμένως αυτή την ερώτηση, θα κάνει selected το συγκεκριμένο radio
        if qa[current_que[0]]['user_answer'] == a:
            print('already answered')
            radio_button.invoke()
        #      if a == 0:
        #          radio_button.invoke()
        radios.append(radio_button)
    return


def check_answers(qa, frame_play, frame_top, frame_bottom, second):
    global game_number
    global game_score
    global game_duration
    # counter_label(lbl, False)

    score = 0
    difficulty = 1
    not_answered = 1
    gs = {'name': '', 'category': '', 'difficulty': 0, 'score': 0, 'correct': 0, 'wrong': 0, 'not_answered': 0,
          'time': 0}
    game_score.append(gs)
    game_score[game_number]['time'] = game_duration - int(second.get())
    game_score[game_number]['name'] = 'Παίκτης 1'
    game_score[game_number]['difficulty'] = difficulty
    game_score[game_number]['category'] = 'Science'
    for que in range(0, len(qa)):
        # Μετράει τις μη απαντημένες ερωτήσεις
        if len(qa[que]['user_answer']) == 0:
            game_score[game_number]['not_answered'] += 1
        print(que + 1, qa[que]['question'], '-user answer=', qa[que]['user_answer'], '-time=',
              qa[que]['time_to_answer'])
        if qa[que]['correct_answer'] == qa[que]['user_answer']:
            game_score[game_number]['score'] += difficulty * qa[que]['time_to_answer']
            game_score[game_number]['correct'] += 1
            print(que + 1, 'correct')
        else:
            game_score[game_number]['wrong'] += 1
            print(que + 1, 'wrong')
    # Αν ο υπολειπόμενος χρόνος είναι > 0 θα πρέπει να ελέγξει αν έχει απαντήσει τουλάχιστον 6 ερωτήσεις τις 2
    print('SCORE=', game_score)
    # Αν ολοκλήρωσε το παιχνίδι εντός του χρόνου
    if game_score[game_number]['time'] < game_duration:
        # και αν δεν έχει παίξει πάνω από 2 παιχνίδια ή αν έχει παίξει και δεν έχει αφήσει αναπάντητες πάνω
        # από 3 ερωτήσεις του δίνει τη δυνατότητα να ξαναπαίξει άλλο ένα set
        if (game_number < 2) or (game_number >= 2 and game_score[game_number-1]['not_answered'] < 3
                                 and game_score[game_number-2]['not_answered'] < 3):
            game_number += 1
        # messagebox.showinfo(second.get())
            get_questions(1, 1)
            play(qa, frame_play, frame_top, frame_bottom)


def stop_countdown():
    global stop_threads
    stop_threads = True


def countdown(parent, second, qa, frame_play, frame_top, frame_bottom):
    temp = int(second.get())
    while temp > -1:
        secs = temp
        # using format () method to store the value up to 3 decimal places
        second.set("{0:3d}".format(secs))
        # updating the GUI window after decrementing the
        # temp value every time
        parent.update()
        time.sleep(1)
        if temp == 0:
            messagebox.showinfo("Τέλος", "Η χρόνος έληξε! ")
            check_answers(qa, frame_play, frame_top, frame_bottom, 0)
        global stop_threads
        if stop_threads:
            break
        # after every one sec the value of temp will be decremented by one
        temp -= 1


counter = 0
running = False


# def counter_label(lbl, running):
#     def count():
#         if running:
#             global counter
#             if counter == 0:
#                 display = "0"
#             else:
#                 display = str(counter)
#             lbl['text'] = display
#             lbl.after(10, count)
#             counter += 1
#     count()


def play(qa, parent, frame_top, frame_bottom):
    global stop_threads
    second = StringVar()
    second.set("180")
    lbl = tk.Label(frame_top, text="00", fg="black", bg="yellow", font="Verdana 30 bold")
    lbl.place(x=10, y=30)
    # counter_label(lbl, True)
    tk.Label(frame_top, font=("Arial", 18, ""), bg='lightgray', text='Χρόνος:').place(x=860, y=30)
    seconds = tk.Label(frame_top, width=3, font=("Arial", 18, ""), bg='lightgray', fg='red', textvariable=second)
    seconds.place(x=950, y=30)
    threading.Thread(target=lambda: countdown(frame_top, second, qa, parent, frame_top, frame_bottom)).start()
    # Η παρακάτω εντολή ανακατεύει τη σειρά των ερωτήσεων
    random.shuffle(qa)
    # φτιάχνει 2 κλειδιά στο λεξικό κάθε ερώτησης, την απάντηση του παίκτη με τιμή -1 το χρόνο εμφάνισης κάθε
    # ερώτησης και το χρόνο απάντησης με τιμή 0
    for q in qa:
        # καταχωρεί τη σωστή και τις λανθασμένες απαντήσεις κάθε ερώτησης στη λίστα answers
        answers = [q['correct_answer'], *q['incorrect_answers']]
        # ανακατεύει τις απαντήσεις
        random.shuffle(answers)
        # τις ανακατεμένες απαντήσεις τις καταχωρεί στο λεξικό κάθε ερώτησης
        q['all_answers'] = answers
        q['user_answer'] = ''
        q['viewing_time'] = 0
        q['time_to_answer'] = 0
    # ans = tk.IntVar()
    # Η τρέχουσα ερώτηση (current_que) ορίζεται σαν λίστα για να μπορεί να αλλάξει τιμή μέσα από άλλη συνάρτηση
    print('-----------------------1η ερώτηση-----------------------------------')
    current_que = [0]
    #   p2 = Process(target=show_question(parent, qa, current_que))
    #   p2.start()
    show_question(parent, qa, current_que)
    ttk.Button(frame_bottom, text="check",
               command=lambda: [stop_countdown(), check_answers(qa, parent, frame_top, frame_bottom, second)]).place(
        x=800, y=20)
    ttk.Button(frame_bottom, text="next question", command=lambda: next_question(parent, qa, current_que)).place(x=550,
                                                                                                                 y=1)
    ttk.Button(frame_bottom, text="prev question", command=lambda: prev_question(parent, qa, current_que)).place(x=550,
                                                                                                                 y=30)
    ttk.Button(frame_bottom, text="1st question", command=lambda: first_question(parent, qa, current_que)).place(x=650,
                                                                                                                 y=1)
    ttk.Button(frame_bottom, text="last question", command=lambda: last_question(parent, qa, current_que)).place(x=650,
                                                                                                                 y=30)
