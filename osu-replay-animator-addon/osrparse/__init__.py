from importlib import metadata

from .utils import (GameMode, Mod, Key, ReplayEvent, ReplayEventOsu,
    ReplayEventTaiko, ReplayEventMania, ReplayEventCatch, KeyTaiko, KeyMania)
from .replay import Replay, parse_replay_data

'''
__version__ = metadata.version(__package__)

__all__ = ["GameMode", "Mod", "Replay", "ReplayEvent", "Key",
    "ReplayEventOsu", "ReplayEventTaiko", "ReplayEventMania",
    "ReplayEventCatch", "KeyTaiko", "KeyMania", "parse_replay_data"]
'''
