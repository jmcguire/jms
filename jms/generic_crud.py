from flask import g
from jms import app
from jms.template import *
from jms.db import get_db
import jms.thing

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


# manage our thing objects, which lets us interact with the config file
# constructs

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

