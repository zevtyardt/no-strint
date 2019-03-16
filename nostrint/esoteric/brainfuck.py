def char2bf(char):
    result_code = ""
    ascii_value = ord(char)
    factor = ascii_value / 10
    remaining = ascii_value % 10

    result_code += str("+" * 10)
    result_code += "["
    result_code += ">"
    result_code += str("+" * factor)
    result_code += "<"
    result_code += "-"
    result_code += "]"
    result_code += ">"
    result_code += str("+" * remaining)
    result_code += "."
    result_code += "[-]"
    return result_code

def obfuscate(string):
    result = ""
    for char in string:
        result += char2bf(char)
    return result

