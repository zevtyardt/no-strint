#!usr/bin/python2
# -*- encoding:utf-8 -*-

"""

main program

"""

# <-- modules -->
from tokenize import *
from template import *
from random import choice as C, randrange as R
from math import ceil, log
from esoteric import brainfuck
from esoteric import jsfuck
from redat import *
import command_line
import sys
import string
import re

# <-- settings -->
sys.setrecursionlimit(999999999)

# <-- data -->
INTER = [ '{ }', '[ ]', '( )' ]
OPER = [ '>', '<', '>=', '<=', '!=', '==' ]

# <-- encoding -->
def encode(string_):
    """Change String to Integers"""
    return (lambda f, s: f(list( ord(c) for c in str(string_) ) , \
            s))(lambda f, s: sum(f[i] * 256 ** i for i in \
            range(len(f))), str(string_))

# <-- zero_seven -->
class utils:
    def sep(self, x):
        """separating every line"""
        print ('----- {0:-<35}'.format((x + ' ').upper()))

    def savefile(self, x, o):
        """Save Result into the file"""
        self.sep('save')
        with open(o, 'w') as f:
            f.write(x)
        sys.exit('all done (%s bytes).. saved as %s' % (len(x), o))

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
       space = ''
       if space != 0:
           space = ' ' * space_lenght
       return '{0}if {1} {2} {3} : {4}'.format(space, R(1, 100), C(OPER),
           R(1, 100), self._random_str(R(1, 20)))

# <-- simple obfuscator -->
class obfuscator(object):
    def __init__(self, arg, utils, ens):
        self.arg = arg
        self.utils = utils
        self.en_words = ens

    def sub_obfus(self, num):
        res = []
        if self.arg.debug:
            self.utils.sep('obfuscate number')
        s = [num]
        if num > 3:
            s = [ num / 2 ] * 2
            if sum(s) != num:
                s = s + [ num % 2 ]
        if self.arg.debug:
            print ('{} -> {}'.format(num, s))
        for i in range(len(s)):
            while True:
                ex = ' '.join(['( {0} {1} {2} ) {3}'.format(
                    C(INTER), C(OPER), C(INTER), C(['-', '+', '*']))
                    for _ in range(int(s[i]) if int(s[i]) not in (0, 1) else 2)]
                )[:-2]
                if eval(ex) == int(s[i]):
                    res.append('( {} )'.format(ex)) ; break
        if self.arg.debug:
            for i in res:
                print ('  -> {0}'.format(i))
        return ' + '.join(res)

    # <-- thanks to Ben Kurtovic -->
    # <-- https://benkurtovic.com/2014/06/01/obfuscating-hello-world.html -->

    def obfuscate(self, num, depth):
        if num <= 8:
            conf = self.sub_obfus(num)
            return '( ' + conf + ' )'
        return "( " + self.convert(num, depth + 1) + " )"

    def convert(self, num, depth=0):
        if num == 0:
            return self.sub_obfus(0)
        result = ""
        while num:
            base = shift = 0
            diff = num
            span = int(ceil(log(abs(num), 1.5))) + (16 >> depth)
            for test_base in range(span):
                for test_shift in range(span):
                    test_diff = abs(num) - (test_base << test_shift)
                    if abs(test_diff) < abs(diff):
                        diff, base, shift = test_diff, test_base, test_shift
            if result:
                result += " + " if num > 0 else " - "
            elif num < 0:
                base = -base
            if shift == 0:
                result += self.obfuscate(base, depth)
            else:
                result += "( {} << {} )".format(self.obfuscate(base, depth),
                                                self.obfuscate(shift, depth))
            num = diff if num > 0 else -diff
        if len(result.split('<<')) >= 2:
            result = '( ' + result + ' )'
        return result

    # <-- shortcut -->
    def zero_base(self, x):
        return ZERO_BASE.format(self.convert(0), self.en_words(x))

    def encode_base(self, x):
        return ENCODE_BASE.format(self.convert(256), self.convert(0), self.convert(encode(x)))

    # <-- rebuild script -->
    def clear_text(self, file):
        f = open(file).read()
        for i in re.findall(r'(?si)(["\']{3}.*?["\']{3})', f):
            f = f.replace(i, repr(i)[3:-3])
        return f.splitlines()

    def remake(self):
        if self.arg.debug:
            self.utils.sep('remake script')
            print('filename -> {}'.format(self.arg.infile))
        f = self.clear_text(self.arg.infile)
        for num, i in enumerate(f):
            if i not in ('\n', ""):
                if R(1, 5) == 3:
                    if i[-1] not in ('(', ',', ':', '\\'):
                        jm = 0
                        while i[jm].isspace():
                            jm += 1
                        if_stat = self.utils.rand_if(jm)
                        if self.arg.debug:
                            self.utils.sep('added')
                            print('{} -> line {}'.format(if_stat[if_stat.index('if'):], num + 1))
                        f.insert(num + 1, if_stat)
        return '\n'.join(f)

    def rebuild(self):
        f, res = self.remake(), []
        for i in generate_tokens(iter(f.splitlines(1)).next):
            i = list(i)
            if i[0] in (2, 3):
                if self.arg.debug or self.arg.verbose:
                    self.utils.sep('original strint')
                    print(i[1])
            if i[0] == 3:
                new = i[1][2 if i[1][0] not in ('\'', '"') else 1 : -1]
                if i[1][0] in ('\'', '"'):
                    new = new.decode('string_escape')
                if self.arg.encode:
                    i[1] = self.encode_base(new)
                else:
                    i[1] = self.zero_base(new)
            elif i[0] == 2:
                if '.' in i[1]:
                    i[1] = 'float ( {} )'.format(self.zero_base(i[1]))
                else:
                    i[1] = self.convert(int(i[1]))
            if i[0] in (2, 3):
                if not self.arg.with_space:
                    i[1] = self.utils.fixing(i[1])
                if self.arg.debug or self.arg.verbose:
                    self.utils.sep('temp')
                    print(i[1])
            res.append(tuple(i))
        return untokenize(res)

# <-- base -->
class strint(object):
    def __init__(self):
        self.parser = command_line.CLI()
        self.arg = self.parser.parse_args()
        self.utils = utils()
        self.obfuscator = obfuscator(self.arg, self.utils, self.en_words)
        self.set_options()
        self.begin()

    def begin(self):
        algo = {'jsfuck': jsfuck, 'brainfuck': brainfuck}
        if self.arg.txt or self.arg.infile:
            if self.arg.only_strint:
                if self.arg.infile:
                    _fin = self.obfuscator.rebuild()
                    print(_fin)
                    if self.arg.outfile:
                        self.utils.savefile(_fin, self.arg.outfile)
            else:
                _text = self.re_text()
                if self.arg.verbose or self.arg.debug or self.arg._eval:
                    self.utils.sep('original strint')
                    print(_text)
                _text = _text.decode('string_escape')
                for alg in algo:
                    if self.arg.__dict__[alg]:
                        _fin = algo[alg].obfuscate(_text)
                        print(_fin)
                        if self.arg.outfile:
                           self.utils.savefile(_fin, self.arg.outfile)
                        sys.exit(0)
                if not _text.isdigit():
                    if self.arg.encode:
                        _fin = self.obfuscator.encode_base(_text)
                    else:
                        _fin = self.obfuscator.zero_base(_text)
                    # <-- next -->
                    if self.arg.stdout:
                        _fin = STDOUT_BASE.format(self.obfuscator.convert(1), self.obfuscator.convert(2), self.obfuscator.convert(5), self.obfuscator.convert(8), _fin)
                    elif self.arg._exec:
                        _fin = EXEC_BASE.format(self.obfuscator.zero_base('<string>'), self.obfuscator.zero_base('exec'), self.obfuscator.convert(1), self.obfuscator.convert(95), self.obfuscator.zero_base(_text), self.obfuscator.convert(0))
                # <-- NOT -->
                else:
                    _fin = self.obfuscator.convert(int(_text))
                if self.arg.debug or self.arg._eval:
                    self.utils.sep('result')
                if not self.arg.with_space:
                    _fin = self.utils.fixing(_fin)
                print(_fin)
                if self.arg._eval:
                    self.utils.sep('eval')
                    print(eval(_fin))
                if self.arg.outfile:
                    self.utils.savefile(_fin, self.arg.outfile)
        else:
            print (BANNER)
            self.parser.print_usage()

    def set_options(self):
        if self.arg._exec:
            self.arg.encode = False

    def re_text(self):
        _txt = ' '.join(self.arg.txt)
        if self.arg.infile:
            _txt = open(self.arg.infile).read()
        return _txt

    def en_words(self, x):
        return ' , '.join(map(self.obfuscator.convert, map(ord, str(x))))
