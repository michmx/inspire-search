#!/usr/bin/env python

from src.hepsearch import Paper
import pickle, os.path, sys, csv


# Get the collaboration matrix from file
file_name = 'data/connections.dat'
if os.path.isfile(file_name):
    file_obj = open(file_name,'rb')
    Matrix = pickle.load(file_obj)
    file_obj.close()
else:
    sys.exit("ERROR: Connections info doesn't exist. Run first get_hepdata.")


# Make the Gephi input file
gephi_input = 'RedFAEConnections.csv'
file_obj = open(gephi_input,'w')

outputWriter = csv.writer(file_obj)
outputWriter.writerow(['Source','Target','Type','Weight'])

for x in range(len(Matrix[0])):
    for y in range(x,len(Matrix[0])):
        if len(Matrix[x][y]) != 0 and x != y:
            outputWriter.writerow([x,y,'Undirected',len(Matrix[x][y])])

file_obj.close()
