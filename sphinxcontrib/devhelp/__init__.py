"""
    sphinxcontrib.devhelp
    ~~~~~~~~~~~~~~~~~~~~~

    Build HTML documentation and Devhelp_ support files.

    .. _Devhelp: https://wiki.gnome.org/Apps/Devhelp

    :copyright: Copyright 2007-2019 by the Sphinx team, see README.
    :license: BSD, see LICENSE for details.
"""

import codecs
from os import path
from typing import Any, Dict

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import get_translation
from sphinx.util import logging
from sphinx.util.nodes import NodeMatcher
from sphinx.util.osutil import make_filename

from sphinxcontrib.devhelp.version import __version__

try:
    import xml.etree.ElementTree as etree
except ImportError:
    import lxml.etree as etree  # type: ignore


if False:
    # For type annotation
    from typing import List  # NOQA


logger = logging.getLogger(__name__)
__ = get_translation(__name__, 'console')

package_dir = path.abspath(path.dirname(__file__))


class DevhelpBuilder(StandaloneHTMLBuilder):
    """
    Builder that also outputs GNOME Devhelp file.
    """
    name = 'devhelp'
    epilog = __('To view the help file:\n'
                '$ mkdir -p $HOME/.local/share/devhelp/books\n'
                '$ ln -s $PWD/%(outdir)s $HOME/.local/share/devhelp/books/%(project)s\n'
                '$ devhelp')

    # don't copy the reST source
    copysource = False
    supported_image_types = ['image/png', 'image/gif', 'image/jpeg']

    # don't add links
    add_permalinks = False
    # don't add sidebar etc.
    embedded = True

    def init(self):
        # type: () -> None
        super().init()
        self.out_suffix = '.html'
        self.link_suffix = '.html'

    def handle_finish(self):
        # type: () -> None
        self.build_devhelp(self.outdir, self.config.devhelp_basename)

    def build_devhelp(self, outdir, outname):
        # type: (str, str) -> None
        logger.info(__('dumping devhelp index...'))

        # Basic info

        # TODO: author attrib
        # TODO: language attrib
        root = etree.Element('book',
                             xmlns='http://www.devhelp.net/book',
                             title=self.config.html_title,
                             name=self.config.project,
                             link="index.html",
                             version=self.config.version,
                             language='',
                             author='')
        tree = etree.ElementTree(root)

        # TOC
        chapters = etree.SubElement(root, 'chapters')

        tocdoc = self.env.get_and_resolve_doctree(
            self.config.master_doc, self, prune_toctrees=False)

        def write_toc(node, parent):
            # type: (nodes.Node, etree.Element) -> None
            if isinstance(node, addnodes.compact_paragraph) or \
               isinstance(node, nodes.bullet_list):
                for subnode in node:
                    write_toc(subnode, parent)
            elif isinstance(node, nodes.list_item):
                item = etree.SubElement(parent, 'sub')
                for subnode in node:
                    write_toc(subnode, item)
            elif isinstance(node, nodes.reference):
                parent.attrib['link'] = node['refuri']
                parent.attrib['name'] = node.astext()

        matcher = NodeMatcher(addnodes.compact_paragraph, toctree=Any)
        for node in tocdoc.traverse(matcher):  # type: addnodes.compact_paragraph
            write_toc(node, chapters)

        # Index keywords
        functions = etree.SubElement(root, 'functions')
        if self.domain_indices:
            for domain_name in sorted(self.env.domains):
                for domain_data in self.env.domains[domain_name].get_objects():
                    name, _, _type, docname, anchor, _ = domain_data
                    link = '{docname}.html#{anchor}'.format(docname=docname,
                                                            anchor=anchor)
                    etree.SubElement(functions, 'keyword',
                                     name=name, link=link, type=_type)

        # Dump the XML file
        xmlfile = path.join(outdir, outname + '.devhelp2')
        with codecs.open(xmlfile, 'a', 'utf-8') as f:
            xmlheader = '<?xml version="1.0" encoding="utf-8" standalone="no"?>'
            xmltree = (etree.tostring(tree.getroot(), method='xml')).decode('utf-8')
            xmlbody = xmlheader + xmltree
            f.write(xmlbody)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension('sphinx.builders.html')
    app.add_builder(DevhelpBuilder)
    app.add_message_catalog(__name__, path.join(package_dir, 'locales'))

    app.add_config_value('devhelp_basename', lambda self: make_filename(self.project), None)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
