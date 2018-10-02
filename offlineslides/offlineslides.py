import io
import os
from os.path import join as pjoin
import re
import shutil
import tempfile
import urllib.request
import zipfile
from contextlib import closing
from urllib.parse import urlparse

import requests
from nbconvert import SlidesExporter


def _add_as_offline_ressource(url, path_prefix):
    """download file at url to the ext/ path location and return its local path

    Arguments:
        url {str} -- url of the file
        path_prefix {str} -- path prefix of where to download

    Returns:
        str -- file location
    """
    (path, lib_filename) = os.path.split(
        pjoin('ext/', urlparse(url).path[1:]))
    os.makedirs(pjoin(path_prefix, path), exist_ok=True)
    file_location, headers = urllib.request.urlretrieve(
        url, filename=pjoin(path_prefix, path, lib_filename))
    return pjoin(path, lib_filename)


def export_to_offline_slides(ipynb_path, template_file=None, reveal_scroll=True):
    head, filename = os.path.split(ipynb_path)

    # Export ipynb to html reveal.js slides
    slides_exporter = SlidesExporter()
    slides_exporter.reveal_theme = 'White'
    slides_exporter.reveal_url_prefix = 'ext/ajax/libs/reveal.js'
    slides_exporter.reveal_scroll=reveal_scroll

    if template_file:
        slides_exporter.template_file = template_file

    new_filename = ''.join(
        (os.path.splitext(filename)[0], '.slides.offline.html'))

    with open(pjoin(head, filename), 'r', encoding='utf-8') as f:
        (body, resources) = slides_exporter.from_file(f)

    if os.path.isdir(pjoin(head, 'ext')):
        shutil.rmtree(pjoin(head, 'ext'))

    exp = re.compile('\"http.*cdnjs.*\"')

    with open(pjoin(head, new_filename), 'w', encoding='utf-8') as fout:
        for url in re.findall(exp, body):
            if 'reveal' in url:
                continue
            url = url.replace('"', '').split(' ')[0]
            if 'http' not in url:
                continue
            local_url = _add_as_offline_ressource(url, path_prefix=head)
            body = body.replace(url, local_url)
        fout.write(body)

    # get missing mathjax files
    os.makedirs(
        pjoin(head, 'ext/ajax/libs/mathjax/2.7.1/extensions/'), exist_ok=True)
    urllib.request.urlretrieve("https://raw.githubusercontent.com/mathjax/MathJax/master/extensions/MathZoom.js",
                               filename=pjoin(head, 'ext/ajax/libs/mathjax/2.7.1/extensions/MathZoom.js'))
    urllib.request.urlretrieve("https://raw.githubusercontent.com/mathjax/MathJax/master/extensions/MathMenu.js",
                               filename=pjoin(head, 'ext/ajax/libs/mathjax/2.7.1/extensions/MathMenu.js'))

    # get reveal
    with tempfile.TemporaryDirectory() as tmpdir:

        r = requests.get(
            "https://github.com/hakimel/reveal.js/archive/3.2.0.zip")
        with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
            zip_ref.extractall(tmpdir)
            reveal_dir = os.path.join(
                tmpdir, zip_ref.filelist[0].filename[:-1]) + '\\'
            os.renames(reveal_dir, pjoin(head, 'ext/ajax/libs/reveal.js'))


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Hacky program to make a jupyter \
                                                  notebook into offline reveal.js slideshow.\n \
                                                  Will create a .slides.offline.html next to \
                                                  the notebook as well as a ext/ folder including all of the required files.\
                                                  You need to copy both of those for the presentation to work.')
    parser.add_argument('notebook_path', type=str,
                        help='Path to the .ipynb notebook')

    args = parser.parse_args()

    export_to_offline_slides(args.notebook_path)


if __name__ == '__main__':
    main()
