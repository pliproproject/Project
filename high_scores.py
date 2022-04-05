import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import datetime



def open_db_table():
    #δημιουργια της βασης και αν υπαρχει απλα την ανοιγει
    sqliteConnection = sqlite3.connect('Trivia_game.db')

    c = sqliteConnection.cursor()
    # εδω τραβαω απο την βαση για το εαν εχει δημιουργηθει το table highscore
    listOfTables = c.execute(
        """SELECT name FROM sqlite_master WHERE type='table'
        AND name='highscore'; """).fetchall()
    # εδω κοιταω για το εαν ειναι αδεια η λιστα και αν ειναι να δημιουργει το table γιατι αλλιως θα εβγαζε error
    if listOfTables == []:
        #η δημιουργια του table
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

    sqliteConnection.commit()

    sqliteConnection.close()



def insert_high_score(player, category, difficulty, times_he_played, time, correct_answers, wrong_answers, score):
    #εδω τραβαω την σημερινη ημερομηνια αυτοματα
    date = datetime.date.today().strftime('%d/%m/%Y')
    # ανοιγω την βαση και προσθετο τα στοιχεια που πρεπει στο table
    sqliteConnection = sqlite3.connect('Trivia_game.db')
    c = sqliteConnection.cursor()
    with sqliteConnection:
    #    c.execute('''SELECT name FROM highscore WHERE name=?''', (player,))
    #    exists = c.fetchall()
    #    if not exists:
        c.execute("INSERT INTO highscore VALUES (:name, :date, :category, :difficulty, :times_he_played, :time,\
                :correct_answers, :wrong_answers, :score)", {'name': player, 'date': date, 'category': category, 'difficulty': difficulty,
                'times_he_played': times_he_played, 'time': time, 'correct_answers': correct_answers, 'wrong_answers': wrong_answers,  'score': score})

    sqliteConnection.close()


CreateStop_ = 0

def show_high_scores(parent):
    # δημιουργησα το CreateStop ετσι ωστε να τα εμφανιζει μια φορα μονο τα high_scores
    global CreateStop_, tv
    if CreateStop_ < 1:
        CreateStop_ += 1
        # δημιουργω το treeview για εμφανιση των high_scores
        parent.pack(side=tk.LEFT, padx=90)

        tv = ttk.Treeview(parent, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", height="11")
        tv.column("1", anchor=CENTER, width="80", minwidth="60")
        tv.column("2", anchor=CENTER, width="80", minwidth="60")
        tv.column("3", anchor=CENTER, width="80", minwidth="60")
        tv.column("4", anchor=CENTER, width="80", minwidth="60")
        tv.column("5", anchor=CENTER, width="120", minwidth="100")
        tv.column("6", anchor=CENTER, width="60", minwidth="50")
        tv.column("7", anchor=CENTER, width="120", minwidth="100")
        tv.column("8", anchor=CENTER, width="120", minwidth="100")
        tv.column("9", anchor=CENTER, width="80", minwidth="70")

        tv.heading(1, text="Name")
        tv.heading(2, text="Date")
        tv.heading(3, text="Category")
        tv.heading(4, text="Difficulty")
        tv.heading(5, text="Times He Played")
        tv.heading(6, text="Time")
        tv.heading(7, text="Correct Answers")
        tv.heading(8, text="Wrong Answers")
        tv.heading(9, text="Final Score")

        tv.pack()
        # εδω ανοιγω την βαση και τραβαω τα 10 πρωτα σε φθινουσα σειρα highscores
        sqliteConnection = sqlite3.connect('Trivia_game.db')
        c = sqliteConnection.cursor()
        with sqliteConnection:
            c.execute("SELECT * FROM highscore ORDER BY score DESC LIMIT 10")
            items = c.fetchall()
            # και τα παιρναω στο treeview για εμφανιση
        for i in items:
            tv.insert('', 'end', values=i)

            # win.resizable(False, False)

            # και αφου γινουν αυτα που πρεπει ξανα κλεινω την βαση
        sqliteConnection.close()
        return
    else:
        #διαγραφω τα προηγουμενα records για να μην τα τυπωσει διπλα
        for record in tv.get_children():
            tv.delete(record)
        # εδω ανοιγω την βαση και τραβαω τα 10 πρωτα σε φθινουσα σειρα highscores
        sqliteConnection = sqlite3.connect('Trivia_game.db')
        c = sqliteConnection.cursor()
        with sqliteConnection:
            c.execute("SELECT * FROM highscore ORDER BY score DESC LIMIT 10")
            items = c.fetchall()
            # και τα παιρναω στο treeview για εμφανιση
        for i in items:
            tv.insert('', 'end', values=i)

            # win.resizable(False, False)

            # και αφου γινουν αυτα που πρεπει ξανα κλεινω την βαση
        sqliteConnection.close()




#def show_splash_screen(parent):
    #pass

#def show_high_scores(parent):
    #lbl_hi_scores = ttk.Label(parent, text='top ten scorers', font='Arial 14 bold')
    #lbl_hi_scores.place(x=500, y=10)


def show_game_score(parent, c, D, At):
    final_score = 0
    difficulty = []
    # εδω βρισκω το τελικο σκορ του καθε παιχτη
    for i in range(0, 9):
        if D == "easy":
            difficulty.append(1)
        elif D == "medium":
            difficulty.append(2)
        else:
            difficulty.append(3)
        final_score += c[i] * difficulty[i] * At[i]

    # και εδω το τυπωνω στον χρηστη
    lbl_end_game = ttk.Label(parent, text='Game Score', font='Arial 20 bold')
    lbl_end_game.place(x=420, y=30)
    lbl_end_game2 = ttk.Label(parent, text='Your Score is' + " " + str(final_score) + " !!!!!", font='Arial 16 bold')
    lbl_end_game2.place(x=400, y=100)
    return final_score





open_db_table()
