#!/usr/bin/env python

from src.hepsearch import *
import pickle

# First, read the nodes list
nodes_file = read_csv('RedFAENodes.csv')
nodes_file.pop(0)

num_authors = len(nodes_file)

authors_list = []

for node in nodes_file:
    # Create object author. The last parameter is the country and is optional
    author = Author(node[1],node[2],'mx')
    # Obtain info from Inspire
    author.get_hindex()

    print author
    authors_list.append(author)

# Save the list of authors in a file
file_name = 'data/FAEmembers.dat'
file_obj = open(file_name,'wb')
pickle.dump(authors_list,file_obj)
file_obj.close()



