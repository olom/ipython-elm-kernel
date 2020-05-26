# IPython Kernel for ELM


This is a Python kernel that has hooks to inspect and modify user input before it's processed (for example, to replace
certain terms, exclude from the command history or make more complex transformations using the AST module)


## Installation


Run

```bash
pip install .
```

to fetch the needed dependencies and install the kernel.


## Running

After launching Jupyer (for example with jupyer notebook) under the New... dropdown you should see an entry "ELM (Python
3)"

Without configuring this works exactly the same as the original kernel.


## Configuring

Create a file named ipython_kernel_elm_config.py and define the set of filters inside it.
In order for it to be loaded you need to do one of this:

  - Copy it to ~/.ipython/profile_default
  - Copy it to /etc/ipython (if running from a virtual env it's under VIRTUALENV_DIR/etc/ipython)
  - Set the environment variable IPYTHONDIR (see IPython docs)
  - Run jupyter from the directory where that file is


We added a configurable trait to ElmPythonKernel, code_filters. It is a list of filter instances.

The contents of the configuration file should be something like this:


```python
# contents of file ipython_kernel_elm_config.py

from elm_kernel.filters import ArabicTranslate


c = get_config()    # get_config is defined by IPython before processing the configuration file


translator = ArabicTranslate()

c.ElmIPythonKernel.code_filters = [translator]
```


## Built-in filters

### ArabicTranslate

This plugin enables the IPython kernel to accept a subset of words in Arabic as their english counterparts.
In order to use it add something like this to the config file:

```python
# contents of file ipython_kernel_elm_config.py

from elm_kernel.filters import ArabicTranslate


c = get_config()    # get_config is defined by IPython before processing the configuration file


translator = ArabicTranslate()

c.ElmIPythonKernel.code_filters = [translator]
```

The included translations are defined in the file elm_kernel/filters/translate/translation_table.py

To add or update the translations call the method add_translation_table() on the filter instance.
For example:

```python
from elm_kernel.filters import ArabicTranslate


c = get_config()    # get_config is defined by IPython before processing the configuration file


# This maps from words in Arabic to Python keywords
# New words are added. If they were already present on the default translations they are updated.

my_extra_translations = {
    'اظهر':     'print',
}

translator = ArabicTranslate()
translator.add_translation_table(my_extra_translations)

c.ElmIPythonKernel.code_filters = [translator]
```


### Filter definition

Filters are classes that extend from `elm_kernel.filters.BaseFilter`
When a new kernel is launched first the register() method is called with the kernel and IPython shell as arguments.

After that the corresponding methods are called when the User enters commands and Python gives a result back.

The config file included under `examples/` has a sample filter that logs user input to a file on /tmp and makes the following
changes:

  - Replaces all occurrences of 'FORBIDDEN_WORD' with 'SAFE_WORD'
  - If anywhere in the code there's the text 'no-history', that block will not be stored on the internal command history
    (%hist)

The filter classes do not need to be all in this file, you can make a custom package and import it from there.


```python
class MyFilter(BaseFilter):
    def process_text_input(self, lines):
        """
        This is called before sending User input to the kernel.
        lines is a list of new-line (\n) terminated strings.
        """
        return lines

    def process_text_output(self, text):
        """
        This is called from the kernel when displaying the results of a command back to the User
        """
        pass

    # This is called from the kernel before feeding input into the IPython Shell
    def process_run_cell(self, code, options):
        """
        This is called from the kernel before feeding input into the IPython Shell
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
```
