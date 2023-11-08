from boggle import Boggle
boggle_game = Boggle()

from flask import Flask, render_template, session, request, jsonify
app = Flask(__name__)
app.config["SECRET_KEY"] = "pugzydog123"
boggle_game = Boggle()

@app.route('/')
def index():
    """Render new board and display on page."""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)
    return render_template('index.html', board=board, highscore=highscore, num_plays=num_plays)

@app.route('/check-word')
def check_word():
    """check if word is in dictionary"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'resulte': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Extract score, update num_plays, update highscore if record broken"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)

    session["num_plays"] = num_plays + 1
    session["highscore"] = max(score, highscore)
    return jsonify(brokeRecord=score > highscore)