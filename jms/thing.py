from collections import OrderedDict

def load_things(config):
  things = {}

  for field, data in config.items():
    # skip meta info
    if field[0] == '_':
      continue

    things[field] = Thing(field, data)

  return things
    

class Thing(object):
  def __init__(self, name, data):
    """
    everything has sane defaults, except the type, the type is required
    field = 'string' # this is the simplest field, it just says the type
    field = ( type: 'string', ... ) a more complicated type
    """
    self.config = data
    self.name = name

    if type(data) is list:
      self.human_name = readable(name)
      self.plural_name = pluralize(name)
      self.table_name = self.plural_name
    elif type(data) is dict:
      self.human_name = data['_human_name'] or readable(name)
      self.plural_name = data['_plural'] or pluralize(name)
      self.table_name = data['_table_name'] or self.plural_name

    # load the columns
    self.cols = OrderedDict()
    for field in data:
      # skip meta info
      if field[0] == '_':
        continue

      # we could have list or a hash, make it work either way
      if type(data) is list:
        self._load_col(field)
      elif type(data) is dict:
        self._load_col(field, data[field])

    self.field_names = map(lambda x: self.cols[x]['field_name'], self.cols)

  def _load_col(self, name, data=None):
    """load a column data into the self.col dict"""

    col_config = {}
    col_config['name'] = name
    col_config['field_name'] = name

    if data is None:
      col_config['human_name'] = readable(name)
      col_config['form_type'] = 'text'
      col_config['required'] = False
      col_config['check'] = False
    elif type(data) is dict:
      col_config['human_name'] = data['human_name'] or readable(name)
      col_config['form_type'] = data['form_type'] or 'text'
      col_config['required'] = data['required'] or False
      col_config['check'] = None
    else:
      raise Exception("Error with config, don't recognize type of %s: %s" % (name, type(data)))

    self.cols[name] = col_config


def readable(string):
  """return a human-readable version of a variable name"""
  return string.replace('_', ' ').title()

def pluralize(string):
  """return the plural of the string"""
  return string + 's'


