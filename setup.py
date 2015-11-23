from setuptools import setup, find_packages

requires = [
    'jupyter',
    'numpy',
    'matplotlib',
]

setup(name='subset-selector',
      version='0.0.1',
      description='Subset selection using IPython/Jupyter Notebook',
      author='Brandon Bradley',
      author_email='bradleytastic@gmail.com',
      url='http://github.com/blbradley/subset-selector',
      packages=find_packages(),
      license='MIT',
      install_requires=requires,
)
