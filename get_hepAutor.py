#!/usr/bin/env python

from src.hepsearch import *
import pickle

# MiembrosRedFAE2017.dat contains the info of the form filled by FAE members
# First, read the members file
members_file = read_csv('data/MiembrosRedFAE2017.dat','|')

num_authors = len(members_file)

authors_names, included = [], []
id = 0
for member in members_file:
    node_name = member[1][0] + "." + member[2].strip()
    if member[3] != "":
        node_name += "-" + member[3].strip()
    if not node_name in included:
        # node in format[id, name, signatures]
        authors_names.append([id, node_name, member[16]])
        id += 1
    else:
        print "WARNING: %s may be duplicated" % node_name

authors_list = [];

for node in authors_names:
    # Create object author. The last parameter is the country and is optional
    author = Author(node, 'mx')
    # Obtain info from Inspire
    author.get_hindex()

    print author
    authors_list.append(author)

# Save the list of authors in a file
file_name = 'data/authors.dat'
file_obj = open(file_name,'wb')
pickle.dump(authors_list,file_obj)
file_obj.close()



