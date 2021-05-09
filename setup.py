import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

setup(
    name='crudlfap',
    setup_requires='setupmeta',
    versioning='dev',
    description='Rich frontend for generic views with Django',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/crudlfap',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    keywords='django crud',
    install_requires=[
        'ryzom>=0.6.3,<0.7',
        'django>=3.1,<3.2',
        'django-tables2',
        'django-filter',
        'timeago',
        'lookupy-unmanaged',
        'libsass',
    ],
    tests_require=['tox'],
    extras_require=dict(
        project=[
            'django-debug-toolbar',
            'django-extensions',
            'django-registration',
            'dj-static',
        ],
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3',
)
