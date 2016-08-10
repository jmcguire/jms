from flask import g
from jms import app
from jms.template import *
from jms.db import get_db

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

