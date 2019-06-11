from traitlets import Type

from ipykernel.kernelapp import IPKernelApp
from .kernel import ElmIPythonKernel


class ElmKernelApp(IPKernelApp):
    name = 'ipython-kernel-elm'
    classes = IPKernelApp.classes + [ElmIPythonKernel]
    # the kernel class, as an importstring
    kernel_class = Type('elm_kernel.kernel.ElmIPythonKernel',
                        klass='elm_kernel.kernel.ElmIPythonKernel',
    help="""The Kernel subclass to be used.

    This should allow easy re-use of the IPKernelApp entry point
    to configure and launch kernels other than IPython's own.
    """).tag(config=False)


launch_new_instance = ElmKernelApp.launch_instance


def main():
    """Run an IPKernel as an application"""
    app = ElmKernelApp.instance()
    app.initialize()
    app.start()


if __name__ == '__main__':
    main()
