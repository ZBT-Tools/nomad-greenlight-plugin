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

import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import Quantity, SchemaPackage

from nomad_greenlight_plugin import read_files as rf
import pint

configuration = config.get_plugin_entry_point(
    'nomad_greenlight_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


def decorator(cls):
    cls.initialize_quantities()
    return cls


@decorator
class GreenlightSchemaPackage(PlotSection, Schema):
    name = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    message = Quantity(type=str)

    # cell_voltage = Quantity(type=np.float64, shape=['*'], unit='V')
    # current_density = Quantity(type=np.float64, shape=['*'], unit='A/cm^2')
    @classmethod
    def initialize_quantities(cls):
        # Initialize all data quantities from empty template csv file
        empty_file_path = os.path.join(os.path.dirname(__file__), 'greenlight_empty.csv')
        data_file_object = rf.read_single_file(empty_file_path)
        columns = data_file_object.data.columns
        units = data_file_object.units
        df = data_file_object.data
        dtypes = df.dtypes
        type_dict = df.dtypes.to_dict()
        for k, v in type_dict.items():
            if isinstance(v, np.dtypes.ObjectDType):
                type_dict[k] = str
        quantities = {}
        for col in columns:
            try:
                quantities[col] = Quantity(type=type_dict[col], shape=['*'], unit=units[col])
            except (pint.errors.UndefinedUnitError, ValueError, AttributeError):
                quantities[col] = Quantity(type=type_dict[col], shape=['*'], unit='dimensionless')
            # print(col, quantities[col],  quantities[col].unit, quantities[col].type)
        # Dynamically assign dictionary entries as object attributes
        for key, value in quantities.items():
            # print(cls, key, value)
            setattr(cls, key, value)
            # print(id(getattr(cls, key)))
        print(cls.__dict__)
        setattr(cls, 'quantity_names', columns)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        if logger is not None:
            logger.info('GreenlightSchema.normalize',
                        parameter=configuration.parameter)
        archive.metadata.entry_name = self.name

        # Make plot
        # Add figure
        plot_df = pd.DataFrame(
            dict(date_time=self.date_time,
                 current_density=self.current,
                 cell_voltage=self.cell_voltage_total))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add lines
        fig.add_trace(go.Scatter(x=plot_df['date_time'], y=plot_df['cell_voltage'], name="Cell Voltage / V"),
                      secondary_y=False)
        fig.add_trace(go.Scatter(x=plot_df['date_time'], y=plot_df['current'], name="Cell Voltage / V"),
                      secondary_y=True)
        # Set x-axis title
        fig.update_xaxes(title_text="Time / s")
        # Set y-axes titles
        fig.update_yaxes(title_text="Voltage / V", secondary_y=False)
        fig.update_yaxes(title_text="Current / A", secondary_y=True)
        self.figures.append(PlotlyFigure(fig.to_plotly_json()))

        # figure = px.line(plot_df, x='date_time', y='cell_voltage')
        # fig.add_scatter(x=plot_df['date_time'], y=plot_df['current'], mode='lines')
        # self.figures.append(
        #    PlotlyFigure(
        #        figure=px.line(
        #            pd.DataFrame(
        #                dict(
        #                    date_time=self.date_time,
        #                    current=self.current,
        #                    cell_voltage=self.cell_voltage_total,
        #                )
        #            ),
        #            x='current_density',
        #           y='cell_voltage',
        #        ).to_plotly_json()
        #    )
        # )


m_package.__init_metainfo__()
