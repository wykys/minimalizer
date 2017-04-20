#!/usr/bin/python
import random
import sys

a = []
while len(a) < int(sys.argv[1]):
  x = random.randint(1, 49)
  if (x in a) == False:
    a += [x]
print a
