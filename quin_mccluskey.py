#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 21:59:01 2014

@author: wykys

program minimalizuje fci danou tabulkou hodnot
využívá Quin McCluskeyho algoritmus
"""
import sys
import copy

# načte soubor do paměti ======================================================
def read_data(loc):
  fr = open(loc, "r")
  data = fr.readlines()
  fr.close()
  return data
  
# zjistí názvy proměnných =====================================================  
def varnames(data):
  variables = data[0].split()
  return variables

# získá základní fci jako disjunkci mintermů ==================================
def fce_maker(data, size):
  mintermes = []
  for i in range(1, len(data)):
    if data[i].find("\t1") != -1:
      data[i] = data[i].replace("\t1", "")      
      mintermes += [[[i-1], data[i].split()]]
  return mintermes

# rozdělí mintermy do skupin podle počtu log. 1 ===============================
def divide(mintermes, size):
  groups = []
  for i in range(size):
    groups += [[]]
  for i in range(len(mintermes)):
    buffer = 0
    for j in range(len(mintermes[i][1])):
      if mintermes[i][1][j] == '1':
        buffer += 1
    groups[buffer] += [mintermes[i]]
  return groups
 
# view vypíše obsah po jednotlivých prvcích ===================================
def view(data):
   for i in data:
     print i

# zjednodušení mintermů =======================================================
def tab(mintermes, size):
  # inicializace hlavních proměnných ----------------------------------------  
  groups = divide(mintermes, size)
  out = []
  used = []
  # pokud je nevhodný vstup, není co řešit ----------------------------------
  if len(groups) < 1:
    return mintermes
  # procházení skupiny ------------------------------------------------------
  for i in range(len(groups)):
    # pokud je skupina prázdná, vynecháme ji    
    if len(groups[i]) < 1:
      continue
    # pokud není prázdná projdeme její prvky
    for j in range(len(groups[i])):
      for k in range(len(groups[i])):
        if j == k or j > k:
          continue
        # porovnání jednotlivých částí mintermů -----------------------        
        buffer = 0
        minterm = []
        for v in range(len(groups[i][j][1])):
          if groups[i][j][1][v] == '-' and groups[i][k][1][v] != '-':
            buffer = -1
            break
          if groups[i][k][1][v] == '-' and groups[i][j][1][v] != '-':
            buffer = -1
            break
          if groups[i][j][1][v] == groups[i][k][1][v]:
            buffer += 1
            minterm += [groups[i][j][1][v]]
          else:
            minterm += ['-']
        # vyhodnocení porovnání ---------------------------------------
        if buffer == size-1 or buffer == size-2:
          # uložení použitých indexů --------------------------------          
          used += [[i, j]]
          used += [[i, k]]
          index = {}
          for h in used:
            index[str(h)] = True
          used = index.keys()
          # skoučení indexů mintermů --------------------------------
          index = {}
          f = groups[i][j][0] + groups[i][k][0]
          for h in f:
            index[h] = True
          # přidání dat k výstupu -----------------------------------
          out += [[index.keys(), minterm]]
      # porovnání s vyšší skupionu --------------------------------------
      # pokud tato skupina neexistuje vynecháme ji
      if i+1 >= len(groups):
        continue
      # pokud je skupina prázdná, vynecháme ji          
      if len(groups[i+1]) < 1:
        continue
      for k in range(len(groups[i+1])):
        # porovnání jednotlivých částí mintermů -----------------------        
        buffer = 0
        minterm = []
        for v in range(len(groups[i][j][1])):
          if groups[i][j][1][v] == '-' and groups[i+1][k][1][v] != '-':
            buffer = -1
            break
          if groups[i+1][k][1][v] == '-' and groups[i][j][1][v] != '-':
            buffer = -1
            break
          if groups[i][j][1][v] == groups[i+1][k][1][v]:
            buffer += 1
            minterm += [groups[i][j][1][v]]
          else:
            minterm += ['-']
        #print "mintemr: ", minterm
        # vyhodnocení porovnání ---------------------------------------
        if buffer == size-1 or buffer == size-2:
          # uložení použitých indexů --------------------------------          
          used += [[i, j]]
          used += [[i+1, k]]
          index = {}
          for h in used:
            index[str(h)] = True
          used = index.keys()
          # skoučení indexů mintermů --------------------------------
          index = {}
          f = groups[i][j][0] + groups[i+1][k][0]
          for h in f:
            index[h] = True
          # přidání dat k výstupu -----------------------------------
          out += [[index.keys(), minterm]]
  # pokud neproběhli žádné změny vrať vstup
  if used == []:
    return mintermes
  # přidání nezjednodušený mintermů -----------------------------------------
  for i in range(len(groups)):
    # pokud je skupina prázdná, vynecháme ji    
    if len(groups[i]) < 1:
      continue
    # pokud není prázdná projdeme její prvky
    for j in range(len(groups[i])):
      if str(used).find(str([i, j])) == -1:
        out += [[groups[i][j][0], groups[i][j][1]]]
  
  # vyřazení duplikátů mintermů ---------------------------------------------
  index = {}
  for j in range(len(out)):
    i = []
    for k in range(len(out)):
      if out[j][1] == out[k][1]:
        i += [k]
    index[str(i)] = i  
  i = index.values()
  # skoučení indexů mintermů ------------------------------------------------
  out_min = []
  for j in i:
    index = {}
    f = []
    for k in j:
      f += out[k][0]
    for h in f:
      index[h] = True
    out_min += [[index.keys(), out[k][1]]]
  # přidání dat k výstupu ---------------------------------------------------
  
  return out_min

# minimální pokrytí všech stavů ===============================================
def states_minimal(mintermes):
  # získání stavů, kde je výstup fce = 1 ------------------------------------
  index = {}
  for m in mintermes:
    for s in m[0]:
      index[s] = True
  states = index.keys()
  # vytvoření tabulky pro analízu -------------------------------------------
  line = []
  for i in states:
    line += [' ']
  table = []
  for i in mintermes:
    table += [copy.deepcopy(line)]
  # vyplnění tabulky --------------------------------------------------------
  for m in range(len(mintermes)):
    for s in mintermes[m][0]:
      for i in range(len(states)):
        if states[i] == s:
          break
      table[m][i] = '*'
  #view(table)
  print ''
  # analíza tabulky ---------------------------------------------------------
  fce = []
  full = 0
  #while full != len(states):
  for i in range(len(states)):
    if line[i] == '*':
      continue
    buffer = []
    
    for j in range(len(mintermes)):
      if table[j][i] == '*':
        buffer += [j]        
    v = 0
    for b in buffer:
      if v < len(mintermes[b][0]):
        v = b
    for k in mintermes[b][0]:
      for f in range(len(states)):
        if line[f] == '*':
          continue
        if  states[f] == k:
          full += 1
          line[f] = '*'
    fce += [mintermes[b]]

    #print line
  return fce

# vrátí funkci z mintermů
def equation(mintermes, variables):
  out = variables[-1] + " = "
  for m in mintermes:
    out += '('
    x = len(m[1]) - str(m[1]).count('-') - 1
    for i in range(len(m[1])):
      """if x > 0:
        x -= 1
        out += " and """
      if m[1][i] == '-':
        continue
      elif m[1][i] == '0':
        out += "not "
      out += variables[i]
      if x > 0:
        x -= 1
        out += " and "
    out += ')'
    if m == mintermes[-1]:
      continue
    out += " or "
  print out

# main code ===================================================================
old = -1
if len(sys.argv) < 2:
  print "input error"
data = read_data(sys.argv[1])
variables = varnames(data)
mintermes = fce_maker(data, len(variables)-1)
"""print "input>"
view(mintermes)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
"""
###############################################################################
while old != mintermes:  
  old = mintermes
  mintermes = tab(mintermes, len(variables))
"""print "out>"
view(mintermes)
print "******************************"
"""
###############################################################################
mintermes  = states_minimal(mintermes)
"""print "states_minimal>"
view(mintermes)
print "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
"""
###############################################################################
view(mintermes)
equation(mintermes, variables)
