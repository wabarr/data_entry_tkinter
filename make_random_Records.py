## first, run the main.py file to create the database
## then run this code to make fake data in the db

from models import Record
from datetime import datetime

import requests
from random import sample, choice, randint, random

word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

response = requests.get(word_site)
WORDS = response.content.splitlines()

samp = sample(WORDS, 20)

for each in range(1, 2000):
   new = Record(name=choice(samp), 
   photo=choice(samp), 
   x=random(), 
   y=random() * random() * random(), 
   date=datetime.now(),
   lastmodified=datetime.now(), 
   count=randint(1, 10))
   new.save()