from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class GreenlightParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_greenlight_plugin.parsers.parser import GreenlightParser

        return GreenlightParser(**self.dict())


parser_entry_point = GreenlightParserEntryPoint(
    name='GreenlightParser',
    description='Greenlight parser entry point configuration.',
    # mainfile_name_re='.greenlight.',
    mainfile_contents_re='\s*\n\s*Emerald Version',
)
