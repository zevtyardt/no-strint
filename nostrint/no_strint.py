#!usr/bin/python2
# -*- encoding:utf-8 -*-

"""

main program

"""

# <-- modules -->
from utils import utils
from tokenize import *
from template import *
from random import choice as C, randrange as R
from math import ceil, log
from redat import *
import command_line
import sys
import re
import token

# <-- settings -->
reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(999999999)

# <-- encoding -->
def encode(string_):
    """Change String to Integers"""
    return (lambda f, s: f(list( ord(c) for c in str(string_) ) , \
            s))(lambda f, s: sum(f[i] * 256 ** i for i in \
            range(len(f))), str(string_))

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
        if x != '':
            template = C(ZERO_BASE)
        else:
            template = C(NULL_STR)
        return template.format(self.convert(0), self.en_words(x))

    def encode_base(self, x):
        return C(ENCODE_BASE).format(self.convert(256), self.convert(0), self.convert(encode(x)))

    def _space(self, x):
        _t = 0
        while x[_t].isspace():
            _t += 1
        return _t

    # <-- rebuild script -->
    def clear_text(self, file):
        f = open(file).read()
        for i in re.findall(r'(?si)(["\']{3}.*?["\']{3})', f):
            f = f.replace(i, repr(i)[3:-3])
        if self.arg.ignore_comments:
            f = re.sub('#.*?\n', '', f)
        if self.arg.remove_blanks:
            f = re.sub('\n\n', '\n', f)
        return f.splitlines()

    def generate_new_script(self):
        prev = ''
        if self.arg.debug:
            self.utils.sep('remake script')
            print('filename -> {}'.format(self.arg.infile))
        f = self.clear_text(self.arg.infile)
        for num, i in enumerate(f):
            if i not in ('\n', ""):
                if self.arg.rand_if:
                    if C([True, False]):
                        if i[-1] not in EXTH:
                            if num + 1 < len(f):
                                if len(f[num + 1]) > 0:
                                    if f[num + 1][0] in EXCH or 'else' in f[num + 1]:
                                        continue
                            jm = self._space(i)
                            if len(f[num - 1]) > 0:
                                if f[num - 1][-1] in EXTH:
                                    if self._space(f[num - 1]) != jm:
                                        continue
                                    if i[-1] in EXCH:
                                        continue
                            if_stat = self.utils.rand_if(jm)
                            if prev == i or prev == f[num - 1]:
                                if_stat = '{}el{}'.format(' ' * jm, if_stat[jm:])
                            if self.arg.debug:
                                self.utils.sep('added')
                                print('{} -> line {}'.format(if_stat[jm:], num + 1))
                            # <-- update -->
                            prev = i
                            indx = 1
                            if 'return' in i or 'yield' in i:
                                indx = 0
                            f.insert(num + indx, if_stat)
        return '\n'.join(f)

    def rebuild(self):
        if self.arg.rand_if or self.arg.remove_blanks:
            f = self.generate_new_script()
        else:
            f = open(self.arg.infile).read()
        res = [] # list
        for i in generate_tokens(iter(f.splitlines(1)).next):
            i = list(i)
            if token.tok_name[i[0]] in ('NUMBER', 'STRING'):
                if self.arg.debug or self.arg.verbose:
                    self.utils.sep('original strint')
                    print(i[1])
            if token.tok_name[i[0]] == 'STRING':
                new = i[1][2 if i[1][0] not in ('\'', '"') else 1 : -1]
                if i[1][0] in ('\'', '"'):
                    new = new.decode('string_escape')
                if self.arg.encode:
                    i[1] = self.encode_base(new)
                else:
                    i[1] = self.zero_base(new)
            elif token.tok_name[i[0]] == 'NUMBER':
                if '.' in i[1]:
                    i[1] = 'float ( {} )'.format(self.zero_base(i[1]))
                else:
                    i[1] = self.convert(int(i[1]))
            if token.tok_name[i[0]] in ('NUMBER', 'STRING'):
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
        if self.arg.txt or self.arg.infile:
            if self.arg.only_strint:
                if self.arg.infile:
                    compile(open(self.arg.infile).read(), '<string>', 'exec') # cek source code
                    _fin = self.obfuscator.rebuild()
                    if self.arg.debug or self.arg._eval or self.arg.verbose:
                        self.utils.sep('result')
                    print(_fin)
                    if self.arg.outfile:
                        self.utils.savefile(_fin, self.arg.outfile)
                else:
                    self.parser.error('argument --infile is required')
            else:
                _text = self.re_text()
                if self.arg.verbose or self.arg.debug or self.arg._eval:
                    self.utils.sep('original strint')
                    print(_text)
                _text = _text.decode('string_escape')
                if not _text.isdigit():
                    if self.arg.encode:
                        _fin = self.obfuscator.encode_base(_text)
                    else:
                        _fin = self.obfuscator.zero_base(_text)
                    # <-- next -->
                    if self.arg.stdout:
                        _fin = C(STDOUT_BASE).format(self.obfuscator.convert(1), self.obfuscator.convert(2), self.obfuscator.convert(5), self.obfuscator.convert(8), _fin)
                    elif self.arg._exec:
                        _fin = C(EXEC_BASE).format(self.obfuscator.zero_base('<string>'), self.obfuscator.zero_base('exec'), self.obfuscator.convert(1), self.obfuscator.convert(95), self.obfuscator.zero_base(_text), self.obfuscator.convert(0))
                # <-- NOT -->
                else:
                    _fin = self.obfuscator.convert(int(_text))
                if self.arg.debug or self.arg._eval or self.arg.verbose:
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
        if self.arg.obf:
            self.arg.only_strint = True
            self.arg.ignore_comments = True
            self.arg.remove_blanks = True
            self.arg.rand_if = True
        if self.arg._exec:
            self.arg.encode = False

    def re_text(self):
        _txt = ' '.join(self.arg.txt)
        if self.arg.infile:
            _txt = open(self.arg.infile).read()
        return _txt

    def en_words(self, x):
        return ' , '.join(map(self.obfuscator.convert, map(ord, str(x))))
