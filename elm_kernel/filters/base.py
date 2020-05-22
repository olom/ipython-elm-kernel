class BaseFilter:
    """
    This is the reference implementation for all filters/hooks.
    Just passes the data as-is without changing it.
    """
    def register(self, kernel, shell):
        self.kernel = kernel
        self.shell = shell

        shell.events.register('post_run_cell', self.post_run_cell)
        shell.input_transformers_cleanup.append(self.process_text_input)

        # You can also perform more advanced modifications, see:
        # https://ipython.readthedocs.io/en/stable/config/inputtransforms.html#ast-transformations

    def process_text_input(self, lines):
        return lines

    def process_text_output(self, text):
        """
        This is called from the kernel when displaying the results of a command back to the User
        """
        pass

    # This is called from the kernel before feeding input into the IPython Shell
    def process_run_cell(self, code, options):
        """
        Modifies the arguments and code passed to shell.run_cell()
        options is a dict like
        {
            'silent': False,
            'store_history': True,
            'user_expressions': None

        }
        that can be modified in place to change behaviour.
        Returns: the new code to run
        """
        return code

    # This is called from the kernel before returning completion data
    def process_completion(self, code, cursor_pos, completion_data):
        """
        This is called from the kernel before returning completion data
        completion_data is a dict like
        {
            'matches' : matches,
            'cursor_end' : cursor_pos,
            'cursor_start' : cursor_pos - len(txt),
            'metadata' : {},
            'status' : 'ok'
        }
        """
        return completion_data

    def post_run_cell(self, result):
        """
        This is called after executing a cell with the result of that
        """
        pass
