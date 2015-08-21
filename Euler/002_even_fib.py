## PROJECT EULER ## PROBLEM 2 ##

'''By considering the terms in the Fibonacci sequence whose values
   do not exceed ___ (4 million), find the sum of the even-valued terms.
   Author: Kimberly Fessel, 26 May 15'''

import sys

if len(sys.argv) < 2: print "Please pass upper limit as argument."
n = int(sys.argv[1])

fib1 = 1
fib2 = 1
efib = 2
sum = 0

while efib < n:
    sum += efib         #Every third Fib number is even.  All others odd.  
    fib1 = fib2 + efib
    fib2 = fib1 + efib
    efib = fib1 + fib2  
print 'The sum of the even Fibonacci terms under %d is %d.' %(n, sum)


