import re
from setuptools import setup

with open('pysimplestorageservice/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


packages = [
    'pysimplestorageservice',
]

requires = [
    'requests',
]

setup(
    name='pysimplestorageservice',
    version=version,
    description='Python S3 access for humans',
    url='https://github.com/poteralski/pysimplestorageservice',
    author='Piotr Poteralski',
    author_email='poteralski.dev@gmail.com',
    license='Apache 2.0',
    packages=packages,
    zip_safe=False,
    install_requires=requires,
)
