from ..base import BaseFilter
from .translation_table import ar_en_map
from .utils import translate_lines, normalize_translation_table


class ArabicTranslate(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translation_table = ar_en_map

    def register(self, kernel, shell):
        super().register(kernel, shell)

        ident = kernel.ident

        kernel.log.info("ArabicTranslate filter registered for elm-kernel {}".format(ident))

    def process_text_input(self, lines):
        return translate_lines(lines, self.translation_table)

    def add_translation_table(self, table):
        """
        Adds a translation table to extend the default.
        Args:
            table (dict): A dict-like object that maps from words in Arabic to their English equivalents
        Returns:
            None
        """
        table = normalize_translation_table(table)
        self.translation_table = dict(**self.translation_table, **table)
