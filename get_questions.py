import requests
def get_questions(url,params):

    qa = [
        {"question": "Which company was established on April 1st, 1976 by Steve Jobs, Steve Wozniak and Ronald Wayne?",
         "correct_answer": "Apple", "incorrect_answers": ["Microsoft", "Atari", "Commodore"]},
        {"question": "In any programming language, what is the most common way to iterate through an array?",
         "correct_answer": "For loops",
         "incorrect_answers": ["If Statements", "Do-while loops", "While loops"]},
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
    #Εκτελεί την αίτηση GET προς τον δικτυακό τόπο opentdb.com
    resp = requests.get(url=url, params=params)
    #Επιστρέφει την απάντηση της αίτησης (request) σε μορφή dict
    data = resp.json()

    print(data['results'])
  #  play(qa, frame_play, frame_top, frame_bottom, frame_game_score)
  #  return data['results']
    return data

