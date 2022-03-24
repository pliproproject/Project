from tkinter import ttk


def show_splash_screen(parent):
    lbl_splash = ttk.Label(parent, text='splash screen', font='Arial 16 bold')
    lbl_splash.place(x=100, y=30)

#    lbl_splash.after(2000, lbl_splash.destroy)


def show_high_scores(parent):
    lbl_hi_scores = ttk.Label(parent, text='top ten scorers', font='Arial 14 bold')
    lbl_hi_scores.place(x=500, y=30)
