import io
import os
import shutil
import tempfile
import unittest
from base64 import encodebytes
from os.path import join as pjoin

from nbformat import write
from nbformat.v4 import (new_code_cell, new_markdown_cell, new_notebook,
                         new_output)
from offlineslides import export_to_offline

png_green_pixel = encodebytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00'
                              b'\x00\x00\x01\x00\x00x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT'
                              b'\x08\xd7c\x90\xfb\xcf\x00\x00\x02\\\x01\x1e.~d\x87\x00\x00\x00\x00IEND\xaeB`\x82'
                              ).decode('ascii')


class integration_test(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

        nb = new_notebook()

        nb.cells.append(new_markdown_cell(u'Created by test ³'))
        cc1 = new_code_cell(source=u'print(2*6)')
        cc1.outputs.append(new_output(output_type="stream", text=u'12'))
        cc1.outputs.append(new_output(output_type="execute_result",
                                      data={'image/png': png_green_pixel},
                                      execution_count=1,
                                      ))
        nb.cells.append(cc1)

        with io.open(pjoin(self.tmpdir.name, 'testnb.ipynb'), 'w',
                     encoding='utf-8') as f:
            write(nb, f, version=4)

    def tearDown(self):
        self.tmpdir.cleanup()
        
    def test_output_without_errors(self):
        export_to_offline(pjoin(self.tmpdir.name, 'testnb.ipynb'))
        assert os.path.isfile(
            pjoin(self.tmpdir.name, 'testnb.slides.offline.html'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs'))
        assert os.path.isdir(
            pjoin(self.tmpdir.name, 'ext/ajax/libs/font-awesome'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs/jquery'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs/mathjax'))
        assert os.path.isdir(
            pjoin(self.tmpdir.name, 'ext/ajax/libs/require.js'))
        assert os.path.isdir(
            pjoin(self.tmpdir.name, 'ext/ajax/libs/reveal.js'))

    def test_offline_jupyter_html_without_errors(self):
        export_to_offline(
            pjoin(self.tmpdir.name, 'testnb.ipynb'), slides=False)
        assert os.path.isfile(pjoin(self.tmpdir.name, 'testnb.offline.html'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs/jquery'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs/mathjax'))
        assert os.path.isdir(
            pjoin(self.tmpdir.name, 'ext/ajax/libs/require.js'))

    def test_offline_jupyter_slides_without_errors(self):
        export_to_offline(pjoin(self.tmpdir.name, 'testnb.ipynb'), slides=True)
        assert os.path.isfile(
            pjoin(self.tmpdir.name, 'testnb.slides.offline.html'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs/jquery'))
        assert os.path.isdir(pjoin(self.tmpdir.name, 'ext/ajax/libs/mathjax'))
        assert os.path.isdir(
            pjoin(self.tmpdir.name, 'ext/ajax/libs/require.js'))
        assert os.path.isdir(
            pjoin(self.tmpdir.name, 'ext/ajax/libs/font-awesome'))
        assert os.path.isdir(
            pjoin(self.tmpdir.name, 'ext/ajax/libs/reveal.js'))

    def test_offline_jupyter_no_download(self):
        export_to_offline(pjoin(self.tmpdir.name, 'testnb.ipynb'),
                          slides=True, no_download=True)
        assert os.path.isfile(
            pjoin(self.tmpdir.name, 'testnb.slides.offline.html'))
        assert not os.path.isdir(pjoin(self.tmpdir.name, '/ext/'))


if __name__ == '__main__':
    unittest.main()
