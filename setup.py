# coding=utf-8
"""Python packaging."""
import os
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


name = 'insight'
version = read_relative_file('VERSION').strip()
readme = read_relative_file('README')
packages = [name.split('.')[0]]
namespace_packages = '.' in name and packages or []


setup(name=name,
      version=version,
      description="Insight is a PostBox async preview generator service.",
      long_description=readme,
      classifiers=[
                   "Programming Language :: Python",
                   'License :: Other/Proprietary License',
                   ],
      keywords='',
      author='Novapost',
      author_email='rd@novapost.fr',
      url='https://github.com/novagile/insight',
      license='closed source',
      packages=packages,
      namespace_packages=namespace_packages,
      include_package_data=True,
      install_requires=['setuptools',
                        'Flask',
                        'redis',
                        'requests',
                        'circus',
                       ],
      entry_points={
          'console_scripts': [
              'insight = insight.worker:main',
              'insight_serve_api = insight.api:main',
          ]
      },
      )
