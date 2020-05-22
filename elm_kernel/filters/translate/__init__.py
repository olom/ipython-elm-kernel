from ..base import BaseFilter
from .translation_table import ar_en_map
from .utils import translate


class ArabicTranslate(BaseFilter):
    def register(self, kernel, shell):
        super().register(kernel, shell)

        ident = kernel.ident

        kernel.log.info("ArabicTranslate filter registered for elm-kernel {}".format(ident))

    def process_text_input(self, lines):
        return translate(lines, ar_en_map)
