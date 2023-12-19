DROP DATABASE IF EXISTS aa;
CREATE DATABASE IF NOT EXISTS aa;
USE aa;

DROP TABLE IF EXISTS GAMES, MOVES, PLAYERS, OBSERVERS, OBSGAMES;

CREATE TABLE GAMES
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    rated varchar(5) NOT NULL,
    victory_status varchar(24) NOT NULL,
    winner varchar(5) NOT NULL,
    increment_code varchar(4) NOT NULL,  
    FOREIGN KEY (white_id) REFERENCES PLAYERS(id), 
    FOREIGN KEY (black_id) REFERENCES PLAYERS(id)
);

CREATE TABLE MOVES
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    moves varchar(255) NOT NULL,
    turns INT NOT NULL,
    opening_name varchar(255) NOT NULL,
    opening_ply INT NOT NULL
);

CREATE TABLE PLAYERS
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(24) UNIQUE NOT NULL,
    win_lose varchar(24) NOT NULL,
    t_Points INT NOT NULL,
    member_since varchar(24) NOT NULL,
    time_spent varchar(24) NOT NULL,
    games_made INT NOT NULL,
    country varchar(24),
    puzzles_made INT NOT NULL 
);

CREATE TABLE OBSERVERS
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(24) UNIQUE NOT NULL,
    FOREIGN KEY (id_Player) REFERENCES PLAYERS(id)
);

CREATE TABLE OBSGAMES
(
    id_Game INT NOT NULL,
    id_Observer INT NOT NULL,
    FOREIGN KEY (id_Game) REFERENCES GAMES(id),
    FOREIGN KEY (id_Observer) REFERENCES OBSERVERS(id),
    PRIMARY KEY (id_Game, id_Observer)
);