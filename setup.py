from setuptools import setup

setup(name='ncbifetcher',
      version='0.3.0',
      description='Fetch ncbi and pull to any location',
      url='https://github.com/bwinnett12/ncbifetcher',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
      ],
      author='Bill Winnett',
      author_email='wwinnett@iastate.edu',
      license='MIT',
      # packages=['ncbifetch'],
      install_requires=[
            'markdown',
            'biopython',
            'glob3',
            'argparse',
            'Bio',
      ],
      # entry_points = {
      #   'console_scripts': ['ncbifetch=ncbifetch.command_line:main'],
      # },
      include_package_data=True,
      zip_safe=False)
