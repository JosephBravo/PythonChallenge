from setuptools import find_packages, setup

setup(
    name='pythonchallenge',
    author_email="jorbravoa@gmail.com>",
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
    ],
)
