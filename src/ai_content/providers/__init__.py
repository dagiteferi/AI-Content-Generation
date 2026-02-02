"""
Providers module.

Import this module to register all available providers.
"""

# Import provider modules to trigger registration
from ai_content.providers import google
from ai_content.providers import loudly # Added loudly
from ai_content.providers import kling

# Re-export providers
from ai_content.providers.google import (
    GoogleLyriaProvider,
    GoogleVeoProvider,
    GoogleImagenProvider,
)
from ai_content.providers.loudly import ( # Changed from aimlapi
    LoudlyMusicProvider,
)
from ai_content.providers.kling import (
    KlingDirectProvider,
)

__all__ = [
    # Google
    "GoogleLyriaProvider",
    "GoogleVeoProvider",
    "GoogleImagenProvider",
    # Loudly
    "LoudlyMusicProvider", # Changed from AIMLAPI
    # Kling
    "KlingDirectProvider",
]
