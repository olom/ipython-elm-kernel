import unicodedata
from io import BytesIO
from tokenize import tokenize, untokenize, NAME


def normalize_translation_table(table):
    return {unicodedata.normalize('NFKC', k): v for k, v in table.items()}


def reverse_translation_table(table):
    return {v: k for k, v in table.items()}


def translate(lines, table):
    tokens = tokenize(BytesIO('\n'.join(lines).encode('utf-8')).readline)
    result = []

    for toknum, tokval, _, _, _ in tokens:
        if toknum == NAME:
            tokval = table.get(unicodedata.normalize('NFKC', tokval), tokval)
        result.append((toknum, tokval))

    return [x+'\n' for x in untokenize(result).decode('utf-8').split('\n')]
