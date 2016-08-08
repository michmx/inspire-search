#!/usr/bin/env python

from src.hepsearch import *
import pickle

# Check if Countries info exists
file_name = 'data/Countries.dat'
if os.path.isfile(file_name):
    file_obj = open(file_name,'rb')
    countries_list = pickle.load(file_obj)
    file_obj.close()
else:
    countries_file = read_csv('data/Countries.csv')
    num_countries = len(countries_file)
    countries_list = []
    for country_site in countries_file:
        # Create object author. The last parameter is the country and is optional
        country = Country(country_site[1],country_site[0])
        # Obtain info from Inspire
        country.get_hindex()
        print country
        countries_list.append(country)

    # Save the list of countries in a file
    file_name = 'data/Countries.dat'
    file_obj = open(file_name,'wb')
    pickle.dump(countries_list,file_obj)
    file_obj.close()


# Read the authors list
file_name = 'data/FAEmembers.dat'
if os.path.isfile(file_name):
    file_obj = open(file_name,'rb')
    author_list = pickle.load(file_obj)
    file_obj.close()
else:
    sys.exit("ERROR: Authors info doesn't exist. Run first get_hepAuthor.")


empty_list = []
# Initialize the collaboration matrix
Matrix = [[empty_list for x in range(len(author_list))] for y in range(len(countries_list))]


# Make the search of authors with countries
for x in range(0,len(author_list)):
    for y in range(0,len(countries_list)):
        if x < y and author_list[x].num_papers != 0 and countries_list[y].num_papers != 0:
            list_papers = make_query('a '+ author_list[x].signature + ' and cc ' +  countries_list[y].code)
            Matrix[x][y] = list_papers
            Matrix[y][x] = list_papers


# Save the collaboration matrix in a file
file_name = 'data/countries_connections.dat'
file_obj = open(file_name,'wb')
pickle.dump(Matrix,file_obj)
file_obj.close()



