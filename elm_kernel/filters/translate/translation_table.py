from .utils import normalize_translation_table, reverse_translation_table


ar_en_map = {
    'و':        'and',
    'كأنها':    'as',
    'تأكد':     'assert',

    'توقف':     'break',

    'فصيلة':    'class',
    'تجاوز':    'continue',

    'عرف':      'def',
    'احذف':     'del',
    'دليل':     'dict',

    'او اذا':   'elif',
    'اخرا':     'else',
    'باستثناء': 'except',
    'نفذ':      'exec',

    'أخيرا':    'finally',
    'لكل':      'for',
    'من':       'from',

    'اذا':      'if',
    'استحضر':   'import',
    'في':       'in',
    'هو':       'is',

    'دالة':     'lambda',
    'مكتبة':    'library',
    'صف':       'list',

    'ليس':      'not',
    'أو':       'or',

    'ديوان':    'package',
    'تجاهل':    'pass',
    'اظهر':     'print',

    'خطأ':      'raise',
    'ﻡﺩﻯ':      'range',
    'النتيجة':  'return',

    'جرب':      'try',
    'نوع':      'type',

    'بينما':    'while',
    'بإستخدام': 'with',

    'انتج':     'yield',
}


ar_en_map = normalize_translation_table(ar_en_map)

en_ar_map = reverse_translation_table(ar_en_map)
