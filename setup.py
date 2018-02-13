"""
A Python3 program that extracts some statistics regarding field coverage in a line-delimited JSON document.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='jsonl_fstats',
      version='0.0.1',
      description='a Python3 program that extracts some statistics regarding field coverage in a line-delimited JSON document',
      url='https://github.com/slub/jsonl-fstats',
      author='Bernhard Hering',
      author_email='bernhard.hering@slub-dresden.de',
      license="Apache 2.0",
      packages=[
          'jsonl_fstats',
      ],
      package_dir={'jsonl_fstats': 'jsonl_fstats'},
      install_requires=[
          'argparse>=1.4.0',
          'numpy>=1.11.0'
      ],
      entry_points={
          "console_scripts": ["jsonl-fstats=jsonl_fstats.jsonl_fstats:run"]
      }
      )
