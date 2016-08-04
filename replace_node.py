#!/usr/bin/env python

from src.hepsearch import *
import pickle, sys, os

# Number of the node to be replaced
node_number = 69

# New signature to search
node_name = 'Cruz, Emilia'

# Get the collaboration matrix from file
file_name = 'data/connections.dat'
if os.path.isfile(file_name):
    file_obj = open(file_name,'rb')
    Matrix = pickle.load(file_obj)
    file_obj.close()
else:
    sys.exit("ERROR: Connections info doesn't exist. Run first get_hepdata.")

# First, make a copy of the .dat file to a .dat.old.#
os.system("mv data/connections.dat data/connections.dat.old")

nodes_file = read_csv('RedFAENodes.csv')
nodes_file.pop(0)

num_authors = len(nodes_file)

# Make the search of authors
for author2 in nodes_file:
    if node_number != int(author2[0]):
        list = make_query_authors(node_name, find_signature(author2[1]))
        Matrix[node_number][int(author2[0])] = list
        Matrix[int(author2[0])][node_number] = list


# Save the collaboration matrix in the file
file_name = 'data/connections.dat'
file_obj = open(file_name,'wb')
pickle.dump(Matrix,file_obj)
file_obj.close()


