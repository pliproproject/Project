import requests


def get_questions(url, params):
    # Εκτελεί την αίτηση GET προς τον δικτυακό τόπο opentdb.com
    resp = requests.get(url=url, params=params)
    # Επιστρέφει την απάντηση της αίτησης (request) σε μορφή dict
    data = resp.json()

    print(data['results'])
    #  play(qa, frame_play, frame_top, frame_bottom, frame_game_score)
    #  return data['results']
    return data
