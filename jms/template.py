from flask import g, render_template, current_app

__all__ = ['add_template_variable', 'my_render_template']

# make templates a bit easier to work with

def add_template_variable(key, value):
  """add a variable that will be made available to the template"""
  if getattr(g, 'template_vars', None) is None:
    g.template_vars = {}
  g.template_vars[key] = value


def my_render_template(template_file):
  """render the template, with our added variables"""
  add_template_variable('site', {'name': current_app.config['SITE_NAME']})
  return render_template(template_file, **g.template_vars)

