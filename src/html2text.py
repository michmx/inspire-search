

import urllib
from bs4 import BeautifulSoup

def extract_html(url):
    html = urllib.request.urlopen(url).read()
    # Make easier to read
    html = html.decode().replace('<td>', '\n').replace('<td align="right">', '; ').replace('</table>', '\n')
    soup = BeautifulSoup(html,"lxml")

    # kill all script
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    # break into lines
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # remove blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text