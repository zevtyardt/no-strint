from math import ceil, log
from random import choice as R
import sys
import re
import argparse

sys.setrecursionlimit(999999999)
if sys.version_info.major != 2:
    sys.exit('run as python2')

banner = '<no strint> 1.3.8 (https://github.com/zevtyardt)'

def sep(x):
    print ('----- {0:-<35}'.format((x + ' ').upper()))

def encode(string):
    return (lambda f, s: f(list( ord(c) for c in str(string) ) , \
             s))(lambda f, s: sum(f[i] * 256 ** i for i in \
            range(len(f))), str(string))

def fix_text(text):
    if only_strint:
        if text[0] in ('r', "u"):
            text = text[1:]
        if text[0] in ('"', "'"):
            text = text[1:]
        if text[-1] in ('"', "'"):
            text = text[:-1]

    return text.replace("\\'", "'").replace('\\"', '"')

def sort(a):
    res = []
    while a:
        m = max([len(i) for i in a])
        for i in a:
            if len(i) == m:
                res.append(i) ; break
        del a[a.index(i)]
    return res

def find_str(li):
    if arg.verbose:
        sep('search string')

    res, final = [], []
    for i in li:
        st = re.findall(r'((?<![\\])[\'"])((?:.(?!(?<![\\])\1))*.?)\1', i)
        if st:
            for i in st:
                if '.join' not in i[1]:
                    res.append(str(i[0] + i[1] + i[0]))

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

    if arg.verbose:
        print ('{} line -> {} string'.format(len(li), len(final)))

    return final

def sub_obfus(num):
    res = []
    inter, oper = [ '{ }', '[ ]', '( )' ], [ '>', '<', '>=', '<=', '!=', '==' ]

    if arg.debug:
        sep('obfuscate number')

    s = [num]
    if num > 3:
        s = [ num / 2 ] * 2
        if sum(s) != num:
            s = s + [ num % 2 ]

    if arg.debug:
        print ('{} -> {}'.format(num, s))

    for i in range(len(s)):
        while True:
            ex = ' '.join(['( {0} {1} {2} ) {3}'.format(R(inter), R(oper), R(inter), R(['-', '+', '*'])) for _ in range(int(s[i]) if int(s[i]) not in (0, 1) else 2)])[:-2]
            if eval(ex) == int(s[i]):
                 res.append('( {} )'.format(ex)) ; break

    if arg.debug:
        for i in res:
            print ('  -> {0}'.format(i))

    return ' + '.join(res)

# <-- https://benkurtovic.com/2014/06/01/obfuscating-hello-world.html -->
# <-- special thanks to Ben Kurtovic -->

def obfuscate(num, depth):
    if num <= 8:
        conf = sub_obfus(num)
        return '( ' + conf + ' )'
    return "( " + convert(num, depth + 1) + " )"

def convert(num, depth=0):
    result = ""
    while num:
        base = shift = 0
        diff = num
        span = int(ceil(log(abs(num), 1.5))) + (16 >> depth)
        for test_base in range(span):
            for test_shift in range(span):
                test_diff = abs(num) - (test_base << test_shift)
                if abs(test_diff) < abs(diff):
                    diff = test_diff
                    base = test_base
                    shift = test_shift

        if result:
            result += " + " if num > 0 else " - "
        elif num < 0:
            base = -base
        if shift == 0:
            result += obfuscate(base, depth)
        else:
            result += "( {} << {} )".format(obfuscate(base, depth),
                                            obfuscate(shift, depth))

        num = diff if num > 0 else -diff

    if len(result.split('<<')) >= 2:
        result = '( ' + result + ' )'

    return result

def parser_args():
    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [(--stdout|--exec)] (str|int) [...]\n       {0} --infile <file> [--only-strint] [--outfile <file>]\n      {0}  --eval or [(--debug|--verbose)]'.format(" " * len(sys.argv[0].split('/')[-1])),
              description=banner, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('txt', metavar='str | int', nargs='*', help='string or interger')
    parser.add_argument('--infile', metavar='file', help='specify the file name to process')
    parser.add_argument('--outfile', metavar='file', help='save the results as a file')
    parser.add_argument('--only-strint', action='store_true', help='just obfuscate strings and integers (experimental)')
    parser.add_argument('--encode', action='store_true', help='convert string to integer before obfuscate (experimental)')
    parser.add_argument('--stdout', action='store_true', help='add print function to output (string only)')
    parser.add_argument('--exec', action='store_true', dest='_exec', help='make the output an executable script')
    parser.add_argument('--eval', action='store_true', dest='_eval', help='try running output (experimental)')
    parser.add_argument('--verbose', action='store_true', help='verbose (debug)')
    parser.add_argument('--debug', action='store_true', help='enable debug mode')

    return parser

def main():
    global arg, only_strint

    parser = parser_args()
    arg = parser.parse_args()

    if arg._exec:
        arg.encode = False

    only_strint, bs_en = arg.only_strint and arg.infile, arg.encode

    if only_strint:
        arg.encode = False
        arg._exec = False
        arg.stdout = False

    if arg.txt or arg.infile:
        base = [' '.join(arg.txt)]
        if arg.infile:
            base = [open(arg.infile).read()]

        ori = re.sub('(?si)["\']{3}.*?["\']{3}', '', base[0])

        for unix in range(2 if only_strint else 1):
            if only_strint:
                if unix == 0:
                    base = find_str(open(arg.infile).readlines())
                else:
                    base, efa = [], [_ for _ in re.findall(r'([\d.]*)', ori) if not _.startswith('.') and _ != '']
                    for _ in efa:
                        if _ not in base:
                            base.append(_)
            eu = sort([base][0])

            sdh = []
            for text in eu:
                if text in sdh:
                    print ('# skipped: duplicate string'); continue

                sdh.append(text)

                text_old = text
                text = fix_text(text_old)

                if text == '':
                    temp = 'str ( ( lambda : {0} ) . func_code . co_lnotab )'
                    if arg._exec:
                        print ('# can\'t execute NoneType string')
                        arg._exec = False

                if bs_en:
                    arg.encode = True
                    if text.isdigit():
                        print ('# disable encoding string')
                        arg.encode = False

                if arg.debug or arg._eval or arg.verbose:
                    sep('original strint')
                    if not arg.encode:
                        print (text_old)
                    else:
                        print ('{} -> {}'.format(text, encode(text)))

                if arg.encode:
                    text = str(encode(text))

                if text.isdigit() and not arg.encode:
                    if text == '0':
                        temp = sub_obfus(0)
                    else:
                        temp = convert(int(text))
                    if only_strint:
                        temp = 'int ' + temp

                else:
                    B = F = '( ( lambda : {0} ) . func_code . co_lnotab ) . join ( [ chr ( _ ) for _ in [ %s ] ] )'.format(sub_obfus(0))
                    if arg.encode:
                        B = F = '( lambda _ , __ : _ ( _ , __ ) ) ( lambda _ , __ : chr ( __ % {0} ) + _ ( _ , __ // {0} ) if __ else ( ( lambda : {1} ) . func_code . co_lnotab ) , %s )'.format(convert(256), sub_obfus(0))

                    ch = lambda tx: ' , '.join([convert(ord(i)) for i in tx])
                    chg = lambda inf: B.replace('%s', inf)

                    if arg.stdout:
                        if text == '':
                            B = '%s'
                        F = 'getattr ( __import__ ( True . __class__ . __name__ [ {0} ] + [ ] . __class__ . __name__ [ {1} ] ) , ( ) . __class__ . __eq__ . __class__ . __name__ [ : {1} ] + ( ) . __iter__ ( ) . __class__ . __name__ [ {2} : {3} ] ) ( {0}, {4} + chr ( {5} + {5} ) )'.format(sub_obfus(1), sub_obfus(2), sub_obfus(5), sub_obfus(8), B, sub_obfus(5) )
                    elif arg._exec:
                        F = "( lambda ___ : [ ( eval ( compile ( __ , {0} , {1} ) , None , ___ ) , None ) [ {2} ] for ___[ chr ( {3} ) * {4} ] in [ ( {5} ) ] ] [ {6} ] ) ( globals ( ) )".format(chg(ch('<string>')), chg(ch('exec')), sub_obfus(1), convert(95), sub_obfus(2), B, sub_obfus(0))

                    if text != '':
                        if arg.encode:
                            obfuscate_string = convert(int(text))
                        else:
                            obfuscate_string = ch(text)
                        temp = F.replace('%s', obfuscate_string)

                    else:
                        if arg.stdout:
                            temp = F.replace('%s', temp)

                if only_strint:
                    if '.' in text_old and unix == 1:
                        temp = 'float ( str ( ' + temp + ' ) )'

                    ur = text_old[0]
                    if ur in ('u', 'r'):
                        if ur == 'u':
                            temp = 'u"{}".format ( ' + temp + ' )'
                        if ur == 'r':
                            temp = 'r"{}".format ( ' + temp + ' )'
                    else:
                        if re.search('\\\\n', repr(text_old)):
                            temp = "'\\n' . join ( ( {} ) . split('\\\\n') )".format(temp)

                    if arg.verbose or arg.debug:
                        sep('temp')
                        print (temp)

                    ori = ori.replace(text_old, temp)

                else:
                    final = temp

        final = ori if only_strint else final
        if arg.debug or arg._eval or arg.verbose:
            sep('result')

        print (final)

        if not only_strint:
            if arg.debug or arg._eval:
                sep('eval')
                print (eval(final))

        if arg.outfile:
            sep('save')
            open(arg.outfile, 'w').write(final)
            print ('all done.. saved as %s' % arg.outfile)
    else:
        print (banner)
        parser.print_usage()

if __name__ == '__main__':
    main()
