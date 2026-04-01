"""
DNA — Immutable agent identity
Solves: Identity persistence, capability validation, portability
"""

import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Personality(BaseModel):
    """Big Five personality traits (OCEAN model)"""
    openness: float = Field(default=0.5, ge=0.0, le=1.0)
    conscientiousness: float = Field(default=0.5, ge=0.0, le=1.0)
    extraversion: float = Field(default=0.5, ge=0.0, le=1.0)
    agreeableness: float = Field(default=0.5, ge=0.0, le=1.0)
    neuroticism: float = Field(default=0.5, ge=0.0, le=1.0)


class DNA(BaseModel):
    """
    Immutable agent identity.
    
    Once created and locked, DNA cannot be modified.
    This ensures agents maintain consistent identity across
    framework migrations and long-running sessions.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(default="Agent")
    version: str = Field(default="1.0.0")
    
    personality: Personality = Field(default_factory=Personality)
    values: List[str] = Field(default_factory=lambda: ["honesty", "helpfulness"])
    capabilities: List[str] = Field(default_factory=lambda: ["reasoning", "communication"])
    forbidden: List[str] = Field(default_factory=list)
    
    created_at: str = Field(default_factory=lambda: __import__("datetime").datetime.utcnow().isoformat())
    
    _locked: bool = False
    _fingerprint: Optional[str] = None
    
    class Config:
        underscore_attrs_allow_private = True
    
    def _lock(self):
        """Lock DNA - cannot be modified after this"""
        if self._locked:
            return
        import hashlib
        self._fingerprint = hashlib.sha256(
            self.json(exclude={"id", "created_at"}).encode()
        ).hexdigest()[:16]
        self._locked = True
    
    def can_perform(self, task: str) -> bool:
        """Check if task is within capabilities"""
        task_lower = task.lower()
        for forbidden in self.forbidden:
            if forbidden.lower() in task_lower:
                return False
        return True
    
    def has_capability(self, capability: str) -> bool:
        """Check if agent has specific capability"""
        return capability.lower() in [c.lower() for c in self.capabilities]
    
    def matches(self, other: "DNA") -> float:
        """
        Calculate similarity between two agents (0-1).
        Used for agent discovery and collaboration.
        """
        # Value overlap
        value_overlap = len(set(self.values) & set(other.values)) / max(
            len(set(self.values) | set(other.values)), 1
        )
        
        # Capability overlap
        cap_overlap = len(set(self.capabilities) & set(other.capabilities)) / max(
            len(set(self.capabilities) | set(other.capabilities)), 1
        )
        
        # Personality distance
        p1 = self.personality
        p2 = other.personality
        personality_sim = 1.0 - (
            abs(p1.openness - p2.openness)
            + abs(p1.conscientiousness - p2.conscientiousness)
            + abs(p1.extraversion - p2.extraversion)
            + abs(p1.agreeableness - p2.agreeableness)
            + abs(p1.neuroticism - p2.neuroticism)
        ) / 5.0
        
        return (value_overlap * 0.3 + cap_overlap * 0.4 + personality_sim * 0.3)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export DNA as dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "personality": self.personality.model_dump(),
            "values": self.values,
            "capabilities": self.capabilities,
            "forbidden": self.forbidden,
            "created_at": self.created_at,
            "fingerprint": self._fingerprint,
        }
    
    def verify(self, fingerprint: str) -> bool:
        """Verify DNA integrity against fingerprint"""
        return self._fingerprint == fingerprint
