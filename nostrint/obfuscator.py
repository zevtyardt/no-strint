from random import choice as _choice
from math import ceil as _ceil, log as _log
from template import *
from redat import *
from reindent import reindenter
import tokenize as _tokenize
import re as _re

# <-- simple obfuscator -->
class obfuscator(object):
    def __init__(self, arg, _utils, ens):
        self.arg = arg
        self._utils = _utils
        self.en_words = ens

    def sub_obfus(self, num):
        res = []
        if self.arg.debug:
            self._utils.sep('obfuscate number')
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
                    _choice(INTER), _choice(OPER), _choice(INTER), _choice(['-', '+', '*']))
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
            span = int(_ceil(_log(abs(num), 1.5))) + (16 >> depth)
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
            template = _choice(ZERO_BASE)
        else:
            template = _choice(NULL_STR)
        return template.format(self.convert(0), self.en_words(x))

    def encode_base(self, x):
        return _choice(ENCODE_BASE).format(self.convert(256), self.convert(0), self.convert(encode(x)))

    def _space(self, x):
        return len(_re.findall(r'^[ ]*', x)[0])

    # <-- rebuild script -->
    def _remove_blanks(self, f):
        return '\n'.join([_ for _ in f.splitlines() if _re.sub(r'^[ ]*', '', _) not in ["\n", ""]])

    def _remove_comments(self, f):
        fm = []
        for _ in f.splitlines():
            if not _re.search(r'["\']', _):
                _ = _re.sub(r'(#.*?(?:\n|$))', '', _)
            fm.append(_)
        return '\n'.join(fm)

    def clear_text(self, file):
        f = open(file).read()
        for i in _re.findall(r'(?si)(["\']{3}.*?["\']{3})', f):
            f = f.replace(i, repr(i)[3:-3])
        if self.arg.ignore_comments:
            f = self._remove_comments(f)
        if self.arg.remove_blanks:
            f = self._remove_blanks(f)
        return f.splitlines()

    def generate_new_script(self):
        PREVIOUS = ''
        if self.arg.debug:
            self._utils.sep('remake script')
            print('filename -> {}'.format(self.arg.infile))
        f = self.clear_text(self.arg.infile)
        for num, i in enumerate(f):
            if i not in ('\n', ""):
                if self.arg.rand_if:
                    if _choice([True, False]):
                        if i[-1] not in EXTH:
                            if num + 1 < len(f):
                                if len(f[num + 1]) > 0:
                                    if _re.sub('^[ ]*', "", f[num + 1])[0] in EXCH or \
                                      'else' in f[num + 1]:
                                        continue
                            jm = self._space(i)
                            if "".join([_ for _ in i[jm:] if _ in EXCH]) == i[jm:] or \
                              i[jm:][0] in EXCH:
                                continue
                            if len(f[num - 1]) > 0:
                                if f[num - 1][-1] in EXTH:
                                    if self._space(f[num - 1]) != jm:
                                        continue
                                    if i[-1] in EXCH:
                                        continue
                            if_stat = self._utils.rand_if(jm)
                            if i in [PREVIOUS, f[num - 1]]:
                                if_stat = '{}el{}'.format(' ' * jm, if_stat[jm:])
                            if self.arg.debug:
                                self._utils.sep('added')
                                print('{} -> line {}'.format(if_stat[jm:], num + 1))
                            # <-- update -->
                            PREVIOUS, _INDEX = if_stat, 1
                            if 'return' in i or 'yield' in i:
                                _INDEX = 0
                            f.insert(num + _INDEX, if_stat)
        f = '\n'.join(f).splitlines()
        if self.arg.indent:
            r = reindenter(f, self.arg.indent)
            return ''.join(r.run())
        return '\n'.join(f)

    def rebuild(self):
        if self.arg.rand_if or self.arg.remove_blanks:
            f = self.generate_new_script()
        else:
            f = open(self.arg.infile).read()
        res = [] # list
        for i in _tokenize.generate_tokens(iter(f.splitlines(1)).next):
            i = list(i)
            ifer = i[0] in (_tokenize.NUMBER, _tokenize.STRING)
            if ifer:
                if self.arg.debug or self.arg.verbose:
                    self._utils.sep('original strint')
                    print(i[1])
            if i[0] == _tokenize.STRING:
                new = i[1][2 if i[1][0] not in ('\'', '"') else 1 : -1]
                if i[1][0] in ('\'', '"'):
                    new = new.decode('string_escape')
                if self.arg.encode:
                    i[1] = self.encode_base(new)
                else:
                    i[1] = self.zero_base(new)
            elif i[0] == _tokenize.NUMBER:
                if '.' in i[1]:
                    i[1] = 'float ( {} )'.format(self.zero_base(i[1]))
                else:
                    i[1] = self.convert(int(i[1]))
            if ifer:
                if not self.arg.with_space:
                    i[1] = self._utils.fixing(i[1])
                if self.arg.debug or self.arg.verbose:
                    self._utils.sep('temp')
                    print(i[1])
            res.append(tuple(i))
        return _tokenize.untokenize(res)
