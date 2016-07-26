from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World\n"

@app.route("/goodbye")
def goodbye():
  return "goodbye\n"

@app.route("/post/<int:post_id>")
def show_post(post_id):
  return "post: %d\n" % post_id

if __name__ == '__main__':
  app.run(debug=True) # auto-restart

# . venv/bin/activate

# to make a basic config-driven mvc cms bbq
#  - get config
#  - connect to db
#  - grab first post
#  - get template
#  - apply post variables to template
#  - display template

