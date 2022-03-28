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
from multiprocessing import Process

appname = "doYouKnow?"


def submit(parent, hour, minute, second):
    try:
        # the input provided by the user is
        # stored in here :temp
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
    except:
        print("Please input the right value")
    while temp > -1:

        # divmod(firstvalue = temp//60, secondvalue = temp%60)
        mins, secs = divmod(temp, 60)

        # Converting the input entered in mins or secs to hours,
        # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
        # 50min: 0sec)
        hours = 0
        if mins > 60:
            # divmod(firstvalue = temp//60, secondvalue
            # = temp%60)
            hours, mins = divmod(mins, 60)

        # using format () method to store the value up to
        # two decimal places
        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))

        # updating the GUI window after decrementing the
        # temp value every time
        parent.update()
        time.sleep(1)

        # when temp value = 0; then a messagebox pop's up
        # with a message:"Time's up"
        if temp == 0:
            messagebox.showinfo("Time Countdown", "Time's up ")

        # after every one sec the value of temp will be decremented
        # by one
        temp -= 1


# ------------------------- frame show/hide functions-----------------------------
def frame_splash_show():
    frame_splash.place(y=100, height=window_height - 160, width=window_width)


def frame_splash_hide():
    frame_splash.place_forget()


def frame_hi_scores_show():
    frame_hi_scores.place(y=100, height=window_height - 160, width=window_width)


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


def frame_game_score_hide():
    frame_game_score.place_forget()


# ----------------------------------------------------------------------------------
def exit_splash():
    frame_splash_hide()
    frame_hi_scores_show()
    show_high_scores(frame_hi_scores)


def start_new_game():
    frame_hi_scores_hide()
    frame_user_data_show()
    userdata = get_user_data(frame_user_data)


def runinparallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def play_game():
    frame_user_data_hide()
    frame_play_show()
    qa = get_questions(1, 1)

    hour = StringVar()
    minute = StringVar()
    second = StringVar()

    hour.set("00")
    minute.set("00")
    second.set("05")

    secondEntry = ttk.Entry(frame_top, width=3, font=("Arial", 18, ""), textvariable=second)
    secondEntry.place(x=180, y=20)
    # play(qa, frame_play, frame_top, frame_bottom)
    runinparallel(play(qa, frame_play, frame_top, frame_bottom), submit(frame_top, hour, minute, second))


def end_game():
    frame_play_hide()
    frame_game_score_show()
    show_game_score(frame_game_score)


def high_scores():
    frame_game_score_hide()
    frame_hi_scores_show()


# ----------------- main --------------------------
if __name__ == '__main__':
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
    frame_top = tk.Frame(root, bg='lightgray')
    frame_top.place(y=1, height=100, width=window_width)
    frame_splash = tk.Frame(root, bg='aliceblue')
    frame_hi_scores = tk.Frame(root, bg='gainsboro')
    frame_user_data = tk.Frame(root, bg='whitesmoke')
    frame_play = tk.Frame(root, bg='white')
    frame_game_score = tk.Frame(root, bg='azure')
    frame_bottom = tk.Frame(root, bg='lightgrey')
    frame_bottom.place(y=708, height=60, width=window_width)
    frame_splash_show()
    # ------------------------------------------------

    # τα παρακάτω labels τα έχω βάλει μόνο για να επιβεβαιώσω ότι αλλάζουν οκ τα frames. Θα τα σβήσουμε
    lbl_splash = ttk.Label(frame_splash, text='splash screen', font='Arial 16 bold')
    lbl_splash.place(x=100, y=30)
    lbl_hi_scores = ttk.Label(frame_hi_scores, text='hi scores', font='Arial 16 bold')
    lbl_hi_scores.place(x=200, y=30)
    #  lbl_play = ttk.Label(frame_play, text='play', font='Arial 16 bold')
    #  lbl_play.place(x=300, y=30)
    lbl_end_game = ttk.Label(frame_game_score, text='game scores', font='Arial 16 bold')
    lbl_end_game.place(x=400, y=30)
    # ---------------------------------------------------------------------------------------------------
    # Έχω βάλει προς το παρόν buttons ια να κάνουμε τις εναλλαγές από τη μια κατάσταση στην άλλη κάποια από αυτά θα
    # φύγουν. Για παράδειγμα, από τη splash screen θα φεύγει μετά από κάποια δευτερόλεπτα ή μετά από click
    btn_exit_splash = ttk.Button(frame_bottom, text="1. exit splash screen", command=exit_splash)
    btn_exit_splash.place(x=5, y=20)

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

    # exit button
    btn_exit = ttk.Button(frame_bottom, text='Exit', command=lambda: root.quit())
    btn_exit.place(x=window_width - 100, y=20)
    # -------------------------------------------------------------------------------------------------------

    root.mainloop()
