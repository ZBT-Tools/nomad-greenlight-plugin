from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class GreenlightSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_greenlight_plugin.schema_packages.schema_package import m_package

        return m_package


schema_package_entry_point = GreenlightSchemaPackageEntryPoint(
    name='GreenlightSchemaPackage',
    description='New schema package entry point configuration.',
)
