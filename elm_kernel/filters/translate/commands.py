import argparse

from os import unlink
from os.path import basename
from string import Template
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


def do_generate_po_file():
    parser = argparse.ArgumentParser(description='Creates a message catalog with the file classes and function definitions to send for translation')
    parser.add_argument('file',   type=argparse.FileType('rb'), help='File to process')
    parser.add_argument('--output', type=argparse.FileType('w'), help='Output file')

    args = parser.parse_args()
    output = args.output


    file_header = Template(
'''
# ipython-elm-kernel translations for file: $filename
# Copyright (C) Alolom - https://alolom.com
# This file is distributed under the same license as the ipython-elm-kernel package.
# Adrián Pardini <github@tangopardo.com.ar>, 2020.
#
msgid ""
msgstr ""
"Project-Id-Version: 0.0.0\\n"
"Language: ar\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

''')

    definitions = extract_file_definitions(args.file)
    if definitions:
        output.write(file_header.substitute(filename=basename(args.file.name)))

        for definition in definitions:
            output.write(f"# {definition['type']}\n")
            output.write(f'msgid "{definition["name"]}"\n')
            output.write(f'msgstr\n')
            output.write(f'\n')
    else:
        try:
            unlink(output.name)
        except FileNotFoundError:
            pass    # when called with stdout as output
