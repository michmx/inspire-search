#!/usr/bin/env python
'''
Uses data/MiembrosRedFAE2017.dat and makes the file of nodes. The output is the nodes file for Gephi.
'''

from src.hepsearch import *
import os, csv

# MiembrosRedFAE2017.dat contains the info of the form filled by FAE members
# First, read the members file
members_file = read_csv('data/MiembrosRedFAE2017.dat','|')

num_authors = len(members_file)

if not os.path.exists("output/"):
    os.makedirs("output")

# Makes the list of nodes
out = csv.writer(open("output/NodesRedFAE2017.csv","w"))
included = []
id = 0
for member in members_file:
    node_name = member[1][0] + "." + member[2].strip()
    if member[3] != "":
        node_name += "-" + member[3].strip()
    if node_name not in included:
        # Nodes file contains: [id, name, gender, type, academic degree, SNI, City, Age]
        if id == 0:
            out.writerow(['Id', node_name, member[4], member[5], member[6], member[7], member[10], member[17]])
        else:
            out.writerow([id, node_name, member[4], member[5], member[6],member[7],member[10],member[17]])
        id += 1
        included.append(node_name)
    else:
        print "WARNING: %s may be duplicated" %node_name
