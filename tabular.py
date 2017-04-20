# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 09:48:57 2014

@author: wykys
"""

import copy
from subprocess import call

# načte soubor do paměti ------------------------------------------------------
def read_data():
    fr = open("k_test_3.txt", "r")
    data = fr.readlines()
    fr.close()
    return data

# vytvoří fci pomocí součtu minetermů -----------------------------------------
def mineterm(data):
    # zjištění názvů proměnných    
    variables = []
    i = 0
    while i < len(data[0]):
        buffer = ""
        if data[0][i] == '\t':
            i += 1
            while i < len(data[0]) and data[0][i] != '\t' and data[0][i] != ' ' and data[0][i] != '\n':
                buffer += data[0][i]            
                i += 1
            if buffer != "":
                variables += [buffer]            
            break    
        else:
            if data[0][i] == ' ':
                i += 1
                continue        
            buffer += data[0][i]
            i += 1
            while i < len(data[0]) and data[0][i] != '\t' and data[0][i] != ' ':
                buffer += data[0][i]            
                i += 1
            if buffer != "":
                variables += [buffer]
    
    # zjištění hodnot výstupů   
    states = [] # vstupní proměnné
    out = []    # výstupní stavy
    for j in range(1, 1+2**(len(variables)-1)):
        i = 0
        while i < len(data[j]):
            buffer = ""
            if data[j][i] == '\t':
                i += 1
                while i < len(data[j]) and data[j][i] != '\t' and data[j][i] != ' ' and data[j][i] != '\n':
                    buffer += data[j][i]
                    i += 1
                if buffer != "":
                    out += [buffer]            
                break    
            else:
                if data[0][i] == ' ':
                    i += 1
                    continue        
                buffer += data[j][i]
                i += 1
                while i < len(data[j]) and data[j][i] != '\t' and data[j][i] != ' ':
                    buffer += data[j][i]            
                    i += 1
                
                if buffer != "":
                    states += [[]]
                    states[j-1] += [buffer]
    
    # vytvoření fce pomocí minetermů
    fce = []
    k = 0
    for i in range(len(out)):
        if out[i] == '1':
            fce += [[]]
            for j in range(len(states[i])):                
                fce[k] += [[states[i][j], variables[j]]]
            k += 1
    
    return fce

# výstup do pdf pomocí latexu -------------------------------------------------
def latex(fce):
    buffer = ""
    buffer += "\\documentclass[a2paper]{article}\n"
    buffer += "\\usepackage[utf8]{inputenc}\n"
    buffer += "\\usepackage[total={20cm,25cm}, top=1cm, left=0cm, includefoot]{geometry}\n"
    buffer += "\\begin{document}\n$$"    
    buffer += "Y ="
    for i in range(len(fce)):
        if i != 0:
            buffer += "  + "        
        for j in range(len(fce[i])):
            if fce[i][j][0] == '0':
                buffer += " \\overline{" + fce[i][j][1] + "}"
            else:
                buffer += " {0}".format(fce[i][j][1])
    buffer += "$$\n\\end{document}"
    fw = open("tabular.tex", "w")
    fw.write(buffer)
    fw.close
    
    call(["pdflatex", "tabular.tex"])

# vypsání fce pomocí rovnice --------------------------------------------------
def show(fce):
    buffer = "Y ="
    for i in range(len(fce)):
        if i != 0:
            buffer += "  + "        
        for j in range(len(fce[i])):
            if fce[i][j][0] == '0':
                buffer += " not"
            buffer += " {0}".format(fce[i][j][1])
    print buffer

# vypsání všech prvků s odsazováním po hlavním indexu
def view(fce):
    for i in range(len(fce)):
        print "{}\t{}".format(i, fce[i])

# tabulkové zjednodušení ------------------------------------------------------
def tabular(fce):    
    
    out = [] 
    indexes = []
    o = 0
    for i in range(len(fce)):
        for j in range(len(fce)):
            if i == j:
                continue
            par = 0                        
            for k in range(len(fce[i])):
                if len(fce[i]) == len(fce[j]):
                    if fce[i][k] == fce[j][k]:
                        par += 1
            
            if par == (len(fce[0])-1) or par == len(fce[0]):
                if len(fce[i]) == len(fce[j]):                 
                    out += [[]]
                    indexes += [i, j]                
                    for k in range(len(fce[i])):
                        if fce[i][k] == fce[j][k]:
                            out[o] += [fce[i][k]]
                    o += 1
    
    # přidání monomů, které nebyli zjednodušeny
    for i in range(len(fce)):
        if indexes.count(i) == 0:
            out += [[]]
            out[o] += fce[i]
            o += 1
    
    # pokud nedošlo k žádné úpravě vrať vstup
    if out[0] == []:
       return fce
        
    # vymazání opakujících se monumů          
    i = 0
    while i < len(out):
        while out.count(out[i]) != 1:
            out.remove(out[i])            
        i += 1  
    while out.count([]) != 0:
        out.remove([])
        
      
    return out

# main code -------------------------------------------------------------------    
fce = mineterm(read_data())
show(fce)
print "\n"
old = 1

while old != fce:
    old = copy.deepcopy(fce)
    fce = tabular(fce)
    show(fce)
    print "\n"
   
# vygenerování PDF výstupu
#latex(fce)

