import random

a = 0
b = 1.2
c = 'abc..'
d = 'can\'t'

if c[0] == random.choice(['a', 'b']):
    print ('tes', 'again')
else:
    print (a, b, c, d)

print '\nthis\nnewline\n'

print '\x1b[32mwith \033[34mcolor\033[0m'

print '\twith tab'
