import re
from setuptools import setup


version = re.search("__version__ = '([^']+)'",
                    open('snapext/__init__.py').read()).group(1)


setup(name = 'snapext',
      version = "0.1.5",
      author = 'Conor Hudson, Tim Radvan',
      author_email = '',
      url = 'https://github.com/technoboy10/snapext',
      description = 'Server for writing Snap! extensions',
      license = 'MIT',
      packages = ['snapext'],
      classifiers = [
        "Programming Language :: Python",
      ],
)
 
