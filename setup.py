
# from distutils.core import setup
from setuptools import setup


def readme_file():
    with open("README.md") as rf:
        return rf.read()


setup(name= "PY_RIGASSIT",version="0.6.1.1",description="Maya Tool",
      long_description=readme_file(),author_email="Yolanda Ping",
      maintainer="PY_RIGASSIT",maintainer_email="pyrigassit@gmali.com",
      packages=["Files","images","modules","plug-ins","reserve","scripts"],py_modules=[""],
      url="https://space.bilibili.com/3493142019967757?spm_id_from=333.1007.0.0",
      license="MIT")