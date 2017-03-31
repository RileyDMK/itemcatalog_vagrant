-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players ( id SERIAL,
                       name TEXT,
                       CONSTRAINT standings_pk PRIMARY KEY (id));

CREATE TABLE matches ( match_id SERIAL,
                       winner_id INT REFERENCES players(id),
                       loser_id INT REFERENCES players(id),
                       CONSTRAINT matches_pk PRIMARY KEY (match_id));
