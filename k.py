# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 21:33:22 2014

@author: wykys

minimalizace založená na k mapě 
"""

import copy
import math
import itertools
from subprocess import call

fr = open("k_test_5.txt", "r")
data = fr.readlines()
fr.close()



# zjištění proměnných => obsah k mapy
k_size = 0
variables = []

i = 0
while i < len(data[0]):
    buffer = ""
    if data[0][i] == '\t':
        break    
    else:
        if data[0][i] == ' ':
            i += 1
            continue
        k_size += 1
        buffer += data[0][i]
        i += 1
        while i < len(data[0]) and data[0][i] != '\t' and data[0][i] != ' ':
            buffer += data[0][i]            
            i += 1
        if buffer != "":
            variables += [buffer]
if k_size > 1:
    k_size = 2**k_size 

# zjištění velikostí stran k mapy
y_size = int(k_size**(1/2.))
x_size = k_size/y_size
if y_size*x_size != k_size:
    y_size -= 1
    x_size  = k_size/y_size

# vytvoření k mapy
k = []
column = []
for y in range(y_size):
    column += [[]]
for x in range(x_size):
    k += copy.deepcopy([column])

# vytvoření kopie pro kontrolu kontrolovanných 
z = copy.deepcopy(k)

# zjištění všech kombinací vstupních proměnných
states = [] # vstupní proměnné
out = []    # výstupní stavy
for i in range(1, 1+2**len(variables)):
    j = 0    
    # přesunutí proměnných z konkrétního řátku do bufferu    
    buffer = []    
    while j < len(data[i]):
        if data[i][j] == '\t':
            j += 1
            out += [int(data[i][j])]
            break    
        else:
            if data[i][j] == ' ':
                j += 1
                continue
            buffer += [int(data[i][j])]
            j += 1
            while i < len(data[i]) and data[i][j] != '\t' and data[i][j] != ' ':
                buffer += [int(data[i][j])]
                j += 1
    
    # vyhodnocení bufferu => získání všech kombinací proměnných        
    states += [[]]    
    for j in range(len(buffer)):
        if buffer[j] == 1:
            states[i-1] += [variables[j]]  

# vytvoření duplikátu k mapy pro proměnné
v = copy.deepcopy(k)

# přiřazení proměnných do duplikátu
u = 0
states.remove(states[0])
while states != []:
    if u < math.log(x_size*y_size, 2):
        for x in range(1, x_size):
            if v[x][0] == []:
                for i in range(len(states)):
                    if len(states[i]) == 1:
                        break
                v[x][0] = states[i]
                states.remove(states[i])
                u += 1
                break
        for y in range(1, y_size):
            if v[0][y] == []:
                for i in range(len(states)):
                    if len(states[i]) == 1:
                        break
                v[0][y] = states[i]
                states.remove(states[i])
                u += 1
                break
    
    # dopočítání zbylích stavů
    # v horním řádku
    for X in range(1, x_size):
        if v[X][0] == [] and X > 2:            
            for Xx in range(1, X):
                for x in range(1, x_size):
                    buffer = v[Xx][0] + v[x][0]
                    per = list(itertools.permutations(buffer))                
                    for i in range(len(per)):
                        for j in range(len(states)):
                            if list(per[i]) == states[j]:
                                v[X][0] = states[j]
                                states.remove(states[j])
                                break
                        if v[X][0] != []:
                            break
                    if v[X][0] != []:
                            break
                
    # v levém sloupci
    for Y in range(1, y_size):
        if v[0][Y] == [] and Y > 2:            
            for Yy in range(1, Y):
                for y in range(1, y_size):
                    buffer = v[0][Yy] + v[0][y]
                    per = list(itertools.permutations(buffer))                
                    for i in range(len(per)):
                        for j in range(len(states)):
                            if list(per[i]) == states[j]:
                                v[0][Y] = states[j]
                                states.remove(states[j])
                                break
                        if v[0][Y] != []:
                            break
                    if v[0][Y] != []:
                            break
    
    # dopočítat střed
    for y in range(1, y_size):
        for x in range(1, x_size):
            if v[x][y] == [] and v[x][0] != [] and v[0][y] != []:
                buffer = v[x][0] + v[0][y]
                per = list(itertools.permutations(buffer))                
                for i in range(len(per)):
                    for j in range(len(states)):
                        if list(per[i]) == states[j]:
                            v[x][y] = states[j]
                            states.remove(states[j])
                            break;
                    if v[x][y] != []:
                        break
    

# vyplnění k mapy
s = copy.deepcopy(k) # jen pro uložení stavů
variables.reverse()
for x in range(x_size):
    for y in range(y_size):
        buffer = 0
        for i in range(len(variables)):
            for j in range(len(v[x][y])):
                if v[x][y][j] == variables[i]:
                    buffer += 2**i
        s[x][y] = buffer
        k[x][y] = out[buffer]
            

# výpis fce z k mapy
high = []
for x in range(x_size):
    for y in range(y_size):
        if k[x][y] == 1:
            high += [[x, y]]
            
# generování souboru pro latex
out_str = ""
out_str += "\\documentclass[a3paper]{article}\n"
out_str += "\\usepackage[utf8]{inputenc}\n\n"
out_str += "\\usepackage[total={30cm,25cm}, top=1cm, left=0.5cm, includefoot]{geometry}\n"
out_str += "\\begin{document}\n"
out_str += "\\section{Karnaughova mapa (modificated by wykys)}\n"
out_str += "\\subsection{rozložení proměnných}\n"
out_str += "\\begin{tabular}[c]{"
out_str += x_size * "| c " + "|}\n"

for y in range(y_size):
    out_str += "\n\\hline\n"  
    for x in range(x_size):
        if x < x_size-1:        
            out_str += str(v[x][y]) + '&'
        else:
            out_str += str(v[x][y])
    out_str += "\\\\"

out_str += "\n\\hline\n"
out_str += "\\end{tabular}\n"

out_str += "\\newline\n\\newline\n\\newline\n"

out_str += "\\begin{tabular}[c]{"
out_str += x_size * "| c " + "|}\n"

for y in range(y_size):
    out_str += "\n\\hline\n"  
    for x in range(x_size):
        if x < x_size-1:        
            out_str += str(s[x][y]) + '&'
        else:
            out_str += str(s[x][y])
    out_str += "\\\\"

out_str += "\n\\hline\n"
out_str += "\\end{tabular}\n"

out_str += "\\newline\n\\newline\n\\newline\n"

out_str += "\\begin{tabular}[c]{"
out_str += x_size * "| c " + "|}\n"

for y in range(y_size):
    out_str += "\n\\hline\n"  
    for x in range(x_size):
        if x < x_size-1:        
            out_str += str(k[x][y]) + '&'
        else:
            out_str += str(k[x][y])
    out_str += "\\\\"

out_str += "\n\\hline\n"
out_str += "\\end{tabular}\n"

out_str += "\\newline\\newline\n\\verb|x_size|: {0}\n\\newline\n\\verb|y_size|: {1}\n".format(x_size, y_size)
       
out_str += "\\end{document}\n"

fw = open("tab.tex", "w")
fw.write(out_str)
fw.close()

# vygenerování PDF výstupu
call(["pdflatex", "tab.tex"])

print high