import unicodedata
from io import BytesIO
from tokenize import tokenize, untokenize, NAME


def normalize_translation_table(table):
    return {unicodedata.normalize('NFKC', k): v for k, v in table.items()}


def reverse_translation_table(table):
    return {v: k for k, v in table.items()}


def lines_to_readline(lines):
    """
    Turns a list of code lines into a file-like object to use with tokenize()
    """
    return BytesIO('\n'.join(lines).encode('utf-8')).readline


def translate_lines(lines, table):
    return translate(lines_to_readline(lines), table)


def translate(readline, table):
    tokens = tokenize(readline)
    result = []

    for toknum, tokval, _, _, _ in tokens:
        if toknum == NAME:
            tokval = table.get(unicodedata.normalize('NFKC', tokval), tokval)
        result.append((toknum, tokval))

    return [x+'\n' for x in untokenize(result).decode('utf-8').split('\n')]
