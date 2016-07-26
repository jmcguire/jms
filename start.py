from flask import Flask
import sqlite3

app = Flask(__name__)

# load config

app.config.from_pyfile('config.cfg')

# test routing

@app.route("/")
def hello():
  return "Hello World: %s\n" % app.config['SITE_NAME']

@app.route("/goodbye")
def goodbye():
  return "goodbye\n"

@app.route("/post/<int:post_id>")
def show_post(post_id):
  return "post: %d\n" % post_id

@app.route("/config/<string:config_var>")
def show_config(config_var):
  return "config_var: %r\n" % app.config[config_var]



# . venv/bin/activate

# to make a basic config-driven mvc cms bbq
#  - setup:
#    - get config
#    - connect to db
#  - basic op
#    - grab first post
#    - get template
#    - apply post variables to template
#    - display template


if __name__ == '__main__':
  app.run()

