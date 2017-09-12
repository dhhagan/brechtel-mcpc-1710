try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '0.1.0'

setup(
    name = 'mcpc',
    version = __version__,
    packages = ['mcpc'],
    description = 'A simple python library to run and use the Brechtel MCPC',
    author = 'David H Hagan',
    author_email = 'dhagan@mit.edu',
    license = 'MIT',
    url = 'https://github.com/dhhagan/brechtel-mcpc-1710',
    keywords = ['atmospheric chemistry'],
    install_requires = [
        'pyserial',
    ],
    classifiers = [
        'Development Status :: 1 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
		'Topic :: Scientific/Engineering :: Atmospheric Science',
		'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
