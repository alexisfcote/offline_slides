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
from nbconvert import SlidesExporter, HTMLExporter


def _get_relative_file_location(url, prefix = 'ext/'):
    return pjoin(prefix, urlparse(url).path[1:])

def _add_as_offline_ressource(url, path_prefix):
    """download file at url to the ext/ path location and return its local path

    Arguments:
        url {str} -- url of the file
        path_prefix {str} -- path prefix of where to download

    Returns:
        str -- file location
    """
    rel_location = _get_relative_file_location(url)
    (path, lib_filename) = os.path.split(rel_location)
    os.makedirs(pjoin(path_prefix, path), exist_ok=True)
    file_location, headers = urllib.request.urlretrieve(
        url, filename=pjoin(path_prefix, path, lib_filename))
    return # pjoin(path, lib_filename)


def export_to_offline(ipynb_path, slides=True, template_file=None, reveal_scroll=True, no_download=False, verbose=False):
    head, filename = os.path.split(ipynb_path)
    head = './' if head == '' else head

    if slides:
        # Export ipynb to html reveal.js slides
        exporter = SlidesExporter()
        exporter.reveal_theme = 'white'
        exporter.reveal_url_prefix = 'ext/ajax/libs/reveal.js'
        exporter.reveal_scroll=reveal_scroll
    else:
        exporter = HTMLExporter()

    if template_file:
        exporter.template_file = template_file

    if slides:
        suffix = '.slides.offline.html'
    else:
        suffix = '.offline.html'

    new_filename = ''.join(
        (os.path.splitext(filename)[0], suffix))

    if verbose: print('Converting')
    with open(pjoin(head, filename), 'r', encoding='utf-8') as f:
        (body, _) = exporter.from_file(f)

    is_ext_folder = os.path.isdir(pjoin(head, 'ext'))
    to_download = not no_download
    if to_download and is_ext_folder:
        if verbose: print('Removing ext folder.')
        shutil.rmtree(pjoin(head, 'ext'))

    # exp = re.compile('\"http.*cdnjs.*\"')
    exp = re.compile('[\"\']http.*cdn[^\"\']+[\"\']')

    with open(pjoin(head, new_filename), 'w', encoding='utf-8') as fout:
        for url in re.findall(exp, body):
            if 'reveal' in url:
                continue
            url = url.replace('"', '').replace("'", '').split(' ')[0]
            url_get = url + '.js' if 'plotly' in url else url
            if 'http' not in url:
                continue
            local_url = _get_relative_file_location(url_get)
            if to_download:
                if verbose: print('Downloading asset - {}'.format(url_get))
                _add_as_offline_ressource(url_get, path_prefix=head)
            local_url_replace = local_url[0:-3] if 'plotly' in url else local_url
            body = body.replace(url, local_url_replace)
        fout.write(body)

    # get missing mathjax files
    if to_download:
        os.makedirs(
            pjoin(head, 'ext/ajax/libs/mathjax/2.7.1/extensions/'), exist_ok=True)
        urllib.request.urlretrieve("https://raw.githubusercontent.com/mathjax/MathJax/master/extensions/MathZoom.js",
                                filename=pjoin(head, 'ext/ajax/libs/mathjax/2.7.1/extensions/MathZoom.js'))
        urllib.request.urlretrieve("https://raw.githubusercontent.com/mathjax/MathJax/master/extensions/MathMenu.js",
                                filename=pjoin(head, 'ext/ajax/libs/mathjax/2.7.1/extensions/MathMenu.js'))
        if verbose: print('Downloaded mathjax extensions')

    # get reveal
    if slides:
        with tempfile.TemporaryDirectory() as tmpdir:
            if to_download:
                if verbose: print('Downloading revealjs')
                r = requests.get(
                    "https://github.com/hakimel/reveal.js/archive/3.2.0.zip")
                with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
                    zip_ref.extractall(tmpdir)
                    reveal_dir = os.path.join(
                        tmpdir, zip_ref.filelist[0].filename[:-1]) #+ '/' #+ '\\'
                    # os.renames(reveal_dir, pjoin(head, 'ext/ajax/libs/reveal.js'))
                    shutil.move(reveal_dir, pjoin(head, 'ext/ajax/libs/reveal.js'))


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Hacky program to make a jupyter \
                                                  notebook into offline reveal.js slideshow.\n \
                                                  Will create a .slides.offline.html next to \
                                                  the notebook as well as a ext/ folder including all of the required files.\
                                                  You need to copy both of those for the presentation to work.')
    parser.add_argument('notebook_path', type=str,
                        help='Path to the .ipynb notebook')
    parser.add_argument('--html', action='store_false',
                        help='Export as offline standalone html')
    parser.add_argument('--no-download', '-n', action='store_true',
                        help='Do not download files if ext folder exists')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Do not download files if ext folder exists')                        
    args = parser.parse_args()

    print('ow', args.no_download)
    export_to_offline(args.notebook_path, slides=args.html, no_download=args.no_download, verbose=args.verbose)


if __name__ == '__main__':
    main()
