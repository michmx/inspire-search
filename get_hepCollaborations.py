#!/usr/bin/env python

from src.hepsearch import *
import pickle, os, csv

# MiembrosRedFAE2017.dat contains the info of the form filled by FAE members
# First, read the members file
members_file = read_csv('data/MiembrosRedFAE2017.txt','|')
#members_file.pop(0)

num_authors = len(members_file)

if not os.path.exists("output/"):
    os.makedirs("output")

# Makes the list of nodes
out = csv.writer(open("output/NodesRedFAE2017.csv","w"))
nodes, included = [], []
id = 0
for member in members_file:
    node_name = member[1][0] + "." + member[2].strip()
    if member[3] != "":
        node_name += "-" + member[3].strip()
    if not node_name in included:
        # Nodes list contains : [id, name, signatures]
        nodes.append([id, node_name, member[16]])
        # Nodes file contains: [id, name, gender, type, academic degree, SNI, City, Age]
        out.writerow([id, node_name, member[4], member[5], member[6],member[7],member[10],member[17]])
        id += 1
        included.append(node_name)
    else:
        print "WARNING: %s may be duplicated" %node_name

empty_list = []
# Initialize the collaboration matrix
Matrix = [[empty_list for x in range(num_authors)] for y in range(num_authors)]


# Make the search of authors
nodes.pop(0);
for author in nodes:
    for author2 in nodes:
        if int(author[0]) < int(author2[0]):
            list = make_query_authors(check_signature(author), check_signature(author2))
            Matrix[int(author[0])][int(author2[0])] = list
            Matrix[int(author2[0])][int(author[0])] = list

exit(0)
# Save the collaboration matrix in a file
file_name = 'data/connections.dat'
file_obj = open(file_name,'wb')
pickle.dump(Matrix,file_obj)
file_obj.close()


