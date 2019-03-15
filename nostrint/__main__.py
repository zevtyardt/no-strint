from no_strint import strint
import sys

def main():
    if sys.version_info.major != 2:
        sys.exit('run as python2')
    strint()

if __name__ == '__main__':
    main()
