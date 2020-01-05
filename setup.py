"""
Web Accessible Slideshow Server
"""
from setuptools import find_packages, setup


INSTALL_REQUIREMENTS = [
    'pillow~=6.2.1',
    'screeninfo~=0.6.1',
    'quart~=0.10.0',
]

TEST_REQUIREMENTS = [
    'pytest',
    'flake8',
    'flake8-quotes',
    'flake8-mypy',
    'flake8-isort',
    'pep8-naming',
    'isort',
    'pylint',
]

setup(
    name='wass',
    author='Victor Kirov',
    version='0.0.1',
    description='Web Accessible Slideshow Server',
    url='https://github.com/victorkirov/wass',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=INSTALL_REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    extras_require={'test': TEST_REQUIREMENTS},
    entry_points={
        'console_scripts': [
            'wass=wass.cli:cli'
        ]
    }
)
