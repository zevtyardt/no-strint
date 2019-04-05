import sys, time

def run(text, lenght=20, sleep=0.2):
    lenght = len(text) + 5 if lenght < len(text) else lenght
    F = '\r\t[ \x1b[36m{0:>%s}\x1b[0m ] @ zvtyrdt.id ' % lenght

    num = 1
    while True:
        axl = lenght
        while True:
            letters = text[0:num]
            if num > len(text) if lenght < len(text) else lenght:
                letters += ' ' * (num - len(text))
                if num > lenght:
                    letters = letters[num - lenght:axl + num - lenght]
                    axl += 1

                    if axl >= lenght:
                        next_words = text[:axl - lenght]
                        letters = letters[:len(letters) - len(next_words)] + next_words
                        if axl - len(text) == lenght:
                            num = len(text); break

            print (F.format( letters )),; sys.stdout.flush()
            time.sleep(sleep)
            num += 1

if len(sys.argv) < 2:
    sys.argv.append('zevtyardt')
run(' '.join(sys.argv[1:]))
