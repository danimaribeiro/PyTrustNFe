# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="PyNfeTrust",
    version="0.1",
    author="Danimar Ribeiro",
    author_email='danimaribeiro@gmail.com',
    keywords=['nfe', 'mdf-e'],
    classifiers=[
        'Development Status :: 1 - alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or \
        later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['*test*']),
    package_data={'pytrustnfe': ['nfe/templates/*xml',
                                 'nfse/paulistana/templates/*xml']},
    url='https://github.com/danimaribeiro/PyNfeTrust',
    license='LGPL-v2.1+',
    description='PyNfeTrust é uma biblioteca para envio de NF-e',
    long_description='PyNfeTrust',
    install_requires=[
        'Jinja2 >= 2.8',
        'signxml >= 1.0.0',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock',
    ],
)
