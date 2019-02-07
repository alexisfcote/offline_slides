
.. image:: https://img.shields.io/pypi/v/offline_slides.svg
    :target: https://pypi.python.org/pypi/offline_slides
    :alt: Latest PyPI version

.. image:: https://travis-ci.com/alexisfcote/offline_slides.svg?branch=master
    :target: https://travis-ci.com/alexisfcote/offline_slides
    :alt: Latest Travis-ci build

# offline slides
Hacky program to make a jupyter 
notebook into offline reveal.js slideshow. Can also output a html version.
Will create a .slides.offline.html next to 
the notebook as well as a ext/ folder including all of the required files.
You need to copy both of those for the presentation to work.

## Usage
### as command line tool
```
 offlineslides [-h] [--html] [--no-download] [--verbose] notebook_path

positional arguments:
  notebook_path      Path to the .ipynb notebook

optional arguments:
  -h, --help         show this help message and exit
  --html             Export as offline standalone html
  --no-download, -n  Do not download files if ext folder exists
  --verbose, -v      Output more info if true
```
### as library
```python
from offlineslides import export_to_offline
export_to_offline('my_notebook.ipynb')
```
