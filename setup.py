from distutils.core import setup

setup(
    name="beautifulkuskus",
    packages=["beautifulkuskus"],
    install_requires=[
        'setuptools',
        'scipy',
        'numpy',
       'beautifulsoup4',
    ],
    long_description="https://github.com/urigoren/beautifulkuskus/blob/master/README.md",
    long_description_content_type="text/markdown",
    version="0.1",
    description='Pruning library for beautifulsoup',
    author='Uri Goren',
    author_email='uri@goren.ml',
    url='https://github.com/urigoren/beautifulkuskus',
    keywords=['beautifulsoup', 'html', 'parsing', 'pruning'],
    classifiers=[],
)
