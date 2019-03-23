from no_strint import strint as _strint
import sys as _sys

def main():
    if _sys.version_info.major != 2:
        _sys.exit('run as python2')
    _strint()

if __name__ == '__main__':
    main()
