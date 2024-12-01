from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

# Import additional libraries

from echem_data import electrochem_data as ed
from nomad.config import config
from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.parser import MatchingParser

from nomad_greenlight_plugin.schema_packages.schema_package import (
    GreenlightSchemaPackage,
)

configuration = config.get_plugin_entry_point(
    'nomad_greenlight_plugin.parsers:parser_entry_point'
)


class GreenlightParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('GreenlightParser.parse', parameter=configuration.parameter)

        archive.workflow2 = Workflow(name='test')
        data_file_object = ed.EChemDataFile(mainfile, 'Greenlight')

        # archive.metadata.entry_name = os.path.basename(mainfile)
        # archive.metadata.external_id = data[0][1:]
        archive.data = GreenlightSchemaPackage()
        print(data_file_object.data.columns)
        archive.data.name = data_file_object.header['Test Name']
        archive.data.cell_voltage = data_file_object.data['cell_voltage_total']
        # archive.data.cell_voltage.unit = data_file_object.units['cell_voltage_total']
        archive.data.current_density = data_file_object.data['current_density']
        # archive.data.current_density.unit = data_file_object.units['current_density']
        # archive.data.current = data_file_object.data['current']
