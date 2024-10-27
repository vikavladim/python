# https://habr.com/ru/articles/469043/
# https://habr.com/ru/articles/44520/

from setuptools import setup, Extension

setup(name='calc',
      ext_modules=[Extension('calc', ['calculator.c'])],
      )
