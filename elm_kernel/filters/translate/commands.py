import argparse
from tokenize import tokenize, NAME, INDENT, DEDENT, COLON, NEWLINE, RPAR

from .translation_table import ar_en_map
from .utils import translate


def do_translate_file():
    parser = argparse.ArgumentParser(description='Translates Python code with a subset of Arabic keywords')
    parser.add_argument('file', type=argparse.FileType('rb'), help='File to translate')

    args = parser.parse_args()

    for line in translate(args.file.readline, ar_en_map):
        print(f'{line}')


def build_definition(name='', type='def', docstring=''):
    type_map = {
        'def': 'function',
    }

    return {
            'name': name,
            'type': type_map.get(type, type),
            'docstring': docstring,
    }


def is_private_definition(definition):
    return definition['name'].startswith('_')


def extract_definitions(readline):
    indentation_level = 0
    current_definition = None
    definitions = []

    tokens = tokenize(readline)

    for toknum, tokval, _, _, _ in tokens:
        if toknum == INDENT:
            indentation_level += 1

        if toknum == DEDENT:
            indentation_level -= 1
            if indentation_level is 0:
                current_definition = 0

        if indentation_level is 0:
            if toknum == NAME and tokval in ('class', 'def'):
                current_definition = build_definition(type=tokval)
                continue

            if current_definition and toknum == NAME:
                current_definition['name'] = tokval
                if not is_private_definition(current_definition):
                    definitions.append(current_definition)
                current_definition = None

    return definitions


def extract_file_definitions(f):
    return extract_definitions(f.readline)


def do_extract_file_definitions():
    parser = argparse.ArgumentParser(description='Extracts function and class definitions from a file')
    parser.add_argument('file', type=argparse.FileType('rb'), help='File to process')

    args = parser.parse_args()

    definitions = extract_file_definitions(args.file)
    print (definitions)
