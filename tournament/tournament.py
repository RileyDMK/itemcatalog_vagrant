#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection.
       The changes to this definition were suggested by a reviewer.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Cannot connect to database!")


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    c.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    c.execute("SELECT count(*) FROM players")
    count = c.fetchone()
    db.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, c = connect()
    query = """
        SELECT players.id AS id,
            players.name AS name,
            (SELECT count(winner_id) FROM matches WHERE winner_id = id) AS wins,
            count(matches.match_id) AS matches
        FROM players
        LEFT JOIN matches
        ON (players.id = matches.winner_id
        OR players.id = matches.loser_id)
        GROUP BY id
        ORDER BY wins DESC
        """
    c.execute(query)
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()
    query = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)"
    param = (winner, loser)
    c.execute(query, param)
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    even_standings = []
    odd_standings = []
    pairings = []

    # This solution is inspired by an answer on the forums.
    # Players at the same index in both lists get paired with eachother.
    for index, val in enumerate(standings):
        if index % 2 == 0:
            even_standings.append(val)
        else:
            odd_standings.append(val)
    for i, j in zip(odd_standings, even_standings):
        row = (i[0], i[1], j[0], j[1])
        pairings.append(row)
    return pairings
