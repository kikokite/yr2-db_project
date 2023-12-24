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
  
  return render_template('game.html', game = game)



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

@APP.route('/players/search/<expr>/')
def search_player(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  players = db.execute(
      ''' 
      SELECT id_player, name
      FROM PLAYERS 
      WHERE name LIKE ?
      ''', [expr]).fetchall()
  return render_template('players-search.html',
           search=search,players=players)

@APP.route('/moves/')
def list_moves():
    moves=db.execute(
        '''
        SELECT id_game, moves, turns, opening_name, opening_ply
        FROM MOVES
        ORDER BY id_game
        ''').fetchall()
    return render_template ('moves_list.html',moves=moves)

@APP.route('/moves/<int:id>/')
def get_moves(id):
  moves = db.execute(
      '''
      SELECT id_moves, id_game, moves, turns, opening_name, opening_ply
      FROM MOVES
      WHERE id_moves = ?
      ''', [id]).fetchone()
  
  if moves is None:
     abort(404, 'Moves id {} does not exist.'.format(id))

  return render_template('moves.html', moves = moves)

@APP.route('/observers/')
def list_observers():
    observers = db.execute( 
        '''
        SELECT id_Observer,Name,id_Player
        FROM OBSERVERS
        ORDER BY id_Observer

    ''').fetchall()
    return render_template ('observers_list.html',observers=observers)


@APP.route('/observers/<int:id>/')
def get_observers(id):
  observers = db.execute(
      '''
      SELECT id_Observer, Name, id_Player
      FROM OBSERVERS
      WHERE id_Observer = ?
      ''', [id]).fetchone()
  
  if observers is None:
     abort(404, 'Observers id {} does not exist.'.format(id))

  return render_template('observer.html', observers = observers)

@APP.route('/achievments/')
def list_achievments():
   achievments = db.execute(
      '''
      SELECT id_achievment, Name, Description 
      FROM ACHIEVMENTS
      ORDER BY id_Achievment
      ''').fetchall()
   return render_template('achievments_list.html', achievments=achievments)

@APP.route('/achievments/<int:id>/')
def get_achievments(id):
  achievment = db.execute(
      '''
      SELECT id_achievment, Name, Description
      FROM ACHIEVMENTS
      WHERE id_achievment = ?
      ''', [id]).fetchone()
  
  if achievment is None:
     abort(404, 'Achievment id {} does not exist.'.format(id))

  return render_template('achievment.html', achievment = achievment)

@APP.route('/achievments/search/<expr>/')
def search_achievment(expr):
  search = { 'expr': expr }
  achievment = db.execute(
      ' SELECT id_achievment, Description'
      ' FROM ACHIEVMENTS '
      ' WHERE Description LIKE \'%' + expr + '%\''
    ).fetchall()
  return render_template('achievments-search.html',
           search=search,achievment=achievment)