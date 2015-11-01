import pbr.version

from .core import create_store  # noqa
from .utils import apply_middleware, combine_reducers  # noqa


__version__ = pbr.version.VersionInfo(
    'aioredux').version_string()
