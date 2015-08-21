## PROJECT EULER ## PROBLEM 4 ##

'''Find the largest palidrome made from 
    the product of two 3-digit numbers.
   Author: Kimberly Fessel, 20 August 15'''


def isPalindrome( num ):
    a = str( num )
    for i in range( len(a)/2 ):
        if a[i] != a[-(i+1)]: return False
    return True

#Initialize variables and empty dictionary for palidrome storage
pals = {}
lower = 100
upper = 999
i = upper
j = upper

#Check each product starting with upper values.  
#If palindrome, store in dictionary.
while j >= lower + (upper - lower)/2.:
    while i >= lower:
        if isPalindrome( i*j ):
            pals[ i*j ] = (i, j)
        i -= 1
    i = upper
    j -= 1

a,b = pals[ max(pals) ]

print "The largest palindrome product of two 3-digit numbers is %d.\n\
It is the product of %d and %d." %( max(pals), a, b )
