import os
import pickle
import sys
import re
import random
import pystache
from collections import defaultdict
from pinder import Campfire
from optparse import OptionParser
from datetime import date, timedelta
from markov import Markov
from bottle import route, run

def load():
  campfire = Campfire(options.domain, options.token)
  room = campfire.find_room_by_name(options.room)
  users = defaultdict(lambda: Markov(int(options.order)))
  ignore = options.ignore.split(',')

  names = {}
  def name(user):
    if not user in names:
      names[user] = campfire.user(user)['user']['name']
    return names[user]

  if not os.path.exists('cache'):
      os.makedirs('cache')

  for i in range(0, int(options.days)):
    day = date.today() - timedelta(i)
    path = os.path.join('cache', str(day))
    transcripts = None
    if os.path.exists(path):
      sys.stdout.write("got %s from cache ... " % day)
      transcripts = pickle.loads(open(path).read())
    else:
      sys.stdout.write("fetching %s from campfire ... " % day)
      transcripts = room.transcript(date.today() - timedelta(i))
      open(path, 'w+').write(pickle.dumps(transcripts))

    for msg in transcripts:
      if msg['user_id'] and msg['body']:
        username = name(msg['user_id'])
        if not username in ignore:
          users[username].add(msg['body'].encode('utf-8'))
    sys.stdout.write("processed %d messages\n" % len(transcripts))

  print "computing probability trees ... "
  for generator in users.values():
    generator.compute()
  return users

@route('/')
def generate():
  abbr = lambda i: re.sub(r'(\w+)\s+(\w)[\w-]+', r'\1 \2.', i)
  messages = []
  for i in range(0, 100):
      user = random.choice(users.keys())
      messages.append({'name': abbr(user), 'message': users[user].generate(int(random.random() * 20)+5)})

  scope = { 'messages' : messages,
            'users' : [{'name': u} for u in users.keys()],
            'domain': options.domain,
            'room': options.room
          }
  return pystache.render(open('template.mustache').read().encode('utf-8'), scope).encode('utf-8', 'ignore')

parser = OptionParser()
parser.add_option("-t", "--token", dest="token", 
  help="Your Campfire API auth token")
parser.add_option("-d", "--domain", dest="domain", 
  help="Campfire subdomain to use")
parser.add_option("-r", "--room", dest="room", 
  help="Name of room to use")
parser.add_option("-n", "--num_days", dest="days",
  help="Number of days to go back for source material.")
parser.add_option("-o", "--order", dest="order", default="2",
  help="Order of markov chain to use. Defaults to 2.")
parser.add_option("-i", "--ignore", dest="ignore", default="",
  help="Comma separated names of users to ignore.")

(options, args) = parser.parse_args()
users = load()
import bottle
bottle.debug(True)
run(host='localhost', port=8080)
print "ready!"
