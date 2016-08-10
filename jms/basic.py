from jms import app

# basic routing

@app.route("/")
def hello():
  return "Hello and welcome to %s\n" % app.config['SITE_NAME']

@app.route("/config/<string:config_var>")
def show_config(config_var):
  return "config_var: %r\n" % app.config[config_var]

@app.route("/site-map")
def site_map():
  return "%r\n" % app.url_map

