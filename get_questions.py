from tkinter import ttk


def get_questions(category, difficulty):
    qa = [
        {"question": "Which company was established on April 1st, 1976 by Steve Jobs, Steve Wozniak and Ronald Wayne?",
         "correct_answer": "Apple", "incorrect_answers": ["Microsoft", "Atari", "Commodore"]},
        {"question": "In any programming language, what is the most common way to iterate through an array?",
         "correct_answer": "&#039;For&#039; loops",
         "incorrect_answers": ["&#039;If&#039; Statements", "&#039;Do-while&#039; loops", "&#039;While&#039; loops"]},
        {"question": "According to the International System of Units, how many bytes are in a kilobyte of RAM?",
         "correct_answer": "1000", "incorrect_answers": ["512", "1024", "500"]},
        {"question": "When Gmail first launched, how much storage did it provide for your email?",
         "correct_answer": "1GB",
         "incorrect_answers": ["512MB", "5GB", "Unlimited"]},
        {"question": "In the programming language Java, which of these keywords would you put on a variable to "
                     "make sure it does&#039;t get modified?", "correct_answer": "Final",
         "incorrect_answers": ["Static", "Private", "Public"]},
        {"question": "The logo for Snapchat is a Bell.", "correct_answer": "False", "incorrect_answers": ["True"]},
        {"question": "RAM stands for Random Access Memory.", "correct_answer": "True", "incorrect_answers": ["False"]},
        {"question": "Time on Computers is measured via the EPOX System.", "correct_answer": "False",
         "incorrect_answers": ["True"]},
        {"question": "The NVidia GTX 1080 gets its name because it can only render at a 1920x1080 screen resolution.",
         "correct_answer": "False", "incorrect_answers": ["True"]}]
    return qa


def get_user_data(parent):
    player = 'Player'
    lbl_player = ttk.Label(parent, text='get user name, category, difficulty frame', font='Arial 12 bold')
    lbl_player.place(x=10, y=10)
    category = 'category 1'
    difficulty = 'difficulty 1'
    return [player, category, difficulty]
