"""

TODO: Change
terraplen
===

Easy and Useful Amazon Scraper

"""

from setuptools import setup
from os import path

about = {}
with open("terraplen/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      long_description_content_type="text/markdown",
      install_requires=["requests", "lxml", "bs4"],
      tests_require=["requests", "lxml", "bs4", "pytest"],
      packages=["terraplen"],
      zip_safe=True,
      platforms="any",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Envterraplennment :: Other Envterraplennment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Envterraplennment :: Console"
      ])
