from redat import __version__
import argparse
import sys

def CLI():
    parser = argparse.ArgumentParser(usage="%(prog)s [-h] [(--stdout|--exec)] (str|int) [...]\n      {0}  [--infile <file> [--only-strint]] [--outfile <file>]\n      {0}  [--no-space] [--eval or (--debug|--verbose)]\n      {0}  [--jsfuck or 'one of the esoteric language choices']".format(" " * len(sys.argv[0].split('/')[-1])),
             description='simple str & int obfuscator (c) zvtyrdt.id',
             formatter_class=argparse.RawTextHelpFormatter,
             version=__version__)

    parser.add_argument('txt', metavar='str | int', nargs='*', help='string or interger')
    parser.add_argument('--infile', metavar='file', help='specify the file name to process')
    parser.add_argument('--outfile', metavar='file', help='save the results as a file')
    parser.add_argument('--with-space', action='store_false', help='generate output strings with spaces')
    parser.add_argument('--only-strint', action='store_true', help='just obfuscate strings and integers')
    parser.add_argument('--encode', action='store_true', help='convert string to integer before obfuscate')
    parser.add_argument('--stdout', action='store_true', help='add print function to output (string only)')
    parser.add_argument('--exec', action='store_true', dest='_exec', help='make the output an executable script')

    algorithm = parser.add_argument_group('esoteric language', description='* program will disable all options, except [(str|int) and --infile]')
    algorithm.add_argument('--jsfuck', action='store_true', help='string conversion into subsets of JavaScript\nsee https://jsfuck.com')
    algorithm.add_argument('--brainfuck', action='store_true', help='convert a char to brainfuck code\nsee https://esolangs.org/wiki/brainfuck')

    verbosity = parser.add_argument_group('verbosity / simulation')
    verbosity.add_argument('--eval', action='store_true', dest='_eval', help='try running output (experimental)')
    verbosity.add_argument('--verbose', action='store_true', help='verbose (debug)')
    verbosity.add_argument('--debug', action='store_true', help='enable debug mode')

    return parser
