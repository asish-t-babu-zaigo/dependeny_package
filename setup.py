from setuptools import setup, find_packages

setup(
    name="dependency-package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "python-jose",
        "sqlalchemy",
    ],
)
