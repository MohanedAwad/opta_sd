"""
opta_sd
~~~~~~~~~~
Python client for the OPTA Sports Data Soccer API.

Quick start::
    from opta_sdapi.soccer import Match
    match =await Match().resource("bsu6pjne1eqz2hs8r3685vbhl").live().lineups().get()
    print(match.data)
"""

from .core        import Core
from .cache       import CacheBackend, FileCache, MemoryCache, NoCache
from .exceptions  import (
    APIError, ConfigurationError, MissingParameterError,
    OptaSDAPIError, ParseError,
)
from . import soccer
__version__ = "0.1.0"
__all__ = [
    "Core",
    "CacheBackend", "FileCache", "MemoryCache", "NoCache",
    "OptaSDAPIError", "ConfigurationError", "APIError",
    "ParseError", "MissingParameterError",
    "soccer",
]