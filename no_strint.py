from math import ceil, log
from random import choice as R
import sys
import re
import argparse

sys.setrecursionlimit(999999999)
if sys.version_info.major != 2:
    sys.exit('run as python2')
banner = '<no strint> 1.4.3 (https://github.com/zevtyardt)'

def encode(string):
    return (lambda f, s: f(list( ord(c) for c in str(string) ) , \
             s))(lambda f, s: sum(f[i] * 256 ** i for i in \
            range(len(f))), str(string))

def command_line():
    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [(--stdout|--exec)] (str|int) [...]\n      {0}  --infile <file> [--only-strint] [--outfile <file>]\n      {0}  [--no-space] [--eval or [(--debug|--verbose)]]'.format(" " * len(sys.argv[0].split('/')[-1])),
              description=banner, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('txt', metavar='str | int', nargs='*', help='string or interger')
    parser.add_argument('--infile', metavar='file', help='specify the file name to process')
    parser.add_argument('--outfile', metavar='file', help='save the results as a file')
    parser.add_argument('--no-space', action='store_true', help='generate output strings without spaces')
    parser.add_argument('--only-strint', action='store_true', help='just obfuscate strings and integers')
    parser.add_argument('--encode', action='store_true', help='convert string to integer before obfuscate')
    parser.add_argument('--stdout', action='store_true', help='add print function to output (string only)')
    parser.add_argument('--exec', action='store_true', dest='_exec', help='make the output an executable script')
    parser.add_argument('--eval', action='store_true', dest='_eval', help='try running output (experimental)')
    parser.add_argument('--verbose', action='store_true', help='verbose (debug)')
    parser.add_argument('--debug', action='store_true', help='enable debug mode')
    return parser

class utils:
    def __init__(self, arg):
        self.arg = arg
        self.sep = self._sep

    def _sep(self, x):
        print ('----- {0:-<35}'.format((x + ' ').upper()))

    def findstr(self):
        li = open(self.arg.infile).readlines()
        if self.arg.verbose:
            self.sep('search string')
        res, final = [], []
        for i in li:
            st = re.findall(r'((?<![\\])[\'"])((?:.(?!(?<![\\])\1))*.?)\1', i)
            if st:
                for i in st:
                    if '.join' not in i[1]:
                        sf = str(i[0] + i[1] + i[0])
                        if sf[:2] not in ("''", '""'):
                            res.append(sf)
        for l in res:
            for d in li:
                if l in d:
                    if "r{}".format(l) in d:
                        l = 'r{}'.format(l)
                    elif "u{}".format(l) in d:
                        l = 'u{}'.format(l)
                    break
            if l not in final:
                final.append(l)
        if self.arg.verbose:
            print ('{} line -> {} string'.format(len(li), len(final)))
        return final

    def sort(self, a):
        res = []
        while a:
            m = max([len(i) for i in a])
            for i in a:
                if len(i) == m:
                    res.append(i) ; break
            del a[a.index(i)]
        return res

    def unescape(self, text):
        if self.arg.only_strint and self.arg.infile:
            if text[0] in ('r', "u"):
                text = text[1:]
            if text[0] in ('"', "'"):
                text = text[1:]
            if text[-1] in ('"', "'"):
                text = text[:-1]
            text = text.replace('\\', '\\\\')
        # <-- clear escape character -->
        return text.decode('string_escape')

    def delete_space(self, temp):
        temp = temp.replace(' ', '')
        for rpt in ['for', 'in', 'if', 'else']:
            temp = temp.replace(rpt, ' {} '.format(rpt))
        temp = temp.replace('jo in ', 'join')
        temp = temp.replace('lambda_', 'lambda _')
        temp = temp.replace(' in t', 'int')
        return temp

class obfuscator(object):
    def __init__(self, arg, utils):
        self.arg = arg
        self.utils = utils

    def sub_obfus(self, num):
        res = []
        inter, oper = [ '{ }', '[ ]', '( )' ], [ '>', '<', '>=', '<=', '!=', '==' ]
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
                ex = ' '.join(['( {0} {1} {2} ) {3}'.format(R(inter), R(oper), R(inter), R(['-', '+', '*'])) for _ in range(int(s[i]) if int(s[i]) not in (0, 1) else 2)])[:-2]
                if eval(ex) == int(s[i]):
                    res.append('( {} )'.format(ex)) ; break
        if self.arg.debug:
            for i in res:
                print ('  -> {0}'.format(i))
        return ' + '.join(res)

    # <-- special thanks to Ben Kurtovic -->
    # <-- https://benkurtovic.com/2014/06/01/obfuscating-hello-world.html -->

    def obfuscate(self, num, depth):
        if num <= 8:
            conf = self.sub_obfus(num)
            return '( ' + conf + ' )'
        return "( " + self.convert(num, depth + 1) + " )"

    def convert(self, num, depth=0):
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


class strint(object):
    def __init__(self):
        self.parser = command_line()
        self.arg = self.parser.parse_args()
        self.utils = utils(self.arg)
        self.obfuscator = obfuscator(self.arg, self.utils)
        self.set_options()
        try:
            self.rebuild()
        except Exception as e:
            print ('Traceback: %s' % e)

    def rebuild(self):
        if self.arg.txt or self.arg.infile:
            self.base = self.grep_content()
            self.ori = self.clear_base(self.base[0])
            for unix in range(2 if self.only_strint else 1):
                if self.only_strint:
                    if unix == 0:
                        self.base = self.utils.findstr()
                    else:
                        self.base, efa = [], re.findall(r'([\d.]*)', self.ori)
                        for s in efa:
                            if s not in self.base and not s.startswith('.') and s != '':
                                self.base.append(s)
                eu = self.utils.sort(self.base)
                sdh = []
                for text in eu:
                    if text in sdh:
                        print ('# skipped: duplicate string'); continue
                    sdh.append(text)
                    text_old = text
                    text = self.utils.unescape(text_old)
                    if text == '':
                        temp = 'str ( ( lambda : {0} ) . func_code . co_lnotab )'
                        if self.arg._exec:
                            print ('# can\'t execute NoneType string')
                            self.arg._exec = False
                    if self.bs_en:
                        self.arg.encode = True
                        if text.isdigit():
                            print ('# disable encoding string: int found')
                            self.arg.encode = False
                    if self.arg.encode:
                        text = str(encode(text))
                    if self.arg.debug or self.arg._eval or self.arg.verbose:
                        self.utils.sep('original strint')
                        if not self.arg.encode:
                            print (text_old)
                        else:
                            print ('{} -> {}'.format(text_old, text))
                    if text.isdigit() and not self.arg.encode:
                        if text == '0':
                            temp = self.obfuscator.sub_obfus(0)
                        else:
                            temp = self.obfuscator.convert(int(text))
                        if self.only_strint:
                            temp = 'int ' + temp
                    else:
                        B = F = '( ( lambda : {0} ) . func_code . co_lnotab ) . join ( [ chr ( _ ) for _ in [ %s ] ] )'.format(self.obfuscator.sub_obfus(0))
                        if self.arg.encode:
                            B = F = '( lambda _ , __ : _ ( _ , __ ) ) ( lambda _ , __ : chr ( __ % {0} ) + _ ( _ , __ // {0} ) if __ else ( ( lambda : {1} ) . func_code . co_lnotab ) , %s )'.format(self.obfuscator.convert(256), self.obfuscator.sub_obfus(0))
                        ch = lambda tx: ' , '.join([self.obfuscator.convert(ord(i)) for i in tx])
                        chg = lambda inf: B.replace('%s', inf)
                        if self.arg.stdout:
                            if text == '':
                                B = '%s'
                            F = 'getattr ( __import__ ( True . __class__ . __name__ [ {0} ] + [ ] . __class__ . __name__ [ {1} ] ) , ( ) . __class__ . __eq__ . __class__ . __name__ [ : {1} ] + ( ) . __iter__ ( ) . __class__ . __name__ [ {2} : {3} ] ) ( {0}, {4} + chr ( {5} + {5} ) )'.format(self.obfuscator.sub_obfus(1), self.obfuscator.sub_obfus(2), self.obfuscator.sub_obfus(5), self.obfuscator.sub_obfus(8), B, self.obfuscator.sub_obfus(5) )
                        elif self.arg._exec:
                            F = "( lambda ___ : [ ( eval ( compile ( __ , {0} , {1} ) , None , ___ ) , None ) [ {2} ] for ___[ chr ( {3} ) * {4} ] in [ ( {5} ) ] ] [ {6} ] ) ( globals ( ) )".format(chg(ch('<string>')), chg(ch('exec')), self.obfuscator.sub_obfus(1), self.obfuscator.convert(95), self.obfuscator.sub_obfus(2), B, self.obfuscator.sub_obfus(0))
                        if text != '':
                            if self.arg.encode:
                                obfuscate_string = self.obfuscator.convert(int(text))
                            else:
                                obfuscate_string = ch(text)
                            temp = F.replace('%s', obfuscate_string)
                        else:
                            if self.arg.stdout:
                                temp = F.replace('%s', temp)
                    if self.arg.no_space:
                        temp = self.utils.delete_space(temp)
                    if self.only_strint:
                        reb = None
                        if '.' in text_old and unix == 1:
                            reb = 'float ( str ( %s ) )'
                        ur = text_old[0]
                        if ur == 'u':
                            reb = 'u"{}".format ( %s )'
                        if ur == 'r':
                            reb = 'r"{}".format ( %s )'
                        if reb:
                            if self.arg.no_space:
                                reb = reb.replace(' ', '')
                            temp = reb % temp
                        if self.arg.verbose or self.arg.debug:
                            self.utils.sep('temp')
                            print (temp)
                        self.ori = self.ori.replace(text_old, temp)
                    else:
                        final = temp
            final = self.ori if self.only_strint else final
            if self.arg.debug or self.arg._eval or self.arg.verbose:
                self.utils.sep('result')
            # <-- output -->
            print (final)
            if not self.only_strint:
                if self.arg.debug or self.arg._eval:
                    self.utils.sep('eval')
                    print (eval(final))
            if self.arg.outfile:
                self.utils.sep('save')
                open(self.arg.outfile, 'w').write(final)
                print ('all done.. saved as %s' % self.arg.outfile)
        else:
            print (banner)
            self.parser.print_usage()

    def set_options(self):
        if self.arg._exec:
            self.arg.encode = False
        self.only_strint, self.bs_en = self.arg.only_strint and self.arg.infile, self.arg.encode
        if self.only_strint:
            self.arg.encode = False
            self.arg._exec = False
            self.arg.stdout = False

    def grep_content(self):
        base_ = [' '.join(self.arg.txt)]
        if self.arg.infile:
            base_ = [open(self.arg.infile).read()]
        return base_

    def clear_base(self, base_):
        for i in re.findall('(?s)(["\']{3}.*?["\']{3})', base_):
            base_ = base_.replace(i, '{} # unpack text in three quotes'.format(repr(i)[3:-3]))
        return base_

def main():
    strint()

if __name__ == '__main__':
    main()
