python source code obfuscator. only obscures strings and integers

>> Installation
   $ git clone https://github.com/zevtyardt/no-strint
   $ cd no-strint
   $ python2 setup.py install or pip install .
   $ strint -h
   
   # via pip, 1.4.5 old version
   $ pip2 install strint

>> Issues
   > https://github.com/zevtyardt/no-strint/issues

>> Basic usage
   $ strint <str> or <int>
   $ strint --obf <filename> 
   $ strint --help

>> Help
   usage: strint [-h] [(--stdout|--exec)] (str|int) [...]
                 [--infile <file> (--obf|--only-strint)]
                 [--outfile <file>] [--with-space] or/and
                 [--eval or (--debug|--verbose)]

   simple str & int obfuscator (c) zvtyrdt.id

   positional arguments:
     STR | INT          strings or integers

   optional arguments:
     -h, --help         show this help message and exit
     -v, --version      show program's version number and exit
     --infile FILE      specify the file name to process
     --outfile FILE     save the results as a file
     --with-space       generate output strings with spaces
     --obf              same as --rand-if, --remove-blanks,
                        --ignore-comments, --indent and --only-strint
                        * default indentation is 1...
     --only-strint      just obfuscate strings and integers
     --encode           convert string to integer before obfuscate
     --stdout           add print function to output (string only)
     --exec             make the output an executable script

   additional:
     if the --only-string option is called

     --rand-if          add a random if statement to the source code
     --indent INDENT    Indentation to use
     --remove-blanks    remove blank lines, instead of obfuscate
     --ignore-comments  remove first block of comments as well

   verbosity / simulation:
     --eval             try running output (experimental)
     --verbose          verbose (debug)
     --debug            enable debug mode