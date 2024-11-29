from nomad.config.models.plugins import NormalizerEntryPoint
from pydantic import Field


class GreenlightNormalizerEntryPoint(NormalizerEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_greenlight_plugin.normalizers.normalizer import GreenlightNormalizer

        return GreenlightNormalizer(**self.dict())


normalizer_entry_point = GreenlightNormalizerEntryPoint(
    name='GreenlightNormalizer',
    description='New normalizer entry point configuration.',
)
