import os, itertools

from setuptools import setup, find_packages

dataFiles = list(
    itertools.chain.from_iterable(
        [(fs[0], [fs[0] + '/' + f]) for f in fs[2] if not f.endswith('~')] 
        for fs in os.walk('rantbase/priv')))

setup(name="rantbase",
      version="0.1",

      description="Simple markdown document collection",
      author="Brendon Hogger",
      author_email="brendonh@gmail.com",
      url="https://github.com/brendonh/rantbase",
      long_description=open('README.md').read(),

      download_url="https://github.com/brendonh/rantbase/zipball/master",

      packages = find_packages(),
      zip_safe = False,

      install_requires = [
      ],

      data_files = dataFiles,

      # include_package_data = True,
      # package_data = {
      #   '': ['priv/**']
      # },

)
