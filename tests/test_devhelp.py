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
    result = (app.outdir / output_file).text(encoding='utf-8')

    assert '<?xml version="1.0" encoding="utf-8" standalone="no"?>' in result
    assert '<book' in result
    assert '<chapters' in result
    assert '<functions' in result


@pytest.mark.sphinx('devhelp', testroot='indexkeywords')
def test_devhelp_index(app):
    app.builder.build_all()
    output_file = app.config.devhelp_basename + '.devhelp2'
    result = (app.outdir / output_file).text(encoding='utf-8')

    index = ElementTree.fromstring(result)

    chapters, functions = index.getchildren()

    sub_element = chapters[0]
    assert sub_element.tag == '{http://www.devhelp.net/book}sub'
    assert 'name' in sub_element.keys() and sub_element.attrib['name'] == 'foo'
    assert 'link' in sub_element.keys() and \
           sub_element.attrib['link'] == 'foo.html'
    assert 'link' in sub_element.keys()

    keyword_element = functions[0]
    assert keyword_element.tag == '{http://www.devhelp.net/book}keyword'
    assert 'name' in keyword_element.keys() and \
           keyword_element.get('name') == 'sphinx'
    assert 'link' in keyword_element.keys() and \
           keyword_element.get('link') == 'index.html#module-sphinx'
    assert 'type' in keyword_element.keys() and \
           keyword_element.get('type') == 'module'
