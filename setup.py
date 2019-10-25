from distutils.core import setup
setup(
    name = 'duxwrap',
    packages = ['duxwrap'],
    version = '0.2',
    license='MIT',
    description = 'Dux-Soup remote control API wrapper',
    author = 'bojan',
    author_email = '',
    url = 'https://github.com/abrihter/duxwrap/releases',
    download_url = 'https://github.com/abrihter/duxwrap/archive/v_02.tar.gz',
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
