import logging

from nomad.datamodel import EntryArchive

from nomad_greenlight_plugin.parsers.parser import GreenlightParser


def test_parse_file():
    parser = GreenlightParser()
    archive = EntryArchive()
    parser.parse('tests/data/example.out', archive, logging.getLogger())

    assert archive.workflow2.name == 'test'
