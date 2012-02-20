#!/usr/bin/python
# -*- coding:Utf-8 -*-

from setuptools import setup

setup(name='irenicurse',
      version='git',
      description='framework based on urwid to write ncurse applications',
      author='Laurent Peuch',
      # long_description=open("README").read(),
      author_email='cortex@worlddomination.be',
      url='http://example.com',
      install_requires=['urwid'],
      packages=['irenicurse'],
      license= 'GPLv3+',
      keywords='framework ncurse urwid',
     )

# vim:set shiftwidth=4 tabstop=4 expandtab:
