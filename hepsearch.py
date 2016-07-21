import sys, os, getopt, re, urllib

class Paper:
    def __init__(self, paper_name):
        self.title = paper_name
        self.authors_num = 0
        self.authors = []
        self.doi = ''
        self.year = 0


class Author:
    def __init__(self, author_name):
        self.name = author_name
        self.country = ''
        self.affiliation = ''
        self.papers = []
        self.alternative_names = []
        self.is_fae = False



def getBibTex(query):
    paperlist = []

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
                registers = int(record_line[0].replace('<strong>','').replace(',','').strip())
                records_fixed = True
    if records_fixed == True and registers == 0:
        print "ERROR: something is wrong. \n"
    if records_fixed == False or registers == 0:
        print "WARNING: Sorry, no records found. \n"

    bibtex = ''
    bibtex = urllib.urlopen('http://inspirehep.net/search?p=' + query + '&of=hx&rg=250&jrec=0').read()

    # Arrange the info
    bibtex = bibtex.replace('@proceedings','@article')
    bibtex = bibtex.replace('@inproceedings','@article')
    bibtex = bibtex.split('@article')
    bibtex.pop(0)
    for entry in bibtex:
        entry = entry.replace('<pre>','')
        entry = entry.replace('</pre>','')
        if not '<div style="clear:both">' in entry:
            paperlist.append(entry)
        else:
            entry = entry.split('<div style="clear:both">')
            last = entry[0]
            paperlist.append(last)

    for entry in paperlist:
        lines = entry.split('\n')
        for line in lines:
            if 'doi' in line:
                print line.replace("doi","").replace("=","").replace('"','').replace(",git","").strip()


    return paperlist

if __name__ == "__main__":
    list = getBibTex('find+a+Eduard+Burelo')