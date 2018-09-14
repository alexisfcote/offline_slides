# offline slides
Hacky program to make a jupyter 
notebook into offline reveal.js slideshow.
Will create a .slides.offline.html next to 
the notebook as well as a ext/ folder including all of the required files.
You need to copy both of those for the presentation to work.

## Usage
### as command line tool
```
python offlineslides.py [-h] notebook_path
```
### as library
```python
from offlineslides import export_to_offline_slides
export_to_offline_slides('my_notebook.ipynb')
```
