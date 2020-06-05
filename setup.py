"""Setup script for elm_kernel package.
"""
import os
import sys
import shutil
from glob import glob
from setuptools import setup, find_packages


DISTNAME = 'elm_kernel'
KERNEL_NAME = 'elm'
DESCRIPTION = 'The Elm Python kernel for Jupyter'
LONG_DESCRIPTION = open('README.md', 'rb').read().decode('utf-8')
MAINTAINER = 'Adrián Pardini'
MAINTAINER_EMAIL = 'github@tangopardo.com.ar'
URL = 'http://github.com/pardo-bsso/elm_kernel'
LICENSE = 'BSD'
REQUIRES = ["ipykernel"]
INSTALL_REQUIRES = ["ipykernel"]
PACKAGES = find_packages()

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development',
    'Topic :: System :: Shells',
]


pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))
pkg_root = pjoin(here, DISTNAME)

version_ns = {}
with open(pjoin(here, DISTNAME, '_version.py')) as f:
    exec(f.read(), {}, version_ns)

current_version = version_ns['__version__']


setup_args = dict(
    name=DISTNAME,
    version=current_version,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    packages=PACKAGES,
    data_files=[],
    url=URL,
    download_url=URL,
    license=LICENSE,
    platforms=["Any"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=CLASSIFIERS,
    requires=REQUIRES,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'elm-kernel-translate=elm_kernel.filters.translate.commands:do_translate_file',
        ]
    },
 )

if any(a.startswith(('bdist', 'build', 'install')) for a in sys.argv):
    from ipykernel.kernelspec import write_kernel_spec, make_ipkernel_cmd

    argv = make_ipkernel_cmd(mod='elm_kernel', executable='python')
    dest = os.path.join(here, 'data_kernelspec')
    if os.path.exists(dest):
        shutil.rmtree(dest)
    write_kernel_spec(dest, overrides={
        'argv': argv,
        'display_name': 'ELM (Python: {} ELM: {})'.format(sys.version_info[0], current_version)
    })

    setup_args['data_files'].append(
        (
            pjoin('share', 'jupyter', 'kernels', KERNEL_NAME),
            glob(pjoin('data_kernelspec', '*')),
        )
    )


if __name__ == '__main__':
    setup(**setup_args)
