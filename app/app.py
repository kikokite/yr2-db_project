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


@APP.route('/games/<int:id>/')
def get_game(id):
  game = db.execute(
      '''
      SELECT id_game, rated, victory_status, winner, increment_code, white_id, black_id
      FROM GAMES 
      WHERE id_game = ?
      ''', [id]).fetchone()
  
  if game is None:
     abort(404, 'Game id {} does not exist.'.format(id))

  players = db.execute(
     '''
     SELECT id_game, moves, turns, opening_ply, opening_name
     FROM GAMES NATURAL JOIN MOVES
     WHERE id_game = ? 
     ''', [id]).fetchone()
  
  return render_template('game.html', game = game, players = players)

@APP.route('/players/')
def list_players():
   players = db.execute(
      '''
      SELECT id_player, name, win_losses, t_points, member_since, play_time, games_made, country,puzzles_made
      FROM PLAYERS
      ORDER BY id_player
      ''').fetchall()
   return render_template('players_list.html', players = players)


@APP.route('/players/<int:id>/')
def get_player(id):
  player = db.execute(
      '''
      SELECT id_player, name, win_losses, t_points, member_since, play_time, games_made, country,puzzles_made
      FROM PLAYERS
      WHERE id_player = ?
      ''', [id]).fetchone()
  
  if player is None:
     abort(404, 'Player id {} does not exist.'.format(id))
    
  return render_template('player.html', player=player)


