# -*- coding: utf-8 -*-

import setuptools

with open('README.md', 'r',) as f:
    readme = f.read()

setuptools.setup(
    name = 'duxwrap',
    packages = ['duxwrap'],
    version = '0.6',
    description = 'Dux-Soup remote control API wrapper',
    long_description_content_type="text/markdown",
    long_description=readme,
    author = 'bojan',
    author_email = '',
    license='MIT',
    url = 'https://github.com/abrihter/duxwrap/releases',
    download_url = 'https://github.com/abrihter/duxwrap/archive/v_06.tar.gz',
    keywords = ['DUX SOUP', 'API', 'WRAPPER'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
