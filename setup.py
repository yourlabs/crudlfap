from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys


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
        'jinja2==3.0.2',
        'django>=3.2,<4',
        'django-jinja',
        'django-bootstrap3',
        'django-material-1.3-dj32==1.3.3',
        'django-tables2',
        'django-filter',
        'django-betterforms',
        'timeago',
        'lookupy-unmanaged',
    ],
    tests_require=['tox'],
    extras_require=dict(
        dev=[
          'django-collectdir',
          'django-reversion',
          'django-debug-toolbar',
          'django-extensions',
          'devpy',
          'dj-static',
        ],
    ),
    entry_points={
        'console_scripts': [
            'crudlfap = crudlfap_example.manage:main',
        ],
    },
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
