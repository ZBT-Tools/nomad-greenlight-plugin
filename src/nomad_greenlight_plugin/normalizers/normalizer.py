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

from nomad.config import config
from nomad.normalizing import Normalizer

configuration = config.get_plugin_entry_point(
    'nomad_greenlight_plugin.normalizers:normalizer_entry_point'
)


class GreenlightNormalizer(Normalizer):
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        logger.info('GreenlightNormalizer.normalize', parameter=configuration.parameter)
        if archive.results and archive.results.material:
            archive.results.material.elements = ['C', 'O']
