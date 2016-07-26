from flask import Flask, g, render_template
import sqlite3

app = Flask(__name__)

# load config

app.config.from_pyfile('config.cfg')

# connect to db

def get_db():
  """return the db connection, create it if it doesn't exist yet"""
  db = getattr(g, 'db', None)
  if db is None:
    db = g._database = sqlite3.connect('sqlite3.db')
    db.row_factory = sqlite3.Row
  return db

def init_if_empty(force=False):
  """if the database is empty, initialize it"""
  db = get_db()
  curr = db.cursor()
  curr.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_name';")
  row = curr.fetchone()
  curr.close()
  if force or row[0] == 0:
    print "database is empty, initializing it..."
    with open(app.config['DB_INIT'], 'r') as f:
      db.executescript(f.read())
      db.commit()

with app.app_context():
  init_if_empty()

# routing

@app.route("/")
def hello():
  return "Hello World: %s\n" % app.config['SITE_NAME']

@app.route("/goodbye")
def goodbye():
  return "goodbye\n"

@app.route("/config/<string:config_var>")
def show_config(config_var):
  return "config_var: %r\n" % app.config[config_var]

@app.route("/post/<int:post_id>")
def show_post(post_id):
  db = get_db()
  curr = db.cursor()
  curr.execute("select * from posts where id = ?", (post_id,))
  row = curr.fetchone()
  return render_template('post.html', entry=row, site={'name':app.config['SITE_NAME']})


if __name__ == '__main__':
  app.run()

