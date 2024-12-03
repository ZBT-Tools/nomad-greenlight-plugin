import os
import logging

from nomad.datamodel import EntryArchive

from nomad_greenlight_plugin.parsers.parser import GreenlightParser


def test_parse_file():
    # test_file = os.path.join('tests', 'data', 'maxcoat-80ti-ast_gts1_ast-mc - 230715 074738 - part_0.csv')
    # test_file = os.path.abspath(os.path.join('..', '..', 'tests', 'data', 'test_greenlight.csv'))
    # test_file = os.path.join('tests', 'data', 'test_greenlight.csv')
    test_file = os.path.join('tests', 'data', 'maxcoat-80ti-ast_gts1_ast-mc - 230715 074738 - part_0.csv')

    parser = GreenlightParser()
    archive = EntryArchive()
    parser.parse(test_file, archive, logging.getLogger())
    assert hasattr(archive.data, 'time_stamp')
