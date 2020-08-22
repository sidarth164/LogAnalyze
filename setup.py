from setuptools import setup

setup(
  name='logAnalyze',
  version='0.2',
  packages=['logAnalyze', 'logAnalyze.core','logAnalyze.utils'],
  url='github.com/sidarth164/logAnalyze',
  license='Apache-2.0',
  author='Siddharth Agrawal',
  author_email='agrawal97siddhath@gmail.com',
  description='Provides python packages to parse http logs and generate aggregation reports',
  scripts=['scripts/log_reader']
)
