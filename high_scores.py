import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import datetime
from PIL import Image, ImageTk, ImageSequence
import time
import pygame
from threading import Timer


def open_db_table():
    # δημιουργια της βασης και αν υπαρχει απλα την ανοιγει
    sqlite_connection = sqlite3.connect('Trivia_game.db')

    c = sqlite_connection.cursor()
    # εδω τραβαω απο την βαση για το εαν εχει δημιουργηθει το table high score
    list_of_tables = c.execute(
        """SELECT name FROM sqlite_master WHERE type='table'
        AND name='highscore'; """).fetchall()
    # εδω κοιταω για το εαν ειναι αδεια η λιστα και αν ειναι να δημιουργει το table γιατι αλλιως θα εβγαζε error
    if not list_of_tables:
        # η δημιουργια του table
        c.execute("""CREATE TABLE highscore(
                name text,
                date text,
                category text,
                difficulty text,
                times_he_played integer,
                time integer,
                correct_answers integer,
                wrong_answers integer,
                score integer
                )""")

    sqlite_connection.commit()

    sqlite_connection.close()


def insert_high_score(player, category, difficulty, times_he_played, time, correct_answers, wrong_answers, score):
    # εδω τραβαω την σημερινη ημερομηνια αυτοματα
    date = datetime.date.today().strftime('%d/%m/%Y')

    # ανοιγω την βαση και προσθετο τα στοιχεια που πρεπει στο table
    sqlite_connection = sqlite3.connect('Trivia_game.db')
    c = sqlite_connection.cursor()
    with sqlite_connection:
        #    c.execute('''SELECT name FROM highscore WHERE name=?''', (player,))
        #    exists = c.fetchall()
        #    if not exists:
        c.execute("INSERT INTO highscore VALUES (:name, :date, :category, :difficulty, :times_he_played, :time,\
                :correct_answers, :wrong_answers, :score)", {'name': player, 'date': date, 'category': category,
                                                             'difficulty': difficulty,
                                                             'times_he_played': times_he_played, 'time': time,
                                                             'correct_answers': correct_answers,
                                                             'wrong_answers': wrong_answers, 'score': score})

    sqlite_connection.close()


CreateStop_ = True


def show_high_scores(parent):
    # δημιουργησα το CreateStop ετσι ωστε να τα εμφανιζει μια φορα μονο τα high_scores
    global CreateStop_, table
    if CreateStop_:
        CreateStop_ = False

        # προσθηκη εικονας top 10 high scores στο frame
        top_ten_imag = ImageTk.PhotoImage(Image.open("top_ten_high_score1.png"))
        lbl_top_ten = Label(parent, image=top_ten_imag, borderwidth=0)
        lbl_top_ten.image = top_ten_imag
        lbl_top_ten.place(x=195, y=50)

        # δημιουργω το tree view για εμφανιση των high_scores
        table = ttk.Treeview(parent, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", height="10")
        table.column("1", anchor=CENTER, width="80", minwidth="60")
        table.column("2", anchor=CENTER, width="80", minwidth="60")
        table.column("3", anchor=CENTER, width="80", minwidth="60")
        table.column("4", anchor=CENTER, width="80", minwidth="60")
        table.column("5", anchor=CENTER, width="120", minwidth="100")
        table.column("6", anchor=CENTER, width="60", minwidth="50")
        table.column("7", anchor=CENTER, width="120", minwidth="100")
        table.column("8", anchor=CENTER, width="120", minwidth="100")
        table.column("9", anchor=CENTER, width="80", minwidth="70")

        table.heading(1, text="Name")
        table.heading(2, text="Date")
        table.heading(3, text="Category")
        table.heading(4, text="Difficulty")
        table.heading(5, text="Times He Played")
        table.heading(6, text="Time")
        table.heading(7, text="Correct Answers")
        table.heading(8, text="Wrong Answers")
        table.heading(9, text="Final Score")

        table.pack(side=tk.LEFT, padx=90)
        # εδω ανοιγω την βαση και τραβαω τα 10 πρωτα σε φθινουσα σειρα high scores
        sqlite_connection = sqlite3.connect('Trivia_game.db')
        c = sqlite_connection.cursor()
        with sqlite_connection:
            c.execute("SELECT * FROM highscore ORDER BY score DESC LIMIT 10")
            items = c.fetchall()
            # και τα παιρναω στο tree view για εμφανιση
        for i in items:
            table.insert('', 'end', values=i)

            # win.resizable(False, False)

            # και αφου γινουν αυτα που πρεπει κλεινω την βαση
        sqlite_connection.close()
        return
    else:
        # διαγραφω τα προηγουμενα records για να μην τα τυπωσει διπλα
        for record in table.get_children():
            table.delete(record)
        # εδω ανοιγω την βαση και τραβαω τα 10 πρωτα σε φθινουσα σειρα high scores
        sqlite_connection = sqlite3.connect('Trivia_game.db')
        c = sqlite_connection.cursor()
        with sqlite_connection:
            c.execute("SELECT * FROM highscore ORDER BY score DESC LIMIT 10")
            items = c.fetchall()
        # και τα παιρναω στο tree view για εμφανιση
        for i in items:
            table.insert('', 'end', values=i)

        # win.resizable(False, False)

        # και αφου γινουν αυτα που πρεπει κλεινω την βαση
        sqlite_connection.close()


def show_splash_screen(parent):
    #  αρχικοποιηση του mixer module
    pygame.mixer.init()
    #  φορτωνω την μουσικη
    pygame.mixer.music.load("splash_screen.mp3")

    # προσθετω την εικονα του splash screen
    splash_root_imag = ImageTk.PhotoImage(Image.open("splash_screen_image.png"))
    lbl_splash_root = Label(parent, image=splash_root_imag, borderwidth=0)
    lbl_splash_root.image = splash_root_imag
    lbl_splash_root.pack()

    # και του λεω ποσες φορες να παιξει το αρχειο της μουσικης
    pygame.mixer.music.play(loops=0)


def show_game_score(parent, game_score, frame_hi_scores, btn_start):
    # σταματαω οποιαδηποτε αλλη μουσικη παιζει
    pygame.mixer.music.stop()
    # εδω κοιταω για το ποσες φορες εχει παιξει ο παιχτης και αναλογος βγαζω το αποτελεσμα για το καθενα
    game_number = len(game_score)
    score_is = 0
    wrong_is = 0
    correct_is = 0
    time_is = 0
    if game_number < 1:
        score_is = game_score[game_number]['score']
        wrong_is = game_score[game_number]['wrong']
        correct_is = game_score[game_number]['correct']
        time_is = game_score[game_number]['time']
    else:
        for number in range(0, game_number):
            score_is += game_score[number]['score']
            wrong_is += game_score[number]['wrong']
            correct_is += game_score[number]['correct']
            time_is += game_score[number]['time']

    # ανοιγω την βαση και τραβαω τα 10 πρωτα με ταξινομηση με βαση το score
    sqlite_connection = sqlite3.connect('Trivia_game.db')
    c = sqlite_connection.cursor()
    with sqlite_connection:
        c.execute("SELECT * FROM highscore ORDER BY score DESC LIMIT 10")
        items = c.fetchall()

    # εδω κοιταω για το εαν εκανε high score ο παιχτης
    count = 0
    if not items:
        count += 1
    for score in items:
        if score_is > score[8] or len(items) <= 9:
            count += 1

    # κλεινω την βαση
    sqlite_connection.close()

    #  αρχικοποιηση του mixer module
    pygame.mixer.init()
    #  φορτωνω την μουσικη
    pygame.mixer.music.load("high_score.mp3")
    # και του λεω ποσες φορες να παιξει το αρχειο της μουσικης
    pygame.mixer.music.play(loops=3)

    # αν εκανε high score τυπωνω το αναλογο μυνημα
    if count > 0:
        lbl_end_game3 = ttk.Label(parent, text='CONGRATULATIONS ACHIEVEMENTS HIGH SCORE !!! WELL DONE !!!!' + "\N{trophy}" +
                                               "\N{trophy}", font='Arial 20 bold')
        lbl_end_game3.place(x=15, y=150)

    # και εδω τυπωνω το score του παιχτη
    lbl_end_game = ttk.Label(parent, text='Game Score', font='Arial 20 bold')
    lbl_end_game.place(x=390, y=30)
    lbl_end_game2 = ttk.Label(parent, text='Your Score is' + " " + str(score_is) + " !!!!!", font='Arial 16 bold')
    lbl_end_game2.place(x=370, y=100)

    # προσθηκη εικονας στο frame game score
    if count == 0:
        game_score_imag = ImageTk.PhotoImage(Image.open("frame_game_score_image2.png"))
        lbl_game_score = Label(parent, image=game_score_imag, borderwidth=0)
        lbl_game_score.image = game_score_imag
        lbl_game_score.place(x=270, y=200)

    # εδω τα εισαγω στην βαση
    insert_high_score(game_score[0]['name'], game_score[0]['category'], game_score[0]['difficulty'], game_number,
                      time_is, correct_is, wrong_is, score_is)

    if count > 0:
        play_gif(parent, 250, 200)
        #  βγαινω απο το frame του game score και παω στα high scores
        parent.place_forget()
        frame_hi_scores.place(y=100, height=768 - 160, width=1024)
        show_high_scores(frame_hi_scores)
    elif count == 0:
        #  μετα απο 5 δευτερολεπτα  εκτελειται η συναρτηση
        t = Timer(5, lambda: time_sleep(parent, frame_hi_scores))
        t.start()

    # καταστρεφω το label γιατι αν παιξει ο χρηστης και κανει high score και μετα δεν κανει παραμενε το label
    if count > 0:
        lbl_end_game3.place_forget()
    elif count == 0:
        #  μετα απο 5 δευτερολεπτα  εκτελειται η συναρτηση
        t = Timer(5, lambda: hide_image(lbl_game_score))
        t.start()

    #  μηδενιζω τον counter του time_sleep() γιατι ειναι αναδρομη και αλλιως θα εβγαινε κατευθειαν απο την συναρτηση
    #  αν εμπαινε δευτερη φορα στην συναρτηση
    global counteR
    counteR = 0
    btn_start["state"] = "NORMAL"


def hide_image(lbl_game_score):
    # καταστρεφω το label γιατι αν παιξει ο χρηστης και δεν κανει high score και μετα κανει παραμενε το label
    lbl_game_score.place_forget()


def time_sleep(parent, frame_hi_scores):
    #  βγαινω απο το frame του game score και παω στα high scores
    parent.place_forget()
    frame_hi_scores.place(y=100, height=768 - 160, width=1024)
    show_high_scores(frame_hi_scores)


counteR = 0


def play_gif(parent, x, y):
    global counteR

    # τερματισμος της αναδρομης
    if counteR > 100:
        return

    # ανοιγω την gif εικονα
    img = Image.open("fireworkds5.gif")

    # δημιουργω το label που θα μπει η εικονα
    lbl = Label(parent)
    # τοποθετω το label στο χωρο του frame
    lbl.place(x=x, y=y)
    #  και εδω σπαω την εικονα σε πολλες για να δωσω την αισθηση της κινησης προβαλοντας τες την μια μετα της αλλη
    for img in ImageSequence.Iterator(img):
        img = ImageTk.PhotoImage(img)
        # παιρναω την εικονα στο label
        lbl.config(image=img)
        counteR += 1

        #  και κανω update το frame για να φανει η επομενη εικονα
        parent.update()
        #  χρονος αναμονης για να παει στην επομενη εικονα
        time.sleep(0.01)
        #  το frame αμεσως μετα ξανα καλει την αναδρομικη συναρτηση
    parent.after(0, play_gif(parent, x, y))


# δημιουργεια η ανοιγμα της βασης
open_db_table()
