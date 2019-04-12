python source code obfuscator. only obscures strings and integers

>> Installation
$ git clone https://github.com/zevtyardt/no-strint
$ cd no-strint
$ python2 setup.py install or pip install .
$ strint -h

# via pip
$ pip2 install strint

>> Issues
> https://github.com/zevtyardt/no-strint/issues

>> Basic usage
$ strint <str> or <int>
$ strint --obf -i <filename> 
$ strint --help

>> Help
usage: strint [-h] [-v] [-i FILE] [-o FILE] [-w] [--obf] [-O] [-e] [-s] [-x]
              [-r] [-n INDENT] [-b] [-c] [-E] [-V] [-D]
              [STR | INT [STR | INT ...]]

simple str & int obfuscator (c) zvtyrdt.id

positional arguments:
  STR | INT             strings or integers

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i FILE, --infile FILE
                        specify the file name to process
  -o FILE, --outfile FILE
                        save the results as a file
  -w, --with-space      generate output strings with spaces
  --obf                 same as --rand-if, --remove-blanks,
                        --ignore-comments, --indent and --only-strint
                        * default indentation is 1...
  -O, --only-strint     just obfuscate strings and integers
  -e, --encode          convert string to integer before obfuscate
  -s, --stdout          add print function to output (string only)
  -x, --exec            make the output an executable script

additional:
  if the --only-string option is called

  -r, --rand-if         add a random if statement to the source code
  -n INDENT, --indent INDENT
                        Indentation to use
  -b, --remove-blanks   remove blank lines, instead of obfuscate
  -c, --ignore-comments
                        remove first block of comments as well

verbosity / simulation:
  -E, --eval            try running output (experimental)
  -V, --verbose         verbose (debug)
  -D, --debug           enable debug mode
