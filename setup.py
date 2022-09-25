from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    requirements = f.readlines()

setup(
    name='CardMarketTrendFinder',
    version='2.0',
    description='A module to finder the trends on cardmarket.com',
    long_description=long_description,
    author='Alexander Komischke',
    author_email='alexander.komischke@tutanota.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requirements,  # external packages as dependencies
    scripts=[
        'scripts/build_exe'
    ]
)
