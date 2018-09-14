import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="offlineslides",
    version="0.1.1",
    author="Alexis Fortin-Côté",
    description="Program to make a jupyter notebook into offline reveal.js slideshow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexisfcote/offline_slides",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
    'console_scripts': [
        'offlineslides=offlineslides.offlineslides:main',
    ],
},
)