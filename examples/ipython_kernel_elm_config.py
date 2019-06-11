import sys
import os.path
import tempfile
import logging

c = get_config()    # noqa - defined by traitlets


from elm_kernel.filters import BaseFilter


class SampleFilter(BaseFilter):
    def register(self, kernel, shell):
        super().register(kernel, shell)

        ident = kernel.ident

        logfile = os.path.join(tempfile.gettempdir(), 'elm-kernel-{}.log'.format(ident))

        logger = self.logger = logging.getLogger('elm-kernel-{}'.format(ident))
        fh = self.fh = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.setLevel(logging.INFO)
        logger.info('STARTED ELM SESSION {}'.format(ident))

        # This intercepts the output of the shell.
        # The kernel subprocess replaces stdout and stderr by streams that talk over 0MQ.
        # XXX FIXME: turn the whole modified kernel into another project that extends ipykernel instead
        # XXX FIXME: the proper way to do this would be to change IPKernelApp.outstream_class to one with logging inside.

        def make_stream_logger(stream, tag):
            __write = stream.write

            def write(string):
                logger.info('OUTPUT FROM SHELL {}: {}'.format(tag, string))
                return __write(string)

            stream.write = write

        make_stream_logger(sys.stdout, 'STDOUT')

        kernel.log.info("FILTER REGISTERED for elm-kernel {}".format(ident))
        kernel.log.info("LOGGING USER INTERACTIONS TO {}".format(logfile))

    def process_text_input(self, lines):
        output = []
        for line in lines:
            self.logger.info('LINE INPUT FROM USER: {}'.format(repr(line)))
            if 'FORBIDDEN_WORD' in line:
                line = line.replace('FORBIDDEN_WORD', 'SAFE_WORD')
                self.logger.info('LINE INPUT FROM USER: "FORBIDDEN_WORD" found, replacing with "SAFE_WORD"')
            output.append(line)

        return output

    # Simple exclusion from command history, try for example:
    # In [1]: print('something to exclude... no-history')
    def process_run_cell(self, code, options):
        if 'no-history' in code:
            options['store_history'] = False
            self.logger.info('RUN CODE, excluded from command history: {}'.format(repr(code)))
        return code

    def process_completion(self, code, cursor_pos, completion_data):
        self.logger.info('COMPLETION REQUESTED FOR: {}'.format(repr(code)))
        self.logger.info('COMPLETION RESULTS: {}'.format(completion_data['matches']))
        completion_data['matches'].insert(0, 'some-new-suggestion')
        return completion_data

    def post_run_cell(self, result):
        """
        This is called after executing a cell with the result of that
        """
        self.logger.info('CELL EXECUTION RESULT: {}'.format(repr(result)))
        self.logger.info('CELL EXECUTION EXPRESSION RESULT : {}'.format(repr(result.result)))
        self.logger.info('CELL EXECUTION EXPRESSION OUTPUT: {}'.format(repr(self.shell.displayhook.exec_result)))


sample_filter = SampleFilter()

# Set to info or greater to see the logs on the Jupyter console
c.ElmKernelApp.log_level = 'INFO'

c.ElmIPythonKernel.code_filters = [sample_filter]
