from tkinter import *
from tkinter.ttk import *
import requests

url = "https://opentdb.com/api.php"

username = ""

level = ""

# Πρώτο παράθυρο για λήψη ονόματος παίκτη
window = Tk()

window.title("Username")

window.geometry('200x200')

lbl = Label(window, text="Please type a username:")

lbl.grid(column=0, row=0)

txt = Entry(window, width=10)

txt.grid(column=1, row=0)


def clicked():
    username = txt.get()

    window.destroy()


btn = Button(window, text="Continue", command=clicked)

btn.grid(column=0, row=2)

window.mainloop()

# --------------------------------------------------

# Δεύτερο παράθυρο επιλογής επιπέδου δυσκολίας

window2 = Tk()

window2.title("Select Level")

window2.geometry('200x200')

var = StringVar()

var.set(None)


def selected():
    nlevel = int(var.get())

    if (nlevel == 1):
        level = "easy"
    if (nlevel == 2):
        level = "medium"
    if (nlevel == 3):
        level = "hard"


rad1 = Radiobutton(window2, text='Easy   ', value=1, variable=var, command=selected)

rad2 = Radiobutton(window2, text='Medium', value=2, variable=var, command=selected)

rad3 = Radiobutton(window2, text='Hard   ', value=3, variable=var, command=selected)

rad1.grid(column=1, row=1)

rad2.grid(column=1, row=2)

rad3.grid(column=1, row=3)

var.set(1)


def clicked2():
    window2.destroy()


btn2 = Button(window2, text="Continue", command=clicked2)

btn2.grid(column=1, row=4)

window2.mainloop()

# ------------------------------------------------------------------------

# Τρίτο παράθυρο επιλογής κατηγορίας ερωτήσεων

window3 = Tk()

window3.title("Select Category")

window3.geometry('150x150')

lbl = Label(window3, text="Please select a category:")

lbl.grid(column=0, row=0)

cat = StringVar()
cat_cb = Combobox(window3, textvariable=cat)

# prevent typing a value
cat_cb['state'] = 'readonly'

cat_cb['values'] = ('Any Category',
                    'General Knowledge',
                    'Entertainment: Books',
                    'Entertainment: Film',
                    'Entertainment: Music',
                    'Entertainment: Musicals & Theatres',
                    'Entertainment: Television',
                    'Entertainment: Video Games',
                    'Entertainment: Board Games',
                    'Science & Nature',
                    'Science: Computers',
                    'Science: Mathematics',
                    'Mythology',
                    'Sports',
                    'Geography',
                    'History',
                    'Politics',
                    'Art',
                    'Celebrities',
                    'Animals',
                    'Vehicles',
                    'Entertainment: Comics',
                    'Science: Gadgets',
                    'Entertainment: Japanese Anime & Manga',
                    'Entertainment: Cartoon & Animations')

cat_cb.current(0)
cat_cb.grid(column=0, row=2)


def clicked3():
    if (cat_cb.current() != 0):
        what_category = 8 + cat_cb.current()
    else:
        what_category = "any"

    if (what_category == "any"):
        params = dict(
            amount='9',
            difficulty=level
        )
    else:
        params = dict(
            amount='9',
            category=what_category,
            difficulty=level
        )
    # Εκτελεί την αίτηση GET προς τον δικτυακό τόπο opentdb.com
    resp = requests.get(url=url, params=params)
    # Επιστρέφει την απάντηση της αίτησης (request) σε μορφή dict
    data = resp.json()

    print(data)
    window3.destroy()


btn3 = Button(window3, text="Continue", command=clicked3)

btn3.grid(column=0, row=5)

window3.mainloop()
# -------------------------------------------------------------------------
