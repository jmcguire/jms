from flask import g
from jms import app
from jms.template import *
from jms.db import get_db
from jms.thing import load_things

# generic CRUD functions for our tables

def show_one(thing, id_):
  """show a single thing"""
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from %s where id = ?" % thing.table_name, (tag_id,))
  row = cursor.fetchone()

  add_template_variable('thing', thing)
  if row:
    add_template_variable('entry', row)
    return my_render_template('thing/show_one.html')
  else:
    add_template_variable('id', id_)
    return my_render_template('thing/not_found.html')


def show_all(thing):
  """show a list of all things"""
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from %s" % thing.table_name)
  entries = cursor.fetchall()

  add_template_variable('thing', thing)
  add_template_variable('entries', entries)
  return my_render_template('thing/show_all.html')


def show_new(thing):
  """show a form to create a new thing"""
  add_template_variable('thing', thing)
  return my_render_template('thing/create.html')


def create(thing):
  """create a new thing"""
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
    return my_render_template('thing/create_post.html')

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

  #this is the definition of route
  def route(self, rule, **options):
    def decorator(f):
      endpoint = options.pop('endpoint', None)
      self.add_url_rule(rule, endpoint, f, **options)
      return f
    return decorator

  app.add_url_rule("/%s/<int:id_>" % thing.name, 'show_one_%s' % thing.name, lambda x: show_one(thing, x))
  app.add_url_rule("/%s" % thing.plural_name, 'show_all_%s' % thing.name, lambda: show_all(thing))
  app.add_url_rule("/%s" % thing.name, 'show_new_%s' % thing.name, lambda: show_new(thing))
  app.add_url_rule("/%s" % thing.name, 'create_%s' % thing.name, lambda: create(thing), methods=['POST'])
  app.add_url_rule("/%s<int:id_>" % thing.name, 'delete_%s' % thing.name, lambda x: delete(thing, x), methods=['DELETE'])

  # @app.route("/FOO/<int:id_>") show_one()
  # @app.route("/FOOs") show_all()
  # @app.route("/FOO") show_new()
  # @app.route("/FOO", methods=['POST']) create()
  # @app.route("/FOO/<int:id_>", methods=['DELETE']) delete()

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

def get_thing(thing):
  """return the thing config we need"""
  things = get_things()
  return things[thing]

