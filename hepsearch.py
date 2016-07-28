import sys, os, getopt, re, urllib


class Paper:
    def __init__(self, paper_name = ''):
        self.title = paper_name
        self.authors_num = 0
        self.authors = []
        self.doi = ''
        self.year = 0

    def __str__(self):
        info = "Title: " + self.title + "\ndoi: " + self.doi + "\nyear: " + str(self.year)
        return info


class Author:
    def __init__(self, author_name):
        self.name = author_name
        self.country = ''
        self.affiliation = ''
        self.papers = []
        self.alternative_names = []
        self.is_fae = False


# Read the data from CSV file
def read_csv(file, split=','):
    data = []
    csv_file = open(file, "r")
    line = csv_file.read().split("\n")
    for row in line:
        if row != "":
            data.append(row.split(split))
    return data


def getBibTex(query):
    bibtex_list = []
    paper_list = []

    bibtex = urllib.urlopen('http://inspirehep.net/search?p=' + query + '&of=hx').read()

    # First, find the number of registers
    registers = 0
    html = bibtex.split('\n')
    records_fixed = False
    for line in html:
        if not records_fixed:
            if 'records found' in line:
                record_line = line.split('</strong>')
                record_line.pop()
                registers = int(record_line[0].replace('<strong>', '').replace(',', '').strip())
                records_fixed = True
    if records_fixed == True and registers == 0:
        print "ERROR: something is wrong. \n"
    elif records_fixed == False or registers == 0:
        print "WARNING: Sorry, no records found. \n"
    else:
        print 'Registros: ', registers

    # INSPIRE only shows 250 registers
    aux = 0
    while aux < registers:
        bibtex = ''
        url = 'http://inspirehep.net/search?p=' + query.encode('ascii') + '&of=hx&rg=250&jrec='+str(aux)
        bibtex = urllib.urlopen(url.encode('ascii')).read()
        print "url: ", url.encode('ascii')

        # Arrange the info
        bibtex = bibtex.replace('@proceedings', '@article')
        bibtex = bibtex.replace('@inproceedings', '@article')
        bibtex = bibtex.split('@article')
        bibtex.pop(0)
        for entry in bibtex:
            entry = entry.replace('<pre>', '')
            entry = entry.replace('</pre>', '')
            if not '<div style="clear:both">' in entry:
                bibtex_list.append(entry)
            else:
                entry = entry.split('<div style="clear:both">')
                last = entry[0]
                bibtex_list.append(last)
        aux += 250    # Increase the maximum value of registers showed

    for entry in bibtex_list:
        paper = Paper()
        lines = entry.split('\n')
        for line in lines:
            if 'title' in line:
                title = line.replace("title", "").replace("=", "").replace('"', '').replace(",", "").strip()
                paper.title = title
            if 'doi' in line:
                doi = line.replace("doi", "").replace("=", "").replace('"', '').replace(",", "").strip()
                paper.doi = doi
            if 'year' in line:
                year = line.replace("year", "").replace("=", "").replace('"', '').replace(",", "").strip()
                if year.isdigit():
                    paper.year = int(year)
        paper_list.append(paper)

    return paper_list


def make_query_authors(name1, name2=''):
    name1 = name1.strip().replace(' ', '+')
    name2 = name2.strip().replace(' ', '+')

    query = 'find+a+' + name1 + '+and+a+' + name2

    print 'Query: ' + query

    list = getBibTex(query)

    return list


def make_query(query):
    print 'Query: ' + query
    query = query.replace(' ','+')
    list = getBibTex(query)

    return list


def find_signature(name):
    signature = ''
    signature_file = read_csv('investigadores_tiny.txt',';')
    for line in signature_file:
        if name in line[0]:
            signature = line[1]
    return signature


if __name__ == "__main__":
    # list = make_query_authors('Sanchez-Hernandez, A.', 'Ramirez Sanchez')
    #list = make_query('find a Hernandez Villanueva')

    # First, read the authors list
    authors_file = read_csv('RedFAENodes_tiny.csv')
    authors_file.pop(0)

    num_authors = len(authors_file)

    find_signature('Eduard')

    Matrix = [[0 for x in range(num_authors)] for y in range(num_authors)]

    # Make the search of authors
    for author in authors_file:
        for author2 in authors_file:
            if author[0] < author2[0]:

                list = make_query_authors(find_signature(author[1]), find_signature(author2[1]))
                Matrix[int(author[0])][int(author2[0])] = list
                Matrix[int(author2[0])][int(author[0])] = list
                print list
    # print "Lista: ", len(list)
    # print list[0]
