from flask import g
from jms import app
from jms.template import *
from jms.db import get_db

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

