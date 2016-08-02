#!/usr/bin/env python

from src.hepsearch import *
import pickle

# First, read the nodes list
nodes_file = read_csv('RedFAENodes_tiny.csv')
nodes_file.pop(0)

num_authors = len(nodes_file)

empty_list = []
# Initialize the collaboration matrix
Matrix = [[empty_list for x in range(num_authors)] for y in range(num_authors)]


# Make the search of authors
for author in nodes_file:
    for author2 in nodes_file:
        if int(author[0]) < int(author2[0]):

            list = make_query_authors(find_signature(author[1]), find_signature(author2[1]))
            Matrix[int(author[0])][int(author2[0])] = list
            Matrix[int(author2[0])][int(author[0])] = list


# Save the collaboration matrix in a file
file_name = 'data/connections.dat'
file_obj = open(file_name,'wb')
pickle.dump(Matrix,file_obj)
file_obj.close()


