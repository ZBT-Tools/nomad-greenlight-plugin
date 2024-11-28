from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class GreenlightParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_greenlight_plugin.parsers.parser import GreenlightParser

        return GreenlightParser(**self.dict())


parser_entry_point = GreenlightParserEntryPoint(
    name='GreenlightParser',
    description='New parser entry point configuration.',
    mainfile_name_re='.*\.newmainfilename',
)
