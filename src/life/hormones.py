"""
Endocrine System — Hormonal modulation of agent behavior
Solves: Behavior regulation, reward signals, stress management
"""

from typing import Dict, Optional
from pydantic import BaseModel, Field
import math


HORMONE_LIMITS = {
    "dopamine": (0.0, 1.0),
    "cortisol": (0.0, 1.0),
    "serotonin": (0.0, 1.0),
    "adrenaline": (0.0, 1.0),
    "oxytocin": (0.0, 1.0),
}

DEFAULT_LEVELS = {
    "dopamine": 0.5,
    "cortisol": 0.1,
    "serotonin": 0.5,
    "adrenaline": 0.1,
    "oxytocin": 0.5,
}


class EndocrineSystem:
    """
    Hormonal modulation system.
    
    Each hormone modulates agent behavior:
    - Dopamine: Reward signal, reinforces successful behaviors
    - Cortisol: Stress response, increases caution
    - Serotonin: Mood stabilizer, prevents oscillations
    - Adrenaline: Urgency, accelerates responses
    - Oxytocin: Trust, modulates collaboration openness
    """
    
    def __init__(self, initial: Optional[Dict[str, float]] = None):
        self._levels: Dict[str, float] = {**DEFAULT_LEVELS}
        if initial:
            for key, value in initial.items():
                if key in HORMONE_LIMITS:
                    lo, hi = HORMONE_LIMITS[key]
                    self._levels[key] = max(lo, min(hi, value))
        self._history: list = []
    
    def inject(self, hormone: str, amount: float) -> float:
        """
        Inject hormone (positive or negative amount).
        Returns new level.
        """
        if hormone not in self._levels:
            raise ValueError(f"Unknown hormone: {hormone}")
        
        lo, hi = HORMONE_LIMITS[hormone]
        old = self._levels[hormone]
        new = max(lo, min(hi, old + amount))
        self._levels[hormone] = new
        
        self._history.append({
            "hormone": hormone,
            "amount": amount,
            "old": old,
            "new": new,
        })
        
        return new
    
    def get(self, hormone: str) -> float:
        """Get current hormone level"""
        return self._levels.get(hormone, 0.0)
    
    def levels(self) -> Dict[str, float]:
        """Get all hormone levels"""
        return dict(self._levels)
    
    def set_levels(self, levels: Dict[str, float]):
        """Set hormone levels directly"""
        for key, value in levels.items():
            if key in HORMONE_LIMITS:
                lo, hi = HORMONE_LIMITS[key]
                self._levels[key] = max(lo, min(hi, value))
    
    def decay(self, rate: float = 0.05):
        """
        Natural decay toward baseline.
        Hormones naturally return to default levels.
        """
        for hormone in self._levels:
            default = DEFAULT_LEVELS[hormone]
            current = self._levels[hormone]
            diff = current - default
            self._levels[hormone] = current - (diff * rate)
    
    def modulate_speed(self, base: float) -> float:
        """
        Modulate processing speed based on hormones.
        Adrenaline = faster, Cortisol = slower
        """
        adren = self._levels["adrenaline"]
        cort = self._levels["cortisol"]
        return base * (1.0 + adren * 0.5 - cort * 0.3)
    
    def modulate_creativity(self, base: float) -> float:
        """
        Modulate creativity based on hormones.
        Dopamine + high serotonin = creative
        High cortisol = conservative
        """
        dopa = self._levels["dopamine"]
        sert = self._levels["serotonin"]
        cort = self._levels["cortisol"]
        return base * (1.0 + dopa * 0.3 + sert * 0.2 - cort * 0.4)
    
    def modulate_trust(self, base: float) -> float:
        """
        Modulate trust/openness based on hormones.
        Oxytocin = more trusting, Cortisol = more cautious
        """
        oxy = self._levels["oxytocin"]
        cort = self._levels["cortisol"]
        return base * (1.0 + oxy * 0.4 - cort * 0.5)
    
    def snapshot(self) -> Dict[str, float]:
        """Snapshot current levels"""
        return dict(self._levels)
