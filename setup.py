from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys


# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


VERSION = '0.4.25'


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('GIT_TAG')

        if tag != VERSION:
            info = 'Git tag: {} does not match the version of app: {}'.format(
                tag,
                VERSION
            )
            sys.exit(info)


setup(
    name='crudlfap',
    version=VERSION,
    description='Rich frontend for generic views with Django',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://github.com/yourlabs/crudlfap',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    long_description=read('README.rst'),
    license='MIT',
    keywords='django crud',
    install_requires=[
        'jinja2',
        'django>=2.0',
        'django-jinja',
        'django-bootstrap3',
        'django-material',
        'django-tables2==2.0.0a3',
        'django-filter',
        'django-betterforms',
        'timeago',
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
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
