from setuptools import setup, find_packages

setup(
    name='BCScrapper',
    version='0.1',
    packages=['tests', 'sample', 'BCScrapper'],
    url="https://github.com/acpguedes/BCSrapper",
    author='Aureliano Guedes',
    license='GNU General Public License v3.0',
    author_email='guedes.aureliano@gmail.com',
    description='Scrapper of currency ',
    install_requires=["pandas", "requests"],
    test_suite='test'
)
