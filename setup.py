#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='spc2py',
      version='0.1',
      description='Statistical Process Control Charts Library',
      long_description='Statistical Process Control Charts Library',
      url='https://github.com/tdnguyen0403/spc2py',
      author='Nguyen Tuan Dat',
      author_email='nguyentuandat0403@gmail.com',
      license='GPLv3',
      packages=find_packages(),
      package_dir={"spc2py": "spc2py"},
      package_data={
          "spc2py": ["data/*.csv"]},
      install_requires=['pandas', 'matplotlib', 'numpy'],
      test_suite="tests",
      keywords='SPC QCC CEQ CEP UEPA',
      classifiers=[
          'Development Status :: 1 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Topic :: Scientific/Engineering',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      zip_safe=False)
