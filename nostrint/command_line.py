from redat import __version__
import argparse
import sys

def CLI():
    parser = argparse.ArgumentParser(usage="%(prog)s [-h] [(--stdout|--exec)] (str|int) [...]\n      {0}  [--infile <file> (--obf|--only-strint)]\n      {0}  [--outfile <file>] [--with-space] or/and\n      {0}  [--eval or (--debug|--verbose)]".format(" " * len(sys.argv[0].split('/')[-1])),
             description='simple str & int obfuscator (c) zvtyrdt.id',
             formatter_class=argparse.RawTextHelpFormatter,
             version=__version__)

    parser.add_argument('txt', metavar='str | int', nargs='*', help='strings or integers')
    parser.add_argument('--infile', metavar='file', help='specify the file name to process')
    parser.add_argument('--outfile', metavar='file', help='save the results as a file')
    parser.add_argument('--with-space', action='store_true', help='generate output strings with spaces')
    parser.add_argument('--obf', action='store_true', help='same as --rand-if, --remove-blanks,\n--ignore-comments and --only-strint\nor ...')
    parser.add_argument('--only-strint', action='store_true', help='just obfuscate strings and integers')
    parser.add_argument('--encode', action='store_true', help='convert string to integer before obfuscate')
    parser.add_argument('--stdout', action='store_true', help='add print function to output (string only)')
    parser.add_argument('--exec', action='store_true', dest='_exec', help='make the output an executable script')

    obfuscate = parser.add_argument_group('additional', description='if the --only-string option is called')
    obfuscate.add_argument('--rand-if', action='store_true', help='add a random if statement to the source code')
    obfuscate.add_argument('--remove-blanks', action='store_true', help='remove blank lines, instead of obfuscate')
    obfuscate.add_argument('--ignore-comments', action='store_true', help='remove first block of comments as well')


    verbosity = parser.add_argument_group('verbosity / simulation')
    verbosity.add_argument('--eval', action='store_true', dest='_eval', help='try running output (experimental)')
    verbosity.add_argument('--verbose', action='store_true', help='verbose (debug)')
    verbosity.add_argument('--debug', action='store_true', help='enable debug mode')

    return parser
