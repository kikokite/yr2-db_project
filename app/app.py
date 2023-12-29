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

@APP.route('/games-stats/')
def statistics():
    
   top50_games = db.execute(
      '''
      SELECT m.id_game, g.id_game, g.white_id, g.black_id, o.id_Observer, o.Name, m.turns
      FROM MOVES AS m
      JOIN GAMES g ON m.id_game = g.id_game
      JOIN OBSGAME og ON g.id_game = og.id_Game
      JOIN OBSERVERS o ON og.id_Observer = o.id_observer
      GROUP BY m.turns
      ORDER BY m.turns DESC 
      LIMIT 50
      ''').fetchall()

   return render_template('games-stats.html',top50_games=top50_games)



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
      GROUP BY id_game      
      ''', [id]).fetchone()
  
  if game is None:
     abort(404, 'Game id {} does not exist.'.format(id))

  player1 = db.execute(
     '''
     SELECT id_player, name
     FROM PLAYERS JOIN GAMES  ON id_player = white_id
     WHERE id_game = ?
     ''', [id]).fetchone()
  
  player2 = db.execute(
     '''
     SELECT id_player, name
     FROM PLAYERS JOIN GAMES ON  id_player = black_id
     WHERE id_game = ?
     ''', [id]).fetchone()
  
  observers = db.execute(
     '''
     SELECT o.id_Observer,o.Name
     FROM GAMES AS g 
     JOIN OBSGAME og ON g.id_game = og.id_Game
     JOIN OBSERVERS o ON og.id_Observer = o.id_Observer
     WHERE g.id_Game = ?
     ''', [id]).fetchall()
  
  moves = db.execute(
     '''
     SELECT m.moves, m.id_moves ,g.id_game
     FROM MOVES AS m JOIN GAMES g ON m.id_game = g.id_game
     WHERE g.id_game = ?
     ''', [id]).fetchone()
  
  return render_template('game.html', game = game, player1=player1, player2=player2, observers = observers, moves = moves)



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
      GROUP BY name
      ''', [id]).fetchone()
  
  if player is None:
     abort(404, 'Player id {} does not exist.'.format(id))

  games = db.execute(
     '''
     SELECT id_game 
     FROM GAMES
     WHERE white_id = ? OR black_id = ?
     ORDER BY id_game
     ''', (id,id)).fetchall()
  
  achievments = db.execute(
     '''
     SELECT a.id_achievment, a.Name
     FROM PLAYERS AS p
     JOIN PLAYERACHIEVS AS pa ON p.id_player = pa.id_player
     JOIN ACHIEVMENTS AS a ON pa.id_achievment = a.id_achievment
     WHERE p.id_player = ?
     ''',[id]).fetchall()
    
  observers = db.execute(
     '''
     SELECT id_Observer, id_Player, Name
     FROM OBSERVERS 
     WHERE id_Player = ?
     ''',[id]).fetchall()
  
  return render_template('player.html', player=player, games=games, achievments=achievments, observers=observers)

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

@APP.route('/players-stats/')
def top_player():
   player = db.execute(
      '''
      SELECT p.id_player, p.name AS pname, p.games_made, o.name AS oname, o.id_Observer, COUNT(pa.id_achievment) AS achievements_count
      FROM PLAYERS AS p 
      JOIN OBSERVERS o ON p.id_player = o.id_Player 
      JOIN PLAYERACHIEVS pa ON p.id_player = pa.id_player
      JOIN ACHIEVMENTS a ON a.id_achievment = pa.id_achievment
      GROUP BY p.id_player
      ORDER BY p.games_made DESC
      LIMIT 50
      ''').fetchall()
   return render_template('player-stats.html', player= player)

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
  
  games = db.execute(
     '''
     SELECT g.id_game, o.Name
     FROM GAMES AS g 
     JOIN OBSGAME og ON g.id_game = og.id_Game
     JOIN OBSERVERS o ON og.id_Observer = o.id_Observer
     WHERE o.id_Observer = ?
     ''', [id]).fetchall()
  
  if observers is None:
     abort(404, 'Observers id {} does not exist.'.format(id))

  return render_template('observer.html', observers = observers, games = games)

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
  
  players = db.execute(
     '''
     SELECT p.id_player, p.name
     FROM PLAYERS AS p
     JOIN PLAYERACHIEVS AS pa ON p.id_player = pa.id_player
     JOIN ACHIEVMENTS AS a ON pa.id_achievment = a.id_achievment
     WHERE a.id_achievment = ?
     ''', [id]).fetchall()
  
  if achievment is None:
     abort(404, 'Achievment id {} does not exist.'.format(id))

  return render_template('achievment.html', achievment = achievment, players = players)

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