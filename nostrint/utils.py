from redat import OPER, __version__
from random import choice as C, randrange as R
import sys
import string
import time

class utils:
    def convertSize(self, n, format='%(value).1f %(symbol)s', symbols='customary'):
        SYMBOLS = {
            'customary': ('B', 'K', 'Mb', 'G', 'T', 'P', 'E', 'Z', 'Y'),
            'customary_ext': ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                              'zetta', 'iotta'),
            'iec': ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
            'iec_ext': ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                        'zebi', 'yobi'),
            }
        n = int(n)
        if n < 0:
            raise ValueError("n < 0")
        symbols = SYMBOLS[symbols]
        prefix = {}
        for i, s in enumerate(symbols[1:]):
            prefix[s] = 1 << (i + 1) * 10
        for symbol in reversed(symbols[1:]):
            if n >= prefix[symbol]:
                value = float(n) / prefix[symbol]
                return format % locals()

        return format % dict(symbol=symbols[0], value=n)

    def sep(self, x):
        """separating every line"""
        print ('----- {0:-<35}'.format((x + ' ').upper()))

    def savefile(self, x, o):
        """Save Result into the file"""
        self.sep('save')
        with open(o, 'w') as f:
            f.write('#    _   @ {}\n#   (o)\n#  (_|_) <no strint> {} @ zvtyrdt.id\n#   |||  (https://github.com/zevtyardt)\n\n{}'.format(time.strftime('%c'), __version__, x))
        sys.exit('all done (%s).. saved as %s' % (self.convertSize(len(x) + 124), o))

    def fixing(self, x):
        """Remove spacebar and fix syntax"""
        x = x.replace(' ', '') # remove space
        for spec in ['if', 'else', 'for', 'in']:
            x = x.replace(spec, ' {} '.format(spec))
        x = x.replace('lambda_', 'lambda _')
        x = x.replace('jo in ', 'join')
        return x

    # <-- randomize -->
    def _random_str(self, lenght=10):
        """Create random text"""
        return '"{}"'.format(
            ''.join([C(string.ascii_letters) for _ in range(lenght)])
        )

    def rand_if(self, space_lenght=0):
       """Create a randomized stat if"""
       space, if_st = ' ' * space_lenght, ""
       # <-- generate -->
       def gen_fake_stdout():
           expr = []
           for _ in range(R(1, 3)):
               if C([True, False]):
                   expr.append(self._random_str(R(1, 20)))
               else:
                   expr.append('{0} {1} {2}'.format(R(1, 100), C(OPER), R(1, 100)))
           return '\n{0}    print '.format(space).join(expr)
       def gen_fake_if():
           if C([True, False]):
               return self._random_str(5), '!='
           else:
               return R(1, 100), '-'

       el = ''
       for i in range(R(1, 4)):
           var, OP = gen_fake_if()
           if_st += '{0}{1}if {2} {3} {2} : \n{0}    print {4}\n'.format(
               space, el, var, OP, gen_fake_stdout())
           if C([True, False]):
               space = space + (' ' * 4)
               el = ''
           else:
               if i != 1:
                   el = 'el'
       # <-- done -->
       return if_st[:-1]