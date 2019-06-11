from . import __version__

import sys

from ipython_genutils.py3compat import PY3
from ipykernel.ipkernel import IPythonKernel
from IPython.core import release
from tornado import gen
from traitlets import Instance, Type, Any, List, Bool


class ElmIPythonKernel(IPythonKernel):
    code_filters = List([], help="(ELM) List of code filters. They should implement a register(kernel, shell) method").tag(config=True)

    def __init__(self, **kwargs):
        super(ElmIPythonKernel, self).__init__(**kwargs)

        for filter_hook in self.code_filters:
            filter_hook.register(self, self.shell)

    # Kernel info fields
    implementation = 'ipython'
    implementation_version = release.version
    language_info = {
        'name': 'python',
        'version': sys.version.split()[0],
        'mimetype': 'text/x-python',
        'codemirror_mode': {
            'name': 'ipython',
            'version': sys.version_info[0]
        },
        'pygments_lexer': 'ipython%d' % (3 if PY3 else 2),
        'nbconvert_exporter': 'python',
        'file_extension': '.py'
    }

    @gen.coroutine
    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        for filter_hook in self.code_filters:
            options = {
                'silent': silent,
                'store_history': store_history,
                'user_expressions': user_expressions
            }
            code = filter_hook.process_run_cell(code, options)
            silent = options.get('silent', silent)
            store_history = options.get('store_history', store_history)
            user_expressions = options.get('user_expressions', user_expressions)

        return super(ElmIPythonKernel, self).do_execute(code, silent, store_history, user_expressions, allow_stdin)

    def do_complete(self, code, cursor_pos):
        completion_data = super(ElmIPythonKernel, self).do_complete(code, cursor_pos)

        for filter_hook in self.code_filters:
            completion_data = filter_hook.process_completion(code, cursor_pos, completion_data)

        return completion_data
