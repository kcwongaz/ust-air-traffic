from setuptools import setup, find_packages

setup(
    name="air_traffic",
    version="1.0.0",
    packages=find_packages("air_traffic"),
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matploblib",
        "cartopy",
        "geopy"
    ],
)
