import pprint
import thing

config = {
  '_hello': 'asdf',
  'post': [
    'title',
    'body'
  ],
  'tag': [
    'name'
  ]
}

things = thing.load_things(config)
pp = pprint.PrettyPrinter(indent=4)
for _, data in things.items():
  pp.pprint(vars(data))

