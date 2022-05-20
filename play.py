import tkinter as tk
from tkinter import *
from tkinter import ttk, StringVar
from tkinter import messagebox
from tkinter.messagebox import askyesno
import random
import time
import threading
from time import perf_counter
from PIL import Image, ImageTk
from turtle import left
from tkinter import PhotoImage
# import requests

# from get_questions import get_questions
from high_scores import show_game_score
from get_questions import get_questions

time_start = 0
game_duration = 180
stop_threads = False
game_score = []
game_number = 0
url = "https://opentdb.com/api.php"


def viewing_time():
    global time_start
    return int((perf_counter() - time_start) * 100)


# εμφανίζει το label με τον χρόνο που πήρε στον παίκτη να απαντήσει την τρέχουσα ερώτηση (current_que)
def show_time_to_answer(qa, current_que, frame_top):
    tta = StringVar()
    lbl_time_to_answer = tk.Label(frame_top, textvariable=tta, fg="black", bg="lightgray", font="Arial 12")
    lbl_time_to_answer.place(x=125, y=30)
    print("currentq=", current_que[0], "time to answer=", qa[current_que[0]]['time_to_answer'])
    tta.set(str(qa[current_que[0]]['time_to_answer']).zfill(6))


def keep_answer(answer, qa, current_que, frame_top):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    print('==============================a/a:', current_que, '--->', answer.get(), '-time=',
          qa[current_que[0]]['viewing_time'])
    qa[current_que[0]]['user_answer'] = answer.get()
    # επιλέγοντας μια απάντηση, ο χρόνος που εμφανίζεται η ερώτηση στον παίχτη γίνεται και ο χρόνος που απαιτήθηκε
    # για να απαντηθεί
    qa[current_que[0]]['time_to_answer'] = qa[current_que[0]]['viewing_time']
    show_time_to_answer(qa, current_que, frame_top)


def next_question(parent, qa, current_que, frame_top):
    global time_start
    print('a/a=', current_que[0], '---len(qa)=', len(qa), "start time=", time_start, "endtime=", perf_counter(), '----',
          perf_counter() - time_start)
    qa[current_que[0]]['viewing_time'] += viewing_time()
    if current_que[0] < len(qa) - 1:
        current_que[0] = current_que[0] + 1
        show_question(parent, qa, current_que, frame_top)


def prev_question(parent, qa, current_que, frame_top):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    if current_que[0] > 0:
        current_que[0] = current_que[0] - 1
        show_question(parent, qa, current_que, frame_top)


def first_question(parent, qa, current_que, frame_top):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    current_que[0] = 0
    show_question(parent, qa, current_que, frame_top)


def last_question(parent, qa, current_que, frame_top):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    current_que[0] = len(qa) - 1
    show_question(parent, qa, current_que, frame_top)


# Η παρακάτω συνάρτηση εμφανίζει την ερώτηση current_que στον παίκτη
def show_question(parent, qa, current_que, frame_top):
    # Η μεταβλητή time_start κρατάει το χρόνο που άρχισε να βλέπει την ερώτηση ο παίκτης
    global time_start
    time_start = perf_counter()
    show_time_to_answer(qa, current_que, frame_top)

    print("start time=", time_start)
    # διαγράφει όλα τα controls του frame για να εμφανίσει την επόμενη ερώτηση
    for widgets in parent.winfo_children():
        widgets.destroy()
    answer = tk.StringVar()
    labelstyle = ttk.Style()  # Creating style element
    labelstyle.configure('Wild.TLabel', background='white', foreground='black')
    label_que = ttk.Label(parent, text=str(current_que[0] + 1) + '.' + ' ' + qa[current_que[0]]['question'],
                          font='Arial 16 bold', wraplength=900, justify="left", style='Wild.TLabel')
    label_que.place(x=100, y=20)
    radio_count = 0
    radios = []
    radiostyle = ttk.Style()  # Creating style element
    radiostyle.configure('Wild.TRadiobutton',  # First argument is the name of style. Needs to end with: .TRadiobutton
                         background='white',  # Setting background to our specified color above
                         foreground='black')  # You can define colors like this also
    for a in qa[current_que[0]]['all_answers']:
        radio_button = ttk.Radiobutton(parent, text=a, variable=answer, value=a, style='Wild.TRadiobutton',
                                       command=lambda: keep_answer(answer, qa, current_que, frame_top))
        radio_button.place(x=200, y=100 + (30 * radio_count))
        radio_count += 1
        # Αν ο παίκτης έχει απαντήσει προηγουμένως αυτή την ερώτηση, θα κάνει selected το συγκεκριμένο radio
        if qa[current_que[0]]['user_answer'] == a:
            print('already answered')
            # Επιλέγει το radio με την απάντηση του παίκτη από προηγούμενη εμφάνιση
            answer.set(a)
        # radio_button.invoke() δεν έπαιξε αυτό γιατί καλεί και την keep_answer και χαλάει τους χρόνους
        #      if a == 0:
        #          radio_button.invoke()
        radios.append(radio_button)
    return


def check_answers(qa, frame_play, frame_top, frame_bottom, frame_game_score, frame_user_data, second, params, username, category):
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
    game_score[game_number]['name'] = username
    game_score[game_number]['difficulty'] = params['difficulty']
    game_score[game_number]['category'] = category
    print('category=',category)
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
    game_end = True
    if game_score[game_number]['time'] < game_duration:
        # και αν δεν έχει παίξει πάνω από 2 παιχνίδια ή αν έχει παίξει και δεν έχει αφήσει αναπάντητες πάνω
        # από 3 ερωτήσεις του δίνει τη δυνατότητα να ξαναπαίξει άλλο ένα set
        if (game_number < 2) or (game_number >= 2 and game_score[game_number - 1]['not_answered'] < 3
                                 and game_score[game_number - 2]['not_answered'] < 3):
            game_number += 1
            answer = askyesno(title='Επόμενο set ερωτήσεων',
                              message='Θέλετε να συνεχίσετε το παιχνίδι;')
            if answer:
                # get_questions(url, params)
                play(frame_play, frame_top, frame_bottom, frame_game_score, frame_user_data, params, username)
                game_end = False
    if game_end:
        # Κάνει hidden το play_frame
        frame_play.place_forget()
        frame_game_score.place(y=100, height=768 - 160, width=1024)
        show_game_score(frame_game_score, game_score)
        game_score.clear()
        game_number = 0


def stop_countdown():
    global stop_threads
    stop_threads = True


def countdown(second, qa, frame_play, frame_top, frame_bottom, frame_game_score, frame_user_data, url, params):
    global stop_threads
    temp = int(second.get())
    while temp > -1:
        secs = temp
        # using format () method to store the value up to 3 decimal places
        second.set("{0:3d}".format(secs))
        # updating the GUI window after decrementing the
        # temp value every time
        # parent.update()
        time.sleep(1)
        if temp == 0:
            messagebox.showinfo("Τέλος", "Η χρόνος έληξε! ")
            check_answers(qa, frame_play, frame_top, frame_bottom, frame_game_score, frame_user_data, second, params)
        if stop_threads:
            break
        # after every one sec the value of temp will be decremented by one
        temp -= 1


def play(parent, frame_top, frame_bottom, frame_game_score, frame_user_data, params, username, category):
    global stop_threads
    stop_threads = False
    # κάνει hidden το frame που έγινε η εισαγωγή των στοιχείων του παίκτη
    frame_user_data.place_forget()
    # καλεί την get_questions με παραμέτρους το url, την επιλεγμένη από τον παίχτη κατηγορία και το επίπεδο δυσκολίας
    jsondata = get_questions(url, params)
    qa = jsondata['results']

    parent.place(y=100, height=768 - 160, width=1024)
    second = StringVar()
    second.set("180")
    print('params=', params)
    # lbl_time_to_answer = tk.Label(frame_top, text="00", fg="black", bg="yellow", font="Verdana 30 bold")
    # lbl_time_to_answer.place(x=10, y=30)
    # counter_label(lbl, True)

    tk.Label(frame_top, font=("Arial", 12, ""), bg='lightgray', text='Time to answer:').place(x=10, y=30)
    tk.Label(frame_top, font=("Arial", 8, ""), bg='lightgray', text='(1/100 sec)').place(x=10, y=50)
    tk.Label(frame_top, font=("Arial", 14, ""), bg='lightgray', text='Time left:').place(x=870, y=30)
    # Φτιάχνω ένα label που εμφανίζει το χρόνο που έχει απομείνει
    seconds = tk.Label(frame_top, width=3, font=("Arial", 14, ""), bg='lightgray', fg='red', textvariable=second)
    seconds.place(x=950, y=30)
    # Καλώ τη συνάρτηση countdown που μετράει το χρόνο που απομένει μέχρι το τέλος του παιχνιδιού
    # Η συνάρτηση καλείται σε διαφορετικό thread. Αν την καλέσω στο ίδιο thread σταματάει η εκτέλεση του υπόλοιπου
    # προγράμματος μέχρι να περάσουν τα 180sec και συνεχίζει μετά.
    t = threading.Thread(
        target=lambda: countdown(second, qa, parent, frame_top, frame_bottom, frame_game_score, frame_user_data, url,
                                 params))
    t.daemon = True
    t.start()

    # Η παρακάτω εντολή ανακατεύει τη σειρά των ερωτήσεων
    random.shuffle(qa)
    # φτιάχνει 4 κλειδιά στο λεξικό κάθε ερώτησης, όλες τις απαντήσεις, την απάντηση του παίκτη, το χρόνο εμφάνισης κάθε
    # ερώτησης και το χρόνο απάντησης με τιμή 0
    for q in qa:
        # εδώ αντικαθιστώ τα &quot; με " και το &#039; με ' στις ερωτήσεις και απαντήσεις
        question = q['question']
        q['question'] = (question.replace('&quot;', '"')).replace("&#039;", "'")
        ca = q['correct_answer']
        ca = (ca.replace('&quot;', '"')).replace("&#039;", "'")
        ia = q['incorrect_answers']
        for i in range(0, len(ia)):
            ia[i] = (ia[i].replace('&quot;', '"')).replace("&#039;", "'")
        # καταχωρεί τη σωστή και τις λανθασμένες απαντήσεις κάθε ερώτησης στη λίστα answers
        # ???????
        answers = [ca, *ia]
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
    # καλεί τη show_question με παράμετρο την current_que ώστε να εμφανίσει την 1η ερώτηση στον παίκτη
    show_question(parent, qa, current_que, frame_top)
    # Παρακάτω, φτιάχνω τα buttons που βρίσκονται στο button frame τα οποία είναι:
    # Ολοκλήρωση παιχνιδιού, επόμενη, προηγούμενη, 1η τελευταία ερώτηση
    # Χρησιμοποιώ lambda συναρτήσεις γιατί στο button "ολοκλήρωση παιχνιδιού" θα πρέπει πρώτα να καλέσω τη
    # stop_countdown ώστε να σταματήσει το thread με τη μέτρηση του χρόνου. Στις υπόλοιπες είναι απαραίτητο επειδή
    # καλώ με πολλά ορίσματα τις συναρτήσεις στο onclick event
    ttk.Button(frame_bottom, text="End Game",
               command=lambda: [stop_countdown(),
                                check_answers(qa, parent, frame_top, frame_bottom, frame_game_score, frame_user_data,
                                              second, params, username, category)]).place(x=150, y=20)
    ttk.Button(frame_bottom, text=">",
               command=lambda: next_question(parent, qa, current_que, frame_top)).place(x=550, y=20)
    ttk.Button(frame_bottom, text="<",
               command=lambda: prev_question(parent, qa, current_que, frame_top)).place(x=450, y=20)
    ttk.Button(frame_bottom, text="<<",
               command=lambda: first_question(parent, qa, current_que, frame_top)).place(x=350, y=20)
    ttk.Button(frame_bottom, text=">>",
               command=lambda: last_question(parent, qa, current_que, frame_top)).place(x=650, y=20)

