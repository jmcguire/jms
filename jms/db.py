from flask import g
from jms import app
import sqlite3

__all__ = ['get_db', 'init_if_empty', 'close_db']

# connect to db

def get_db():
  """return the db connection, create it if it doesn't exist yet"""
  db = getattr(g, 'db', None)
  if db is None:
    db = g.db = sqlite3.connect('sqlite3.db')
    db.row_factory = sqlite3.Row
  return db

def init_if_empty(force=False):
  """if the database is empty, initialize it"""
  db = get_db()
  cursor = db.cursor()
  cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='posts';")
  row = cursor.fetchone()
  cursor.close()
  if force or row[0] == 0:
    print "database is empty, initializing it..."
    with open(app.config['DB_INIT'], 'r') as f:
      try:
        db.executescript(f.read())
      except:
        print "...failed to initialize database"
        db.rollback()
        raise
      else:
        print "...success!"
        db.commit()
  else:
    print "using existing database"


@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'db'):
    g.db.close()

