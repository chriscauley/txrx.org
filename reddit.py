from datetime import datetime, timedelta
from math import log
from random import randint

epoch = datetime(1970, 1, 1)

def epoch_seconds(date):
  """Returns the number of seconds from the epoch to date."""
  td = date - epoch
  return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(ups, downs):
  return ups - downs

now = datetime.now()

class Post:
  def __init__(self,id):
    self.id = id
    self.ups = randint(0,200)
    self.downs = randint(0,50)
    self.date = now-timedelta(0,randint(0,10)*3600)
  @property
  def hot(self):
    """The hot formula. Should match the equivalent function in postgres."""
    s = score(self.ups, self.downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(self.date) - 1134028003
    return round(sign * order + seconds / 45000, 7)

posts = [Post(i) for i in range(100)]
reddit_sorted = sorted(posts,key=lambda p:p.hot)
for post in reddit_sorted:
  print post.id,'\t',post.hot,post.ups
