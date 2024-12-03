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
from nomad.config import config
from nomad.parsing.parser import MatchingParser

from nomad_greenlight_plugin import read_files as rf
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
        if logger is not None:
            logger.info('GreenlightParser.parse', parameter=configuration.parameter)

        # archive.workflow2 = Workflow(name='test')
        data_file_object = rf.read_files(mainfile)
        data = data_file_object.data

        # archive.metadata.entry_name = os.path.basename(mainfile)
        # archive.metadata.external_id = data[0][1:]
        archive.data = GreenlightSchemaPackage()
        print(archive.data.__dict__)

        for name in data.columns:
            if name in archive.data:
                try:
                    # print(archive.data, name, data[name].values[0])
                    setattr(archive.data, name, data[name])
                    # print(id(getattr(archive.data, name)))
                except (ValueError, TypeError) as E:
                    print(name)
                    print(data[name])
                    raise E
        # print(archive.data.__dict__)
        archive.data.name = data_file_object.header['Test Name']
        # item = data_file_object.data['cell_voltage_total']
        # archive.data.cell_voltage = item
        # archive.data.cell_voltage.unit = data_file_object.units['cell_voltage_total']
        # pass
        # archive.data.current_density = data_file_object.data['current_density']
        # archive.data.current_density.unit = data_file_object.units['current_density']
        # archive.data.current = data_file_object.data['current']
