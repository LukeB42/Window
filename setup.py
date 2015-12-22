# _*_ coding: utf-8 _*_
from setuptools import setup, Extension
#from distutils.core import setup, Extension

banner = """
██████╗ ███████╗██╗   ██╗██████╗ ███████╗██████╗ ███╗   ██╗███████╗████████╗██╗ ██████╗███████╗   
██╔══██╗██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝██║██╔════╝██╔════╝   
██████╔╝███████╗ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██╔██╗ ██║█████╗     ██║   ██║██║     ███████╗   
██╔═══╝ ╚════██║  ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║╚██╗██║██╔══╝     ██║   ██║██║     ╚════██║   
██║     ███████║   ██║   ██████╔╝███████╗██║  ██║██║ ╚████║███████╗   ██║   ██║╚██████╗███████║██╗
╚═╝     ╚══════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝╚══════╝╚═╝
"""
print banner

setup(name='window',
      description='Easy ncurses applications',
      author='Luke Brooks',
      author_email='luke@psybernetics.org',
      url="http://github.com/LukeB42/Window",
      download_url="http://github.com/LukeB42/Window/tarball/0.1",
      version='0.0.1',
      py_modules=['window'],
      long_description="""
This module provides Window and Pane objects for rapidly creating ncurses programs without sacrificing quality.
""",
      keywords="ncurses tui",
      license="MIT",
      test_suite='test'
      )

