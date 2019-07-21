"""
    test_devhelp
    ~~~~~~~~~~~~

    Test for devhelp extension.

    :copyright: Copyright 2007-2019 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import xml.etree.cElementTree as ElementTree

import pytest


@pytest.mark.sphinx('devhelp', testroot='basic')
def test_devhelp_basic(app):
    app.builder.build_all()
    output_file = app.config.devhelp_basename + '.devhelp2'
    result = (app.outdir / output_file).text()

    assert '<?xml version="1.0" encoding="utf-8" standalone="no"?>' in result
    assert '<book' in result
    assert '<chapters' in result
    assert '<functions' in result


@pytest.mark.sphinx('devhelp', testroot='indexkeywords')
def test_devhelp_index(app):
    app.builder.build_all()
    output_file = app.config.devhelp_basename + '.devhelp2'
    result = (app.outdir / output_file).text()

    index = ElementTree.fromstring(result)
    assert index.attrib['language'] == 'unknown'

    chapters, functions = index.getchildren()

    sub_element = chapters[0]
    assert sub_element.tag == '{http://www.devhelp.net/book}sub'
    assert sub_element.attrib['name'] == 'foo'
    assert sub_element.attrib['link'] == 'foo.html'

    keyword_element = functions[0]
    assert keyword_element.tag == '{http://www.devhelp.net/book}keyword'
    assert keyword_element.get('name') == 'sphinx'
    assert keyword_element.get('link') == 'index.html#module-sphinx'
    assert keyword_element.get('type') == 'module'
