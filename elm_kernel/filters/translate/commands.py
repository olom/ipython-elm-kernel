import argparse

from .translation_table import ar_en_map
from .utils import translate


def do_translate_file():
    parser = argparse.ArgumentParser(description='Translates Python code with a subset of Arabic keywords')
    parser.add_argument('file', type=argparse.FileType('rb'), help='File to translate')

    args = parser.parse_args()

    for line in translate(args.file.readline, ar_en_map):
        print(f'{line}')
