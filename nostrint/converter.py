def nwords(num):
    num = int(num)
    units = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    teens = ['', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',  \
             'seventeen', 'eighteen', 'nineteen']
    tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',  \
            'eighty', 'ninety']
    thousands = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion',  \
                 'quintillion', 'sextillion', 'septillion', 'octillion',  \
                 'nonillion', 'decillion', 'undecillion', 'duodecillion',  \
                 'tredecillion', 'quattuordecillion', 'sexdecillion',  \
                 'septendecillion', 'octodecillion', 'novemdecillion',  \
                 'vigintillion']
    words = []
    if num==0: words.append('zero')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = (numStrLen+2)/3
        numStr = numStr.zfill(groups*3)
        for i in range(0, groups*3, 3):
            h, t, u = int(numStr[i]), int(numStr[i+1]), int(numStr[i+2])
            g = groups-(i/3+1)
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1:
                    words.append(units[u])
            elif t==1:
                if u>=1:
                    words.append(teens[u])
                else:
                    words.append(tens[t])
            else:
                if u>=1:
                    words.append(units[u])
            if (g>=1) and ((h+t+u)>0):
                words.append(thousands[g])
    return '_' + '_'.join(words)

def wints(textnum,  numwords={}):
    if not numwords:
      units = [
        "zero",  "one",  "two",  "three",  "four",  "five",  "six",  "seven",  "eight", 
        "nine",  "ten",  "eleven",  "twelve",  "thirteen",  "fourteen",  "fifteen", 
        "sixteen",  "seventeen",  "eighteen",  "nineteen", 
      ]
      tens = ["",  "",  "twenty",  "thirty",  "forty",  "fifty",  "sixty",  "seventy",  "eighty",  "ninety"]
      scales = ['hundred', 'thousand', 'million', 'billion', 'trillion', 'quadrillion',  \
                 'quintillion', 'sextillion', 'septillion', 'octillion',  \
                 'nonillion', 'decillion', 'undecillion', 'duodecillion',  \
                 'tredecillion', 'quattuordecillion', 'sexdecillion',  \
                 'septendecillion', 'octodecillion', 'novemdecillion',  \
                 'vigintillion']

      numwords["and"] = (1,  0)
      for idx,  word in enumerate(units):    numwords[word] = (1,  idx)
      for idx,  word in enumerate(tens):     numwords[word] = (1,  idx * 10)
      for idx,  word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2),  0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale,  increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

#print nwords(''.join(getattr(__import__('sys'), 'argv')[1:]))
