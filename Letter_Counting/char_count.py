#!/usr/bin/python

import sys
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from string import ascii_lowercase

'''Creates bar graph of character frequency of plain text document. 
   Document name should be provide in command line.
   Option to sort by letter count (count) or by English language frequency (wiki).
   Author: Kimberly Fessel, Date: 17 August 2015'''


def make_char_dict( filename ):
    '''Make dictionary of letter frequency of file.  Ignore numbers, symbols, whitespace.'''
    char_dict = {}
    CHAR = re.compile(r'[A-Za-z]')
    with open( filename ) as f:
        for line in f:
            for char in CHAR.findall(line):
                char_dict.setdefault( char, 0 )
                char_dict[ char ] += 1
    return char_dict


def make_table( mydict, sortby ):
    '''Build dataframe with counts of lower- and uppercase letters. 
       Sort by lower+upper count or wikipedia frequency.'''
    mylist = []    
    for c in ascii_lowercase:
        char_tuple = (c.upper(), mydict.get( c, 0 ), mydict.get( c.upper(), 0 ))
        mylist.append( char_tuple )
    chars = pd.DataFrame( mylist, columns = ['letter', 'lower_count', 'upper_count'] )
    chars['total'] = chars.lower_count + chars.upper_count
    if sortby == 'count':
        chars.sort( 'total', inplace=True, ascending=False )
    elif sortby == 'wiki':
        pass
    else:
        print('Please select "count" or "wiki" as option to sort table.')
        sys.exit(0)
    return chars


def wiki_char_percent():
	'''Retrieve character frequency percent from Wikipedia'''
	import urllib2
	from bs4 import BeautifulSoup
	
	address = 'https://en.wikipedia.org/wiki/Letter_frequency'
	url = urllib2.urlopen( address ).read()

	soup = BeautifulSoup(url)
	table = soup.find(attrs={'class': re.compile(r"\bwikitable\b.*")})
	PERCENT = re.compile(r'([0-9\.]+)%')
	nums = [ PERCENT.match(num.text).group(1) for num in table('td', align='right') ]
	return [ float(num) for num in nums ]


def main():
    #Read in filename from user input
    if len(sys.argv) < 2:
        print( 'Please provide plain text document name.' )
        sys.exit(0)
    filename = sys.argv[1]

    #Build character frequency dictionary and dataframe (sorted by option)
    option = 'wiki'
    char_dict = make_char_dict( filename )
    mytable = make_table( char_dict, option )
    
    blue, ltblue = sns.color_palette()[0], sns.color_palette()[5]

    if option == 'count':
        #Plot resulting bar graph of character frequency (by doc count)
        plt.figure()
        ax = mytable.plot( x = 'letter', y=['lower_count', 'upper_count'], 
                          		 kind='bar', stacked=True, color = [blue, ltblue] )
        ax.set_xlabel( 'Character' )
        ax.set_ylabel( 'Count' )
        plt.legend( labels=['Lowercase', 'Uppercase'] )
        plt.show()

    elif option == 'wiki':
        #Import wiki character frequencies and build table (sorted by wiki)
		wiki_percent = wiki_char_percent()
		mytable['wiki'] = pd.Series( wiki_percent ).transpose() * sum( mytable.total ) / 100

		#Plot resulting bar graph of character frequency (by wiki count)
		mytable.sort( 'wiki', inplace=True, ascending=False )
		plt.figure()
		ax = mytable.plot( x = 'letter', y=['lower_count', 'upper_count'],
		                  		kind='bar', stacked=True, color = [blue, ltblue] )
		mytable.plot( x = 'letter', y='wiki', ax = ax, style='r' )
		ax.lines[-1].set_linewidth(4)
		ax.set_xlabel( 'Character' )
		ax.set_ylabel( 'Count' )
		plt.legend( labels=['English Language', 'Lowercase', 'Uppercase'] )
		plt.show()
    
    else:
		print('Please choose "count" or "wiki" option to sort table.')
		sys.exit(0)
		
		
if __name__ == '__main__':
    main()
