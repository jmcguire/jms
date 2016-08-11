from flask import Flask, url_for
app = Flask(__name__)

from jms.db import init_if_empty

# routing libraries
import jms.basic
from jms.generic_crud import create_routes_from_things

# load config
app.config.from_pyfile('config.cfg')
app.secret_key = app.config['SECRET_KEY']

# load things
from jms.thing import load_things
things = load_things(app.config['THINGS'])
create_routes_from_things(things)

# load db
with app.app_context():
  init_if_empty()

if __name__ == '__main__':
  app.run()

