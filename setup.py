from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


long_description = open('README.rst').read()

setup(name='GoogleGroup Exporter',
      version='1.0.0',
      description='Export all your GoogleGroup content.',
      long_description=readme(),
      author='Henrique Bastos',
      author_email='henrique@bastos.net',
      url='https://github.com/henriquebastos/googlegroupexporter',
      license='MIT',
      keywords='googlegroup export mbox csv crawler web',
      packages=['googlegroupexporter'],
      install_requires=[
          'cachecontrol[filecache]',
          'python-dateutil',
          'requests',
          'requests-futures',
          'tqdm',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      entry_points={
          'console_scripts': [
              'ggexport = googlegroupexport.cmd:main',
          ]
      },
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Utilities',
      ])
