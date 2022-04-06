# Τα παρακάτω που σας γράφω είναι πρόταση. Αν θέλετε τα συζητάμε οκ;

# Νομίζω ότι η πιο εύκολη και αποτελεσματική προσέγγιση είναι να χρησιμοποιήσουμε frames.
# Χώρισα το window σε 3 περιοχές. Η πάνω περιοχή έχει το frame_top στο οποίο θα εμφανίζεται το score, χρόνος
# παιχνιδιού, χρόνος ερώτησης, όνομα παίκτη κλπ
# Στο κάτω (frame_bottom) θα εμφανίζονται τα απαραίτητα buttons ανάλογα με το σημείο που είμαστε
# Το μεσαίο θα εναλλάσσεται ανάλογα σε ποια κατάσταση βρισκόμαστε
# Έβαλα διαφορετικό χρώμα σε κάθε frame για να μας βοηθήσει να μην κάνουμε κανένα λάθος. Θα τα φτιάξουμε αυτά στο τέλος
# frame_splash (όνομα εφαρμογής, τα ονόματα μας κλπ)
# frame_high_scores (top10)
# frame_user_data (φόρμα εισαγωγής ονόματος, κατηγορίας, βαθμού δυσκολίας)
# frame_play (φόρμα παιχνιδιού
# frame_game_score (φόρμα της βαθμολογίας που θα εμφανίζεται με το τέλος του παιχνιδιού)

# για να μπορέσετε να βάλετε controls (labels, entry boxes, combo boxes κλπ) θα πρέπει να έχετε τον parent
# οπότε στην κλήση της συνάρτησης από τη main περνάμε το αντίστοιχο frame σαν παράμετρο

# Έχω βάλει προς το παρόν buttons ια να κάνουμε τις εναλλαγές από τη μια κατάσταση στην άλλη κάποια από αυτά θα
# φύγουν. Για παράδειγμα, από τη splash screen θα φεύγει μετά από κάποια δευτερόλεπτα ή μετά από click

# ---ΝΙΚΟΣ----
# Θα δουλέψει στο get_questions.py
# Το frame που θα χρησιμοποιήσει είναι το frame_user_data
# Θα πρέπει να φτιάξει τη function userdata = get_user_data(frame_user_data)
# που καλεί η main και θα επιστρέφει μια λίστα με το όνομα την κατηγορία και τον βαθμό δυσκολίας
# και τη function qa = get_questions(1, 1) που θα παίρνει σαν όρισμα την κατηγορία και τον βαθμό δυσκολίας
# και θα επιστρέφει ένα λεξικό (μάλλον) με τις ερωτήσεις και τις απαντήσεις

# ---ΣΥΜΕΩΝ----
# θα δουλέψει στο high_scores.py
# Το frame που θα χρησιμοποιήσει είναι το frame_user_data
# Θα φτιάξει τη show_high_scores(frame_hi_scores)
# Επίσης θα φτιάξει τη show_game_score(frame_game_score) στο frame frame_game_score


import tkinter as tk
from tkinter import ttk
from time import sleep
from get_questions import *
from high_scores import *
from play import *

appname = "doYouKnow?"


# ------------------------- frame show/hide functions-----------------------------


def frame_hi_scores_show():
    show_high_scores(frame_hi_scores)


def frame_hi_scores_hide():
    frame_hi_scores.place_forget()


def frame_user_data_show():
    frame_user_data.place(y=100, height=window_height - 160, width=window_width)


def frame_user_data_hide():
    frame_user_data.place_forget()


def frame_play_show():
    frame_play.place(y=100, height=window_height - 160, width=window_width)


def frame_play_hide():
    frame_play.place_forget()


def frame_game_score_show():
    frame_game_score.place(y=100, height=window_height - 160, width=window_width)
    infos = get_user_data(frame_user_data)
    At = [5, 7, 5, 8, 1, 6, 7, 8, 9]
    c = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    show_game_score(frame_game_score, c, infos[2], At)


def frame_game_score_hide():
    frame_game_score.place_forget()


# ----------------------------------------------------------------------------------
def exit_splash():
    frame_hi_scores.place(y=100, height=window_height - 160, width=window_width)
    show_high_scores(frame_hi_scores)


def start_new_game():
    frame_hi_scores_hide()
    frame_user_data_show()
    userdata = get_user_data(frame_user_data)


def play_game():
    frame_user_data_hide()
    frame_play_show()
    qa = get_questions(1, 1)
    play(qa, frame_play, frame_top, frame_bottom)


def end_game():
    frame_play_hide()
    infos = get_user_data(frame_user_data)
    At = [5, 3, 2, 8, 19, 6, 7, 80, 9]
    c = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    finalscore = show_game_score(frame_game_score, c, infos[2], At)
    insert_high_score(infos[0], infos[1], infos[2], 2, 180, 7, 1, finalscore)
    frame_game_score_show()


def high_scores():
    frame_user_data_hide()
    frame_game_score_hide()
    frame_hi_scores_show()


def main_window():
    # καταστροφη του splash screen
    splash_root.destroy()
    # create main form
    root = tk.Tk()
    root.title(appname)
    window_width = 1024
    window_height = 768
    min_width = 200
    max_width = window_width
    min_height = 200
    max_height = window_height
    root.minsize(min_width, min_height)
    root.maxsize(max_width, max_height)
    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # create all frames needed
    global frame_hi_scores, frame_user_data, frame_play, frame_game_score,\
        frame_top, frame_bottom, btn_hi_scores2
    frame_top = tk.Frame(root, bg='lightgray')
    frame_top.place(y=1, height=100, width=window_width)
    frame_hi_scores = tk.Frame(root, bg='gainsboro')
    frame_user_data = tk.Frame(root, bg='whitesmoke')
    frame_play = tk.Frame(root, bg='white')
    frame_game_score = tk.Frame(root, bg='azure')
    frame_bottom = tk.Frame(root, bg='lightgrey')
    frame_bottom.place(y=708, height=60, width=window_width)

    # Έχω βάλει προς το παρόν buttons ια να κάνουμε τις εναλλαγές από τη μια κατάσταση στην άλλη κάποια από αυτά θα
    # φύγουν. Για παράδειγμα, από τη splash screen θα φεύγει μετά από κάποια δευτερόλεπτα ή μετά από click
    # exit button
    btn_exit = ttk.Button(frame_bottom, text='Exit', command=root.destroy)
    btn_exit.place(x=window_width - 100, y=20)
    # start new game button (ask username etc.)
    btn_start = ttk.Button(frame_bottom, text="2. Enter name, category, difficulty", command=start_new_game)
    btn_start.place(x=120, y=20)

    # play button
    btn_play = ttk.Button(frame_bottom, text="3. Start Game", command=play_game)
    btn_play.place(x=310, y=20)

    # game end-score button
    btn_end_game = ttk.Button(frame_bottom, text="4. End Game", command=end_game)
    btn_end_game.place(x=390, y=20)

    # Hi-score button
    btn_hi_scores2 = ttk.Button(frame_bottom, text="5. hi scores", command=high_scores)
    btn_hi_scores2.place(x=470, y=20)
    exit_splash()
    root.mainloop()


# ----------------- main --------------------------
if __name__ == '__main__':
    # splash screen
    splash_root = Tk()
    window_width = 1024
    window_height = 568
    min_width = 200
    max_width = window_width
    min_height = 200
    max_height = window_height
    splash_root.minsize(min_width, min_height)
    splash_root.maxsize(max_width, max_height)
    # get the screen dimension
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    splash_root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    # για να μην εχει τον τιτλο
    splash_root.overrideredirect(True)

    show_splash_screen(splash_root)
    # μετα απο 3 δευτερολεπτα φευγει το splash screen και παει στο κεντρικο παραθυρο
    splash_root.after(3000, main_window)

    # ------------------------------------------------

    splash_root.mainloop()
