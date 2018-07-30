from setuptools import setup, find_packages
import os


# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='crudlfap',
    version='0.4.12',
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
)
