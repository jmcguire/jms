from flask import Flask, g, render_template, request, flash, redirect, url_for

app = Flask(__name__)

import thing
from jms.template import *
from jms.db import *
import jms.posts


# load config

app.config.from_pyfile('config.cfg')
app.secret_key = app.config['SECRET_KEY']

def get_things():
  """return the thing objects, create them if they don't exist yet"""
  things = getattr(g, 'things', None)
  if things is None:
    things = g.things = thing.load_things(app.config['THINGS'])
  return things

def get_thing(thing):
  """return the thing config we need"""
  things = get_things()
  return things[thing]


# load db

with app.app_context():
  init_if_empty()


# routing

@app.route("/")
def hello():
  return "Hello and welcome to %s\n" % app.config['SITE_NAME']

@app.route("/config/<string:config_var>")
def show_config(config_var):
  return "config_var: %r\n" % app.config[config_var]



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


# generic CRUD functions for our tables

def show_one(thing, id_):
  """show a single thing"""
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from %s where id = ?" % thing.table_name, (tag_id,))
  row = cursor.fetchone()
  if row:
    add_template_variable('entry', row)
    add_template_variable('thing', thing)
    return my_render_template('thing/show_one.html')
  else:
    add_template_variable('id', id_)
    return my_render_template('thing/not_found.html')

def show_all(thing):
  """show a list of all things"""
  pass

def show_new(thing):
  """show a form to create a new thing"""
  pass

def create(thing):
  """create a new thing"""
  pass

def delete(thing, id_):
  """delete a single thing"""
  pass



if __name__ == '__main__':
  app.run()

