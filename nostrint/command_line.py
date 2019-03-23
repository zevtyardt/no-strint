from redat import __version__
import argparse as _argparse
import sys as _sys

def CLI():
    _parser = _argparse.ArgumentParser(usage="%(prog)s [-h] [(--stdout|--exec)] (str|int) [...]\n      {0}  [--infile <file> (--obf|--only-strint)]\n      {0}  [--outfile <file>] [--with-space] or/and\n      {0}  [--eval or (--debug|--verbose)]".format(" " * len(_sys.argv[0].split('/')[-1])),
             description='simple str & int obfuscator (c) zvtyrdt.id',
             formatter_class=_argparse.RawTextHelpFormatter,
             version=__version__)

    _parser.add_argument('txt', metavar='str | int', nargs='*', help='strings or integers')
    _parser.add_argument('--infile', metavar='file', help='specify the file name to process')
    _parser.add_argument('--outfile', metavar='file', help='save the results as a file')
    _parser.add_argument('--with-space', action='store_true', help='generate output strings with spaces')
    _parser.add_argument('--obf', action='store_true', help='same as --rand-if, --remove-blanks,\n--ignore-comments and --only-strint\nor ...')
    _parser.add_argument('--only-strint', action='store_true', help='just obfuscate strings and integers')
    _parser.add_argument('--encode', action='store_true', help='convert string to integer before obfuscate')
    _parser.add_argument('--stdout', action='store_true', help='add print function to output (string only)')
    _parser.add_argument('--exec', action='store_true', dest='_exec', help='make the output an executable script')

    _obfuscate = _parser.add_argument_group('additional', description='if the --only-string option is called')
    _obfuscate.add_argument('--rand-if', action='store_true', help='add a random if statement to the source code')
    _obfuscate.add_argument('--remove-blanks', action='store_true', help='remove blank lines, instead of obfuscate')
    _obfuscate.add_argument('--ignore-comments', action='store_true', help='remove first block of comments as well')


    _verbosity = _parser.add_argument_group('verbosity / simulation')
    _verbosity.add_argument('--eval', action='store_true', dest='_eval', help='try running output (experimental)')
    _verbosity.add_argument('--verbose', action='store_true', help='verbose (debug)')
    _verbosity.add_argument('--debug', action='store_true', help='enable debug mode')

    return _parser
