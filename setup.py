from setuptools import setup, find_packages

setup(
    name="geohelpers",
    version="0.1.0",
    author="klqmba",
    description="Geospatial helper utilities",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # Add any third-party packages your utils.py imports, e.g.:
        "pandas",
        "rasterstats",
        "pyproj",
    ],
)
