#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 17:14:46 2014

@author: wykys

program vygeneruje tabulku určenou pro minimalizaci
"""

LEN_A = 8;
LEN_B = 8;
LEN_Y = 8;

buffer = ""
out = "";

# hlavička --------------------------------------------------------------------
for i in range(LEN_A-1, -1, -1):
  out += "A[%1d] " % i

for i in range(LEN_A-1, -1, -1):
  out += "B[%1d] " % i

out += '\t'

for i in range(LEN_A-1, -1, -1):
  out += "Y[%1d]\t" % i

out += "Err"

out += '\n'

print out
# konec hlavičky --------------------------------------------------------------

for i in range(2**(LEN_A+LEN_B)):
  buffer = ("{0:0" + str(LEN_A+LEN_B) + "b}").format(i)
  for j in range(LEN_A+LEN_B):
    out += buffer[j] + "    "
  A = int(buffer[0:8], 2)
  B = int(buffer[8:16], 2)
  if B != 0:  
    buffer = ("{0:0" + str(LEN_Y) + "b}").format(A/B)
    for s in buffer:
      out += '\t' + s
    Err = 0
  else:
    out += "\t0" * LEN_Y
    Err = 1
  
  out += "\t{}".format(Err)
  out += '\n'
out += '\n'
fw = open("div.txt", 'w')
fw.write(out)
fw.close()
