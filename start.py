from flask import Flask, g, render_template, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)

# load config

app.config.from_pyfile('config.cfg')
app.secret_key = app.config['SECRET_KEY']

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
  cursor = db.cursor()
  cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_name';")
  row = cursor.fetchone()
  cursor.close()
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
  return "Hello and welcome to %s\n" % app.config['SITE_NAME']

@app.route("/config/<string:config_var>")
def show_config(config_var):
  return "config_var: %r\n" % app.config[config_var]


@app.route("/posts")
def show_all_posts():
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from posts")
  posts = cursor.fetchall()
  return render_template('show_all_posts.html', posts=posts, site={'name':app.config['SITE_NAME']})


@app.route("/post/<int:post_id>")
def show_post(post_id):
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from posts where id = ?", (post_id,))
  row = cursor.fetchone()
  if row:
    return render_template('post.html', entry=row, site={'name':app.config['SITE_NAME']})
  else:
    return render_template('post_not_found.html', post_id=post_id, site={'name':app.config['SITE_NAME']})
    

@app.route("/post")
def show_new_post():
  """show form to create a new post"""
  return render_template('create_post.html', site={'name':app.config['SITE_NAME']})


@app.route("/post", methods=['POST'])
def create_post():
  """create a new post from a submitted form"""
  # get fields
  title = request.form.get('title', None)
  body = request.form.get('body', None)

  # error check required fields
  errors = []
  if title is None:
    print "one\n"
    errors.append('Title cannot be empty')
  if body is None:
    print "two\n"
    errors.append('Body cannot be empty')

  if errors:
    print "three\n"
    for e in errors:
      flash(e)
    print "four\n"
    return render_template('create_post.html', title=title, body=body, site={'name':app.config['SITE_NAME']})

  # insert into database
  db = get_db()
  cursor = db.cursor()
  cursor.execute("insert into posts ('title', 'body') values (?, ?)", (title, body))
  db.commit()
  post_id = cursor.lastrowid

  # show new post to the user
  flash("You made a new post")
  return redirect(url_for('show_post', post_id=post_id))


if __name__ == '__main__':
  app.run()

