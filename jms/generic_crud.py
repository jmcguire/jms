from flask import g
from jms import app
from jms.view import *
from jms.db import get_db
from jms.thing import load_things

# generic CRUD functions for our tables

def show_one(thing, id_):
  """show a single thing"""
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from %s where id = ?" % thing.table_name, (id_,))
  row = cursor.fetchone()

  add_template_variable('thing', thing)
  if row:
    add_template_variable('entry', row)
    return my_render_template('generic/show_one.html')
  else:
    add_template_variable('id', id_)
    return my_render_template('generic/not_found.html')


def show_all(thing):
  """show a list of all things"""
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from %s" % thing.table_name)
  entries = cursor.fetchall()

  add_template_variable('thing', thing)
  add_template_variable('entries', entries)
  return my_render_template('generic/show_all.html')


def show_new(thing):
  """show a form to create a new thing"""
  add_template_variable('thing', thing)
  return my_render_template('generic/create.html')


def create(thing):
  """create a new thing form a post"""
  fields = {}
  errors = []

  for col in thing.cols:
    new[col.field_name] = request.form.get(col.field_name)
    if col.required and not new[col.field_name]:
      errors.append('%s cannot be empty' % col.human_name)

  if errors:
    for e in errors:
      flash(e)
    add_template_variable('thing', thing)
    add_template_variable('fields', fields)
    return my_render_template('generic/create_post.html')

  # insert into database

  db = get_db()
  cursor = db.cursor()

  # create the two strings we use in the query
  field_names = "'" + "', '".join(thing.field_names) + "'"
  question_marks = ", ".join(map(lambda x: '?', thing.field_names.count() ))

  cursor.execute("insert into posts (%s) values (%s)" % (field_names, question_marks), (title, body))
  db.commit()
  new_id = cursor.lastrowid

  # show new post to the user
  flash("You made a new %s" % thing.human_name)
  return redirect(url_for('show_one', id_=new_id))


def delete(thing, id_):
  """delete a single thing"""
  pass


# turn a thing into a series of CRUD operations

def create_routes_from_thing(thing):
  app.add_url_rule("/%s/<int:id_>" % thing.name, 'show_one_%s' % thing.name, lambda id_: show_one(thing, id_))
  app.add_url_rule("/%s" % thing.plural_name, 'show_all_%s' % thing.name, lambda: show_all(thing))
  app.add_url_rule("/%s" % thing.name, 'show_new_%s' % thing.name, lambda: show_new(thing))
  app.add_url_rule("/%s" % thing.name, 'create_%s' % thing.name, lambda: create(thing), methods=['POST'])
  #app.add_url_rule("/%s<int:id_>" % thing.name, 'delete_%s' % thing.name, lambda id_: delete(thing, id_), methods=['DELETE'])

def create_routes_from_things(things):
  """a shortcut to the above"""
  for thing in things.values():
    create_routes_from_thing(thing)


# manage our thing objects, which lets us interact with the config file
# constructs

def get_things():
  """return the thing objects, create them if they don't exist yet"""
  things = getattr(g, 'things', None)
  if things is None:
    things = g.things = load_things(app.config['THINGS'])

  return things

def get_thing(name):
  """return the thing config we need"""
  things = get_things()
  return things[name]

