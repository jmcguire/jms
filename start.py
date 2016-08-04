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

with app.app_context():
  init_if_empty()


# routing

@app.route("/")
def hello():
  return "Hello and welcome to %s\n" % app.config['SITE_NAME']

@app.route("/config/<string:config_var>")
def show_config(config_var):
  return "config_var: %r\n" % app.config[config_var]


# post routes

@app.route("/posts")
def show_all_posts():
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from posts")
  posts = cursor.fetchall()

  add_template_variable('posts', posts)
  return my_render_template('show_all_posts.html')


@app.route("/post/<int:post_id>")
def show_post(post_id):
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from posts where id = ?", (post_id,))
  row = cursor.fetchone()
  if row:
    add_template_variable('entry', row)
    return my_render_template('post.html')
  else:
    add_template_variable('post_id', post_id)
    return my_render_template('post_not_found.html')
    

@app.route("/post")
def show_new_post():
  """show form to create a new post"""
  return my_render_template('create_post.html')


@app.route("/post", methods=['POST'])
def create_post():
  """create a new post from a submitted form"""
  # get fields
  title = request.form.get('title', None)
  body = request.form.get('body', None)

  # error check required fields
  errors = []
  if not title:
    errors.append('Title cannot be empty')
  if not body:
    errors.append('Body cannot be empty')

  if errors:
    for e in errors:
      flash(e)
    add_template_variable('title', title)
    add_template_variable('body', body)
    return my_render_template('create_post.html')

  # insert into database
  db = get_db()
  cursor = db.cursor()
  cursor.execute("insert into posts ('title', 'body') values (?, ?)", (title, body))
  db.commit()
  post_id = cursor.lastrowid

  # show new post to the user
  flash("You made a new post")
  return redirect(url_for('show_post', post_id=post_id))


# tag routes

@app.route("/tags")
def show_all_tags():
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from tags")
  tags = cursor.fetchall()

  add_template_variable('tags', tags)
  return my_render_template('show_all_tags.html')


@app.route("/tag/<int:tag_id>")
def show_tag(tag_id):
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from tags where id = ?", (tag_id,))
  row = cursor.fetchone()
  if row:
    add_template_variable('entry', row)
    return my_render_template('tag.html')
  else:
    add_template_variable('tag_id', tag_id)
    return my_render_template('tag_not_found.html')


@app.route("/tag")
def show_new_tag():
  """show form to create a new tag"""
  return my_render_template('create_tag.html')


@app.route("/tag", methods=['POST'])
def create_tag():
  """create a new tag from a submitted form"""
  # get fields
  name = request.form.get('name', None)

  # error check required fields
  errors = []
  if not name:
    errors.append('Name cannot be empty')

  if errors:
    for e in errors:
      flash(e)
    add_template_variable('name', name)
    return my_render_template('create_tag.html')

  # insert into database
  db = get_db()
  cursor = db.cursor()
  cursor.execute("insert into tags ('name') values (?)", (name,))
  db.commit()
  tag_id = cursor.lastrowid

  # show new tag to the user
  flash("You made a new tag")
  return redirect(url_for('show_tag', tag_id=tag_id))


# make templates a bit easier to work with

def add_template_variable(key, value):
  """add a variable that will be made available to the template"""
  if getattr(g, 'template_vars', None) is None:
    g.template_vars = {}
  g.template_vars[key] = value


def my_render_template(template_file):
  """render the template, with our added variables"""
  add_template_variable('site', {'name': app.config['SITE_NAME']})
  return render_template(template_file, **g.template_vars)


if __name__ == '__main__':
  app.run()

