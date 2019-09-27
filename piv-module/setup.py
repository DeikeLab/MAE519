from setuptools import setup, find_packages

setup(name='piv_mae519',
      description='PIV module for MAE 519, Fall 2019',
      url='https://github.com/danjruth/MAE519-piv-module',
      author='Daniel Ruth',
      author_email='druth@princeton.edu',
      packages=find_packages(),
      install_requires=[
          'openpiv',
          'scipy',
          'matplotlib',
          'numpy',
          ],
      )