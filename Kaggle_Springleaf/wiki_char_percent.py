import urllib2
from bs4 import BeautifulSoup
import re

def wiki_char_percent():
    address = 'https://en.wikipedia.org/wiki/Letter_frequency'
    url = urllib2.urlopen( address ).read()

    soup = BeautifulSoup(url)
    table = soup.find(attrs={'class': re.compile(r"\bwikitable\b.*")})
    PERCENT = re.compile(r'([0-9\.]+)%')
    nums = [ PERCENT.match(num.text).group(1) for num in table('td', align='right') ]
    return [ float(num) for num in nums ]

