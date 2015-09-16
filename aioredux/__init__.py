import pbr.version

from .core import Store  # noqa

__version__ = pbr.version.VersionInfo(
    'aioredux').version_string()
