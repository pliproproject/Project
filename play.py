import tkinter as tk
# The Tkinter StringVar helps you manage the value of a widget such as a Label or Entry more effectively.
from tkinter import ttk, StringVar
# The tkinter.messagebox module provides a template base class as well as a variety of convenience methods for
# commonly used configurations.
from tkinter import messagebox
from tkinter.messagebox import askyesno
# This module implements pseudo-random number generators for various distributions.
import random
# This module provides various time-related functions.
import time
import threading
from time import perf_counter
import pygame
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
    lbl_time_to_answer.place(x=125, y=20)
    tta.set(str(qa[current_que[0]]['time_to_answer']).zfill(6))


# Κρατάει την απάντηση του παίκτη για την ερώτηση current_que
def keep_answer(answer, qa, current_que, frame_top):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    qa[current_que[0]]['user_answer'] = answer.get()
    # επιλέγοντας μια απάντηση, ο χρόνος που εμφανίζεται η ερώτηση στον παίχτη γίνεται και ο χρόνος που απαιτήθηκε
    # για να απαντηθεί
    qa[current_que[0]]['time_to_answer'] = qa[current_que[0]]['viewing_time']
    show_time_to_answer(qa, current_que, frame_top)


# Εμφανίζει την επόμενη ερώτηση πατώντας το Next στα navigation buttons
def next_question(parent, qa, current_que, frame_top):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    if current_que[0] < len(qa) - 1:
        current_que[0] = current_que[0] + 1
        show_question(parent, qa, current_que, frame_top)


# Εμφανίζει την προηγούμενη ερώτηση πατώντας το Next στα navigation buttons
def prev_question(parent, qa, current_que, frame_top):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    if current_que[0] > 0:
        current_que[0] = current_que[0] - 1
        show_question(parent, qa, current_que, frame_top)


# Εμφανίζει τη 1η ερώτηση πατώντας το Next στα navigation buttons
def first_question(parent, qa, current_que, frame_top):
    global time_start
    qa[current_que[0]]['viewing_time'] += viewing_time()
    current_que[0] = 0
    show_question(parent, qa, current_que, frame_top)


# Εμφανίζει την τελευταία ερώτηση πατώντας το Next στα navigation buttons
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
    radiostyle = ttk.Style()  # Δημιουργεί το style των radio buttons
    radiostyle.configure('Wild.TRadiobutton',  # Το όνομα του style
                         background='white',
                         foreground='black')
    for a in qa[current_que[0]]['all_answers']:
        radio_button = ttk.Radiobutton(parent, text=a, variable=answer, value=a, style='Wild.TRadiobutton',
                                       command=lambda: keep_answer(answer, qa, current_que, frame_top))
        radio_button.place(x=200, y=100 + (30 * radio_count))
        radio_count += 1
        # Αν ο παίκτης έχει απαντήσει προηγουμένως αυτή την ερώτηση, θα κάνει selected το συγκεκριμένο radio
        if qa[current_que[0]]['user_answer'] == a:
            # Επιλέγει το radio με την απάντηση του παίκτη από προηγούμενη εμφάνιση
            answer.set(a)
        radios.append(radio_button)
    return


# Ελέγχει όλες τις απαντήσεις του παίκτη. Αν ισχύουν οι προυποθέσεις του δίνει τη δυνατότητα να παίξει ξανά
# διαφορετικά περνάει στα αποτελέσματα του παιχνιδιού στη show_game_score για να εμφανίσει το score του παιχνιδιού
def check_answers(qa, frame_play, frame_top, frame_bottom, frame_game_score, frame_user_data, frame_hi_scores, second,
                  params, username, category, btn_start):
    global game_number
    global game_score
    global game_duration
    # counter_label(lbl, False)
    score = 0
    difficulty = 1
    not_answered = 1
    # Ορίζω ένα λεξικό το οποίο θα περιέχει όλα τα αποτελέσματα του παιχνιδιού
    gs = {'name': '', 'category': '', 'difficulty': 0, 'score': 0, 'correct': 0, 'wrong': 0, 'not_answered': 0,
          'time': 0}
    game_score.append(gs)
    game_score[game_number]['time'] = game_duration - int(second.get())
    game_score[game_number]['name'] = username
    game_score[game_number]['difficulty'] = params['difficulty']
    game_score[game_number]['category'] = category
    for que in range(0, len(qa)):
        # Μετράει τις μη απαντημένες ερωτήσεις
        if len(qa[que]['user_answer']) == 0:
            game_score[game_number]['not_answered'] += 1
        # τις σωστές και τις λάθος
        if qa[que]['correct_answer'] == qa[que]['user_answer']:
            # αν η απάντηση είναι σωστή, προσθέτει στο score το γινόμενο: βαθμός Δυσκολίας * χρόνος απάντησης
            # βέβαια, περίμενε κανείς ότι ο χρόνος απάντησης θα ήταν αντιστρόφως ανάλογος της βαθμολογίας
            game_score[game_number]['score'] += difficulty * qa[que]['time_to_answer']
            game_score[game_number]['correct'] += 1
        else:
            game_score[game_number]['wrong'] += 1
    # Αν ο υπολειπόμενος χρόνος είναι > 0 θα πρέπει να ελέγξει αν έχει απαντήσει τουλάχιστον 6 ερωτήσεις τις 2 τελ. φορές
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
            # αν επιλέξει να παίξει ένα επόμενο set, καλείται η play και επαναλαμβάνεται όλη η εκτέλεση
            if answer:
                play(frame_play, frame_top, frame_bottom, frame_game_score, frame_user_data, frame_hi_scores, params,
                     username, category, btn_start)
                game_end = False
    # αν επιλέξει να μη συνεχίσει με επόμενο set
    if game_end:
        # Κάνει hidden το play_frame
        frame_play.place_forget()
        # και εμφανίζει το frame για να την εμφάνιση της βαθμολογίας
        frame_game_score.place(y=100, height=768 - 160, width=1024)
        show_game_score(frame_game_score, game_score, frame_hi_scores, btn_start)
        game_score.clear()
        game_number = 0
        # Καταστρέφει όλα τα widgets του top frame (Χρόνος, κατηγορία, δυσκολία κλπ)
        for widgets in frame_top.winfo_children():
            widgets.destroy()
        frame_bottom.nametowidget("btn_end_game").destroy()
        frame_bottom.nametowidget("btn_next").destroy()
        frame_bottom.nametowidget("btn_prev").destroy()
        frame_bottom.nametowidget("btn_first").destroy()
        frame_bottom.nametowidget("btn_last").destroy()


# Σταματάει το countdown του χρόνου του παιχνιδιού
def stop_countdown():
    global stop_threads
    stop_threads = True


# Με αυτή τη συνάρτηση υλοποιώ το countdown time του παιχνιδιού. Αν τελειώσει ο χρόνο καλεί την check_answers
# Η συνάρτηση αυτή εκτελείται σε άλλο thread γιατί διαφορετικά κολλάει η εκτέλεση μέχρι να τελειώσει ο χρόνος
def countdown(second, qa, frame_play, frame_top, frame_bottom, frame_game_score, frame_user_data, frame_hi_scores,
              params, username, category, btn_start):
    global stop_threads
    temp = int(second.get())
    while temp > -1:
        secs = temp
        second.set("{0:3d}".format(secs))
        time.sleep(1)
        # Αν τελειώσει ο χρόνος των 180sec, καλείται η check_answer για να γίνει ο έλεγχος του score και ο
        # υπολογισμός της βαθμολογίας
        if temp == 0:
            messagebox.showinfo("Τέλος", "Η χρόνος έληξε! ")
            check_answers(qa, frame_play, frame_top, frame_bottom, frame_game_score, frame_user_data, frame_hi_scores,
                          second, params, username, category, btn_start)
        if stop_threads:
            break
        # Μετά από κάθε δευτερόλεπτο μειώνει την temp κατά ένα
        temp -= 1


# Η εκκίνηση του παιχνιδιού γίνεται από αυτή τη συνάρτηση. Φέρνει τις ερωτήσεις, τις προετοιμάζει, φτιάχνει τα buttons
# στο bottom frame
def play(parent, frame_top, frame_bottom, frame_game_score, frame_user_data, frame_hi_scores, params, username,
         category, btn_start):
    global stop_threads
    stop_threads = False
    # Καλεί την get_questions με παραμέτρους το url, την επιλεγμένη από τον παίχτη κατηγορία και το επίπεδο δυσκολίας
    # Η επιλογή του παίκτη "difficulty=Easy, Category=Musical and Theater" δε φέρνει ερωτήσεις από την opentdb.
    # Σε αυτή την περίπτωση αλλάζω τον βαθμό δυσκολίας μέχρι να φέρει ερωτήσεις
    while True:
        jsondata = get_questions(url, params)
        qa = jsondata['results']
        if len(qa) == 0:
            if params['difficulty'] == 'easy':
                params['difficulty'] = 'medium'
            if params['difficulty'] == 'medium':
                params['difficulty'] = 'hard'
            if params['difficulty'] == 'hard':
                params['difficulty'] = 'medium'
            messagebox.showwarning(title='Change selection', message='There are no questions in the selected category '
                                                                     'and level. Difficulty is changed to ' + params[
                                                                         'difficulty'])
        else:
            break
    # κάνει hidden το frame που έγινε η εισαγωγή των στοιχείων του παίκτη
    frame_user_data.place_forget()
    # σταματάω οποιαδήποτε άλλη μουσική παίζει
    pygame.mixer.music.stop()
    #  αρχικοποίηση του mixer module
    pygame.mixer.init()
    #  φορτώνω τη μουσική
    pygame.mixer.music.load("play.mp3")
    # και του λεω ποιες φορές να παίξει το αρχείο της μουσικής
    pygame.mixer.music.play(loops=4)

    parent.place(y=100, height=768 - 160, width=1024)
    second = StringVar()
    second.set("180")
    tk.Label(frame_top, font=("Arial", 8, ""), bg='lightgray',
             text='Category: ' + category + ', Difficulty:' + params['difficulty']).place(x=10, y=75)
    tk.Label(frame_top, font=("Arial", 12, ""), bg='lightgray', text='Time to answer:').place(x=10, y=20)
    tk.Label(frame_top, font=("Arial", 8, ""), bg='lightgray', text='(1/100 sec)').place(x=10, y=40)
    tk.Label(frame_top, font=("Arial", 14, ""), bg='lightgray', text='Time left:').place(x=870, y=20)
    # Φτιάχνω ένα label που εμφανίζει το χρόνο που έχει απομείνει
    seconds = tk.Label(frame_top, width=3, font=("Arial", 14, ""), bg='lightgray', fg='red', textvariable=second)
    seconds.place(x=950, y=20)
    # Καλώ τη συνάρτηση countdown που μετράει το χρόνο που απομένει μέχρι το τέλος του παιχνιδιού
    # Η συνάρτηση καλείται σε διαφορετικό thread. Αν την καλέσω στο ίδιο thread σταματάει η εκτέλεση του υπόλοιπου
    # προγράμματος μέχρι να περάσουν τα 180sec και συνεχίζει μετά.
    t = threading.Thread(
        target=lambda: countdown(second, qa, parent, frame_top, frame_bottom, frame_game_score, frame_user_data,
                                 frame_hi_scores, params, username, category, btn_start))
    t.daemon = True
    t.start()

    # Η παρακάτω εντολή ανακατεύει τη σειρά των ερωτήσεων
    random.shuffle(qa)
    # φτιάχνει 4 κλειδιά στο λεξικό κάθε ερώτησης, όλες τις απαντήσεις, την απάντηση του παίκτη, το χρόνο εμφάνισης κάθε
    # ερώτησης και το χρόνο απάντησης με τιμή 0
    for q in qa:
        # εδώ αντικαθιστώ τα &quot; με ", το &#039; με ', το amp; με &, το &/divide με /, &lt; με <, &gt; με > στις
        # ερωτήσεις και απαντήσεις
        q['question'] = (q['question'].replace("&lt;", "<")).replace("&gt;", ">")
        q['question'] = (q['question'].replace("&iacute;", "E")).replace("&ndash;", "-")
        q['question'] = (((((q['question'].replace('&quot;', '"')).replace("&#039;", "'")).replace("&amp;",
                                                                                                   "&")).replace(
            "&ivide;", "/")).replace("&rsquo;", "'")).replace("&eacute;", "e")
        q['correct_answer'] = (q['correct_answer'].replace("&lt;", "<")).replace("&gt;", ">")
        q['correct_answer'] = (q['correct_answer'].replace("&iacute;", "<")).replace("&ndash;", ">")
        q['correct_answer'] = (((((q['correct_answer'].replace('&quot;', '"')).replace("&#039;", "'")).replace("&amp;",
                                                                                                               "&")).replace(
            "&ivide;", "/")).replace("&rsquo;", "/")).replace("&eacute;", "e")
        for i in range(0, len(q['incorrect_answers'])):
            q['incorrect_answers'][i] = (q['incorrect_answers'][i].replace("&lt;", "<")).replace("&gt;", ">")
            q['incorrect_answers'][i] = (q['incorrect_answers'][i].replace("&iacute;", "<")).replace("&ndash;", ">")
            q['incorrect_answers'][i] = (((((q['incorrect_answers'][i].replace('&quot;', '"')).replace("&#039;",
                                                                                                       "'")).replace(
                "&amp;", "&")).replace("&ivide;", "/")).replace("&rsquo;", "/")).replace("&eacute;", "e")

        # καταχωρεί τη σωστή και τις λανθασμένες απαντήσεις κάθε ερώτησης στη λίστα answers
        answers = [q['correct_answer'], *q['incorrect_answers']]
        # ανακατεύει τις απαντήσεις
        random.shuffle(answers)
        # τις ανακατεμένες απαντήσεις τις καταχωρεί στο λεξικό κάθε ερώτησης
        q['all_answers'] = answers
        q['user_answer'] = ''
        q['viewing_time'] = 0
        q['time_to_answer'] = 0

    # Η τρέχουσα ερώτηση (current_que) ορίζεται σαν λίστα για να μπορεί να αλλάξει τιμή μέσα από άλλη συνάρτηση
    current_que = [0]
    # καλεί τη show_question με παράμετρο τη current_que ώστε να εμφανίσει τη 1η ερώτηση στον παίκτη
    show_question(parent, qa, current_que, frame_top)
    # Παρακάτω, φτιάχνω τα buttons που βρίσκονται στο bottom frame τα οποία είναι:
    # Ολοκλήρωση παιχνιδιού, επόμενη, προηγούμενη, 1η και τελευταία ερώτηση
    # Χρησιμοποιώ lambda συναρτήσεις γιατί στο button "ολοκλήρωση παιχνιδιού" θα πρέπει πρώτα να καλέσω τη
    # stop_countdown ώστε να σταματήσει το thread με τη μέτρηση του χρόνου. Στις υπόλοιπες είναι απαραίτητο επειδή
    # καλώ με πολλά ορίσματα τις συναρτήσεις στο onclick event
    ttk.Button(frame_bottom, text="End Game", name='btn_end_game',
               command=lambda: [stop_countdown(),
                                check_answers(qa, parent, frame_top, frame_bottom, frame_game_score,
                                              frame_user_data, frame_hi_scores, second, params, username, category,
                                              btn_start)]).place(x=150, y=20)
    ttk.Button(frame_bottom, text=">", name='btn_next',
               command=lambda: next_question(parent, qa, current_que, frame_top)).place(x=550, y=20)
    ttk.Button(frame_bottom, text="<", name='btn_prev',
               command=lambda: prev_question(parent, qa, current_que, frame_top)).place(x=450, y=20)
    ttk.Button(frame_bottom, text="<<", name='btn_first',
               command=lambda: first_question(parent, qa, current_que, frame_top)).place(x=350, y=20)
    ttk.Button(frame_bottom, text=">>", name='btn_last',
               command=lambda: last_question(parent, qa, current_que, frame_top)).place(x=650, y=20)
