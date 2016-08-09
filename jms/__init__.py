from flask import Flask
app = Flask(__name__)

from jms.db import init_if_empty

# routing libraries
import jms.basic
import jms.posts
import jms.tags
import jms.generic_crud

# load config
app.config.from_pyfile('config.cfg')
app.secret_key = app.config['SECRET_KEY']

# load db
with app.app_context():
  init_if_empty()

if __name__ == '__main__':
  app.run()

