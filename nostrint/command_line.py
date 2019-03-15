from redat import __version__
import argparse
import sys

def CLI():
    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [(--stdout|--exec)] (str|int) [...]\n      {0}  [--infile <file> [--only-strint]] [--outfile <file>]\n      {0}  [--no-space] [--eval or (--debug|--verbose)]'.format(" " * len(sys.argv[0].split('/')[-1])),
             description='simple str & int obfuscator',
             formatter_class=argparse.RawTextHelpFormatter,
             version=__version__)
    parser.add_argument('txt', metavar='str | int', nargs='*',
             help='string or interger')
    parser.add_argument('--infile', metavar='file',
            help='specify the file name to process')
    parser.add_argument('--outfile', metavar='file',
            help='save the results as a file')
    parser.add_argument('--no-space', action='store_true',
            help='generate output strings without spaces')
    parser.add_argument('--only-strint', action='store_true',
            help='just obfuscate strings and integers')
    parser.add_argument('--encode', action='store_true',
            help='convert string to integer before obfuscate')
    parser.add_argument('--stdout', action='store_true',
            help='add print function to output (string only)')
    parser.add_argument('--exec', action='store_true', dest='_exec',
            help='make the output an executable script')
    parser.add_argument('--eval', action='store_true', dest='_eval',
            help='try running output (experimental)')
    parser.add_argument('--verbose', action='store_true',
            help='verbose (debug)')
    parser.add_argument('--debug', action='store_true',
            help='enable debug mode')

    return parser
