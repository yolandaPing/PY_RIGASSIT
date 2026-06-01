
# from distutils.core import setup
from setuptools import setup


def readme_file():
    with open("README.rst") as rf:
        return rf.read()


setup(name= "PY_RIGASSIT",version="5.1.1",description="Mayatool",
      long_description=readme_file(),author_email="Yolanda Ping",
      maintainer="PY_RIGASSIT",maintainer_email="pyou1224@foxmail.com ",
      packages=["Files","images","modules","plug-ins","reserve","scripts"],py_modules=[""],
      url="https://b23.tv/pmLchH6",
      license="MIT")