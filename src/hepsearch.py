# Functions to obtain the info from Inspirehep.net   -- Michel

import sys, os, getopt, re, urllib2, socket
from html2text import *
import unicodedata
import codecs

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
    def __init__(self, author_name, gender, country = ''):
        self.name = author_name
        self.num_papers = 0
        self.affiliation = ''
        self.signature = find_signature(author_name, True)
        self.is_fae = True
        self.cites = 0
        self.hindex = 0
        self.country = country
        self.gender = gender

    def __str__(self):
        info = "Name: " + self.signature + "\nPublished papers: " + str(self.num_papers) + "\nCites: " + str(self.cites) + \
                "\nhindex: " + str(self.hindex)
        return info

    def get_hindex(self):
        # Make the query in format Cite Summary
        query = 'find a ' + self.signature
        if self.country != '':
            query += ' and cc ' + self.country
        url = 'http://inspirehep.net/search?p=' + query.encode('ascii').replace(' ','+') + '&of=hcs'
        print url
        summary = extract_html(url)

        # Find the h index and cites
        for line in summary.split('\n'):
            if 'hHEP index' in line:
                self.hindex = int(line.split(';')[1].replace(',',''))
            if 'Total number of citations' in line:
                self.cites = int(line.split(';')[1].replace(',',''))
            if 'Total number of papers' in line:
                self.num_papers = int(line.split(';')[1].replace(',',''))


class Country:
    def __init__(self, country_name, country_code ):
        self.name = country_name
        self.code = country_code
        self.num_papers = 0
        self.cites = 0
        self.hindex = 0

    def get_hindex(self):
        # Make the query in format Cite Summary
        query = 'find cc ' + self.code
        url = 'http://inspirehep.net/search?p=' + query.encode('ascii').replace(' ','+') + '&of=hcs'
        print url
        summary = extract_html(url)

        # Find the h index and cites
        for line in summary.split('\n'):
            if 'hHEP index' in line:
                self.hindex = int(line.split(';')[1].replace(',',''))
            if 'Total number of citations' in line:
                self.cites = int(line.split(';')[1].replace(',',''))
            if 'Total number of papers' in line:
                self.num_papers = int(line.split(';')[1].replace(',',''))

    def __str__(self):
        info = "Name: " + self.name + "\nCode:" + self.code +  "\nPublished papers: " + str(self.num_papers) +\
               "\nCites: " + str(self.cites) + "\nhindex: " + str(self.hindex)
        return info



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

    bibtex = None
    while bibtex is None:
        try:
            bibtex = urllib2.urlopen('http://inspirehep.net/search?p=' + query + '&of=hx', timeout=100).read()
        except urllib2.URLError as e:
            print str(e)
            print "Retry..."
        except socket.timeout as e:
            print str(e)
            print "Retry..."
            

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
        bibtex = None
        url = 'http://inspirehep.net/search?p=' + query.encode('ascii') + '&of=hx&rg=250&jrec='+str(aux)
        while bibtex is None:
            try:
                bibtex = urllib2.urlopen(url.encode('ascii'), timeout=100).read()
            except urllib2.URLError as e:
                print str(e)
                print "Retry..."
            except socket.timeout as e:
                print str(e)
                print "Retry..."

            
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


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


# Gets node in format [id, name, signatures]. Returns signatures
def check_signature(node, all = False):
    if node[2].strip() != '':
        signatures = node[2].split(';')
        if len(signatures) == 1 or not all:
            return signatures[0].strip()
        # If all = True, join all signatures with 'or' operand
        signature = signatures[0].strip()
        for x in range(1, len(signatures) - 1):
            signature += ' or ' + signatures[x].strip()
        return signature

    # If there is no signature, make the 'Lastname, Name' format
    [first, last] = node[1].split(".")
    signature = last.replace("-", " ") + ", " + first
    return signature




def find_signature(name, all = False):
    signature = ''
    members_file = read_csv('MiembrosRedFAE2017.csv',';')
    for line in members_file:
        if name in line[0]:
            if len(line) == 2:
                signature = line[1]
            # Connect the signatures with 'or' operand
            elif len(line) > 2:
                signature = line[1]
                if all:
                    for x in range(2, len(line)):
                        if line[x] != '':
                            signature += ' or ' + line[x]
    # If there is no signature, make the 'Lastname, Name' format
    if signature == '':
        sig = name.split('.')
        if len(sig) == 2:
            signature = sig[1] + ', ' + sig[0]+ '.'
        elif len(sig) == 1:
            signature = sig[0]
        elif len(sig) > 2:
            signature = sig[len(sig)-1] + ', ' + sig[0] + '.' + sig[1] + '.'
    return strip_accents(signature)





