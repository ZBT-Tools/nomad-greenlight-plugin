import os.path

from nomad.client import normalize_all, parse
from nomad.units import ureg


def test_schema_package():
    # test_file = os.path.join(
    #   'tests', 'data',
    #   'maxcoat-80ti-ast_gts1_ast-mc - 230715 074738 - part_0.csv')
    # test_file = os.path.abspath(os.path.join('tests', 'data',
    #                                          'test_greenlight.csv'))
    # test_file = os.path.join('tests', 'data', 'test_greenlight.csv')
    test_file = os.path.join(
        'tests', 'data', 'maxcoat-80ti-ast_gts1_ast-mc - 230715 074738 - part_0.csv'
    )

    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    assert entry_archive.data.current_density.units == ureg.Unit('A / cm^2')


test_schema_package()
