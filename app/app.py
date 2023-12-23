# app.py

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import abort,render_template, Flask
import logging
import db

APP = Flask(__name__)


# Connect to the database before executing queries
db.connect()

# Start page
@APP.route('/')
def index():

    stats = {}
    x = db.execute('SELECT COUNT(*) AS g FROM games').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS p FROM players').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS m FROM moves').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS o FROM observers').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS a FROM achievments').fetchone()
    stats.update(x)
    logging.info(stats)

    return render_template('index.html',stats=stats)

@APP.route('/games/')
def list_games():
    games = db.execute(
        '''
        SELECT id_game, rated, victory_status, winner, increment_code, white_id, black_id
        FROM GAMES
        ORDER BY id_game
        ''').fetchall()
    return render_template ('game_list.html',games=games)

