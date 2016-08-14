#!/usr/bin/env python

from src.hepsearch import *
import pickle, os.path, sys, csv


# Get the collaboration matrix from file
file_name = 'data/countries_connections.dat'
if os.path.isfile(file_name):
    file_obj = open(file_name,'rb')
    Matrix = pickle.load(file_obj)
    file_obj.close()
else:
    sys.exit("ERROR: Connections info doesn't exist. Run first get_hepCountry.py")

# Check if Countries info exists
file_name = 'data/Countries.dat'
if os.path.isfile(file_name):
    file_obj = open(file_name,'rb')
    countries_list = pickle.load(file_obj)
    file_obj.close()
else:
    sys.exit("ERROR: Countries info doesn't exist. Run first get_hepCountry.py")


file_name = 'data/FAEmembers.dat'
if os.path.isfile(file_name):
    file_obj = open(file_name,'rb')
    author_list = pickle.load(file_obj)
    file_obj.close()
else:
    sys.exit("ERROR: Authors info doesn't exist. Run first get_hepAuthor.")


for y in range(len(countries_list)):
    colaboradores = []
    for x in range(len(author_list)):
        if author_list[x].num_papers != 0 and countries_list[y].num_papers != 0:
            if len(Matrix[y][x]) != 0:
                colaboradores.append(author_list[x].name)
    if len(colaboradores) != 0:
        print 'Colaboracion con ', countries_list[y].name, ', Colaboradores:', len(colaboradores)
       # print "\t",colaboradores


