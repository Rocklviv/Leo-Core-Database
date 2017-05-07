from setuptools import setup
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='Leo-Core-Database',
    version="0.1.0",
    description="Leo Core Database module",
    long_description=long_description,
    url="https://github.com/Rocklviv/Leo-Core-Database",
    author="Denys Chekirda aka Rocklviv",
    author_email="dchekirda@gmail.com",
    license="GPLv3",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Database Module',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU GPL v3 License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='rethinkdb database orm db',
    install_requires=['rethinkdb'],
    packages=['leo.core']
)