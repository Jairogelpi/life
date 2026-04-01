"""
ClawNet Context — Memory portability between agents
Solves: Framework lock-in, context loss, semantic drift
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json


@dataclass
class ContextEntry:
    """A single context entry with lineage"""
    key: str
    value: Any
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    created_by: str = ""
    locked: bool = False
    version: int = 1
    lineage: List[Dict[str, Any]] = field(default_factory=list)
    freshness: float = 1.0  # 1.0 = fresh, 0.0 = stale


class ClawNetContext:
    """
    Portable context with locking and lineage tracking.
    
    This is the memory system that can move between agents
    without losing context. It solves the "memory rot" problem
    by tracking freshness and preventing semantic drift.
    """
    
    def __init__(self, agent_id: str = ""):
        self.agent_id = agent_id
        self._entries: Dict[str, ContextEntry] = {}
        self._locks: Dict[str, str] = {}
        self._migration_history: List[Dict] = []
    
    def set(self, key: str, value: Any, lineage: bool = True) -> None:
        """Set context value"""
        if key in self._locks and self._locks[key] != self.agent_id:
            raise PermissionError(f"Context key '{key}' is locked by another agent")
        
        if key in self._entries:
            entry = self._entries[key]
            if entry.locked:
                raise PermissionError(f"Context key '{key}' is locked")
            old_value = entry.value
            entry.value = value
            entry.modified_at = datetime.utcnow().isoformat()
            entry.version += 1
            entry.freshness = 1.0
            if lineage:
                entry.lineage.append({
                    "action": "modify",
                    "by": self.agent_id,
                    "at": entry.modified_at,
                    "old_hash": hashlib.sha256(json.dumps(old_value, default=str).encode()).hexdigest()[:8],
                    "new_hash": hashlib.sha256(json.dumps(value, default=str).encode()).hexdigest()[:8],
                })
        else:
            self._entries[key] = ContextEntry(
                key=key,
                value=value,
                created_by=self.agent_id,
                lineage=[{"action": "create", "by": self.agent_id, "at": datetime.utcnow().isoformat()}] if lineage else [],
            )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get context value"""
        entry = self._entries.get(key)
        if entry:
            # Update freshness on access
            entry.freshness = min(1.0, entry.freshness + 0.05)
            return entry.value
        return default
    
    def lock(self, key: str) -> None:
        """Lock context key (no more modifications)"""
        if key in self._entries:
            self._entries[key].locked = True
            self._locks[key] = self.agent_id
            self._entries[key].lineage.append({
                "action": "lock",
                "by": self.agent_id,
                "at": datetime.utcnow().isoformat(),
            })
    
    def unlock(self, key: str) -> None:
        """Unlock context key"""
        if key in self._entries and self._locks.get(key) == self.agent_id:
            self._entries[key].locked = False
            del self._locks[key]
            self._entries[key].lineage.append({
                "action": "unlock",
                "by": self.agent_id,
                "at": datetime.utcnow().isoformat(),
            })
    
    def decay(self, rate: float = 0.01):
        """
        Decay freshness of all entries.
        Freshness decays over time, simulating memory aging.
        Fresh entries are preferred in retrieval.
        """
        for entry in self._entries.values():
            entry.freshness = max(0.0, entry.freshness - rate)
    
    def migrate_to(self, target: "ClawNetContext") -> None:
        """
        Migrate all context to another agent.
        This is the PORTABILITY feature that solves framework lock-in.
        """
        migration_record = {
            "from": self.agent_id,
            "to": target.agent_id,
            "entries": len(self._entries),
            "at": datetime.utcnow().isoformat(),
        }
        
        for key, entry in self._entries.items():
            # Copy entry to target
            target._entries[key] = ContextEntry(
                key=entry.key,
                value=entry.value,
                created_at=entry.created_at,
                modified_at=entry.modified_at,
                created_by=entry.created_by,
                locked=entry.locked,
                version=entry.version,
                lineage=entry.lineage + [{"action": "migrate", "from": self.agent_id, "to": target.agent_id, "at": datetime.utcnow().isoformat()}],
                freshness=entry.freshness,
            )
        
        self._migration_history.append(migration_record)
        target._migration_history.append(migration_record)
    
    def export(self) -> Dict[str, Any]:
        """Export context for serialization"""
        return {
            "agent_id": self.agent_id,
            "entries": {
                k: {
                    "key": v.key,
                    "value": v.value,
                    "created_at": v.created_at,
                    "modified_at": v.modified_at,
                    "created_by": v.created_by,
                    "locked": v.locked,
                    "version": v.version,
                    "lineage": v.lineage,
                    "freshness": v.freshness,
                }
                for k, v in self._entries.items()
            },
            "migration_history": self._migration_history,
        }
    
    def import_data(self, data: Dict[str, Any]) -> None:
        """Import context from exported data"""
        self.agent_id = data.get("agent_id", self.agent_id)
        for key, entry_data in data.get("entries", {}).items():
            self._entries[key] = ContextEntry(**entry_data)
        self._migration_history = data.get("migration_history", [])
    
    def lineage(self, key: Optional[str] = None) -> List[Dict]:
        """Get lineage history"""
        if key and key in self._entries:
            return self._entries[key].lineage
        return self._migration_history
    
    def get_fresh(self, min_freshness: float = 0.5) -> Dict[str, Any]:
        """
        Get only fresh entries.
        Solves semantic drift by preferring recent data.
        """
        return {
            k: v.value
            for k, v in self._entries.items()
            if v.freshness >= min_freshness
        }
    
    def stats(self) -> Dict[str, Any]:
        """Get context statistics"""
        entries = list(self._entries.values())
        return {
            "total_entries": len(entries),
            "locked": sum(1 for e in entries if e.locked),
            "avg_freshness": sum(e.freshness for e in entries) / max(len(entries), 1),
            "migrations": len(self._migration_history),
        }
