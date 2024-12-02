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

import numpy as np
import pandas as pd
import plotly.express as px
from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import Quantity, SchemaPackage

configuration = config.get_plugin_entry_point(
    'nomad_greenlight_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class GreenlightSchemaPackage(PlotSection, Schema):
    name = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    message = Quantity(type=str)
    cell_voltage = Quantity(type=np.float64, shape=['*'], unit='V')
    current_density = Quantity(type=np.float64, shape=['*'], unit='A/cm^2')

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        if logger is not None:
            logger.info('GreenlightSchema.normalize',
                        parameter=configuration.parameter)
        archive.metadata.entry_name = self.name
        self.figures.append(
            PlotlyFigure(
                figure=px.line(
                    pd.DataFrame(
                        dict(
                            current_density=self.current_density,
                            cell_voltage=self.cell_voltage,
                        )
                    ),
                    x='current_density',
                    y='cell_voltage',
                ).to_plotly_json()
            )
        )



m_package.__init_metainfo__()
