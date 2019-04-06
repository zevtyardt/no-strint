from redat import __version__
import argparse as _argparse
import sys as _sys

def CLI():
    _parser = _argparse.ArgumentParser(
        description='simple str & int obfuscator (c) zvtyrdt.id',
        formatter_class=_argparse.RawTextHelpFormatter,
        version=__version__)

    _parser.add_argument('txt', metavar='STR | INT', nargs='*', help='strings or integers')
    _parser.add_argument('-i', '--infile', metavar='FILE', help='specify the file name to process')
    _parser.add_argument('-o', '--outfile', metavar='FILE', help='save the results as a file')
    _parser.add_argument('-w', '--with-space', action='store_true', help='generate output strings with spaces')
    _parser.add_argument('--obf', action='store_true', help='same as --rand-if, --remove-blanks,\n--ignore-comments, --indent and --only-strint\n* default indentation is 1...')
    _parser.add_argument('-O', '--only-strint', action='store_true', help='just obfuscate strings and integers')
    _parser.add_argument('-e', '--encode', action='store_true', help='convert string to integer before obfuscate')
    _parser.add_argument('-s', '--stdout', action='store_true', help='add print function to output (string only)')
    _parser.add_argument('-x', '--exec', action='store_true', dest='_exec', help='make the output an executable script')

    _obfuscate = _parser.add_argument_group('additional', description='if the --only-string option is called')
    _obfuscate.add_argument('-r', '--rand-if', action='store_true', help='add a random if statement to the source code')
    _obfuscate.add_argument('-n', '--indent', help='Indentation to use', type=int)
    _obfuscate.add_argument('-b', '--remove-blanks', action='store_true', help='remove blank lines, instead of obfuscate')
    _obfuscate.add_argument('-c', '--ignore-comments', action='store_true', help='remove first block of comments as well')

    _verbosity = _parser.add_argument_group('verbosity / simulation')
    _verbosity.add_argument('-E', '--eval', action='store_true', dest='_eval', help='try running output (experimental)')
    _verbosity.add_argument('-V', '--verbose', action='store_true', help='verbose (debug)')
    _verbosity.add_argument('-D', '--debug', action='store_true', help='enable debug mode')

    return _parser
