import sqlite3
import uuid
from bottle import response, request

DATABASE_NAME = 'likes_db.db'

def create_tables(db):
    """Create and initialise the database tables
    This will have the effect of overwriting any existing
    data."""

    cursor = db.cursor()

    # Drop the tables
    sql = """DROP TABLE IF EXISTS likes"""
    cursor.execute(sql)

    # Drop the tables
    sql = """    DROP TABLE IF EXISTS sessions"""
    cursor.execute(sql)


    # Create the tables
    sql = """CREATE TABLE likes (
        thing text,
        key text
    );
    """
    cursor.execute(sql)

    # Create the tables
    sql = """CREATE TABLE sessions (
        key text UNIQUE PRIMARY KEY
    );
    """
    cursor.execute(sql)

    db.commit()


def new_session(db):
    """Create a new session using cookies. Return the key of the cookie."""
    key = str(uuid.uuid4())

    cursor = db.cursor()

    cursor.execute("INSERT INTO sessions VALUES (?)", (key ,))

    db.commit()

    response.set_cookie('COOKIE_NAME', key)

    return key


def get_session(db,  key):
    """Get current session key from DB. If none, create a new key"""

    sql = """SELECT key FROM sessions WHERE key=(?)"""

    cursor = db.cursor()

    cursor.execute(sql, (key, ))

    row = cursor.fetchone()
    if not row:
        key = new_session(db)

    return key


def store_like(db, like, key):
    """Store a new like into the database"""

    if not like:
        return

    cursor = db.cursor()

    sql = """INSERT INTO likes (thing, key) VALUES (?,?)"""

    cursor.execute(sql, (like, key))
    db.commit()


def get_likes(db, key):
    """Returns a list of all the likes stored in the database"""
    likeslist = []

    cursor = db.cursor()

    sql = """SELECT thing FROM likes WHERE key=?"""

    cursor.execute(sql, (key, ))

    for row in cursor:
        likeslist.append(row[0])

    return likeslist


def delete_like(db, dlike):
    """Deletes checked likes from the database"""
    cursor = db.cursor()

    print("deleting")

    sql = """DELETE FROM likes WHERE thing=?"""

    cursor.execute(sql, (dlike ,))

    db.commit()

if __name__ == '__main__':
    #if we call this script directly, create the database and make sample data
    db = sqlite3.connect(DATABASE_NAME)
    create_tables(db)