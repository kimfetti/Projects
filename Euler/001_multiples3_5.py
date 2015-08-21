## PROJECT EULER ## PROBLEM 1 ##

'''Find the sum of all the multiples of 3 or 5 below ___ (1000).
   Author: Kimberly Fessel, 26 May 15'''

import sys

if len( sys.argv ) < 2:
    print "Please pass max value as argument."
n = int(sys.argv[1])

sum = 0
for i in range(1, n):
    if i%3 == 0 or i%5==0:
        sum += i
print 'The sum of all multiples of 3 or 5 below %d is %d.' %(n, sum)


