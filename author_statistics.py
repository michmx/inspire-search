#!/usr/bin/env python

from src.hepsearch import Author
import pickle, os.path, sys, csv


file_name = 'data/FAEmembers.dat'
if os.path.isfile(file_name):
    file_obj = open(file_name,'rb')
    author_list = pickle.load(file_obj)
    file_obj.close()
else:
    sys.exit("ERROR: Authors info doesn't exist. Run first get_hepAuthor.")

h_total = 0.0
for author in author_list:
    h_total += author.hindex
    print author.name,',',author.hindex, ',', author.num_papers

print "h-index promedio: ", h_total/len(author_list)