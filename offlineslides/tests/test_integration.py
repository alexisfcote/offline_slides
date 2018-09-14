import unittest
import io
import os
from os.path import join as pjoin
import shutil

from base64 import encodebytes
from nbformat import write
from nbformat.v4 import (
    new_notebook, new_markdown_cell, new_code_cell, new_output,
)

from offlineslides import export_to_offline_slides

png_green_pixel = encodebytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00'
b'\x00\x00\x01\x00\x00x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT'
b'\x08\xd7c\x90\xfb\xcf\x00\x00\x02\\\x01\x1e.~d\x87\x00\x00\x00\x00IEND\xaeB`\x82'
).decode('ascii')



class integration_test(unittest.TestCase):
    def setUp(self):
        nbdir = 'tests'
        subdir = pjoin(nbdir)
        self.subdir = subdir
        
        if not os.path.isdir(pjoin(nbdir)):
            os.makedirs(subdir)


        nb = new_notebook()
        
        nb.cells.append(new_markdown_cell(u'Created by test ³'))
        cc1 = new_code_cell(source=u'print(2*6)')
        cc1.outputs.append(new_output(output_type="stream", text=u'12'))
        cc1.outputs.append(new_output(output_type="execute_result",
            data={'image/png' : png_green_pixel},
            execution_count=1,
        ))
        nb.cells.append(cc1)
        
        with io.open(pjoin(nbdir, 'testnb.ipynb'), 'w',
                     encoding='utf-8') as f:
            write(nb, f, version=4)
    
    
    def tearDown(self):
        shutil.rmtree(self.subdir, ignore_errors=False)

    def test_output_without_errors(self):
        export_to_offline_slides('tests/testnb.ipynb')
        assert os.path.isfile('tests/testnb.slides.offline.html')
        assert os.path.isdir('tests/ext/ajax/libs')
        assert os.path.isdir('tests/ext/ajax/libs/font-awesome')
        assert os.path.isdir('tests/ext/ajax/libs/jquery')
        assert os.path.isdir('tests/ext/ajax/libs/mathjax')
        assert os.path.isdir('tests/ext/ajax/libs/require.js')
        assert os.path.isdir('tests/ext/ajax/libs/reveal.js')


if __name__ == '__main__':
    unittest.main()