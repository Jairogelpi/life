"""
LIFE — Living Infrastructure for Agents
The framework that solves the 10 gaps no one else has.
"""

from life.core import LifeAgent
from life.dna import DNA, Personality
from life.hormones import EndocrineSystem
from life.immune import ImmuneSystem
from life.nervous import NervousSystem
from life.homeostasis import Homeostasis
from life.context import ClawNetContext
from life.vibe import Vibe, VibeProtocol
from life.genesis import Genesis, Discovery
from life.observation import ObservationSystem

__version__ = "1.1.0"
__all__ = [
    "LifeAgent",
    "DNA",
    "Personality",
    "EndocrineSystem",
    "ImmuneSystem",
    "NervousSystem",
    "Homeostasis",
    "ClawNetContext",
    "Vibe",
    "VibeProtocol",
    "Genesis",
    "Discovery",
    "ObservationSystem",
]
