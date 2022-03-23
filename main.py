import tkinter as tk
from tkinter import ttk

appname = "doYouKnow?"


def callback():
    print('demo')
    l2.config(text="test")


# ----------------- main --------------------------
if __name__ == '__main__':
    # create main form
    root = tk.Tk()
    root.title('doYouKnow?')
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
    # transparency
    # root.attributes('-alpha', 0.5)  # transparency
    # root.resizable(False, False)

    # l1 = tk.Label(root, text='Classic Label').pack()
    l2 = ttk.Label(root, text=appname).pack()
    # exit button
    exit_button = ttk.Button(root, text='Exit', command=lambda: root.quit())
    exit_button.pack(ipadx=5, ipady=10, expand=True)

    demo_button = ttk.Button(root, text="Demo Button", command=callback)
    demo_button.pack(ipadx=20, ipady=20, expand=True)

    root.mainloop()
