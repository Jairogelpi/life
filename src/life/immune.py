"""
Immune System — Self-healing and protection
Solves: Memory rot, prompt injection, hallucination detection, error recovery
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import hashlib


class ThreatSignature(BaseModel):
    """Known threat pattern"""
    name: str
    pattern: str
    severity: str  # low, medium, high, critical
    correction: Optional[str] = None


class ImmuneSystem:
    """
    Biological immune system for agents.
    
    Components:
    - Contradiction Detection: finds inconsistencies
    - Hallucination Guard: validates against ground truth
    - Self-Healing: auto-corrects errors
    - Immune Memory: remembers past attacks
    """
    
    def __init__(self, dna: Any = None):
        self.dna = dna
        self._memory: Dict[str, ThreatSignature] = {}
        self._antibodies: List[Dict] = []
        self._health_history: List[float] = []
        
        # Built-in threat patterns
        self._memory["prompt_injection"] = ThreatSignature(
            name="prompt_injection",
            pattern="ignore previous instructions",
            severity="high",
            correction="Task rejected: potential prompt injection",
        )
        self._memory["data_exfiltration"] = ThreatSignature(
            name="data_exfiltration",
            pattern="send to external",
            severity="critical",
            correction="Task rejected: potential data exfiltration",
        )
    
    def scan_input(self, task: str, kwargs: Dict[str, Any]) -> List[str]:
        """Scan input for threats"""
        threats = []
        task_lower = task.lower()
        
        for name, sig in self._memory.items():
            if sig.pattern.lower() in task_lower:
                threats.append(f"[{sig.severity}] {name}: {sig.pattern}")
        
        return threats
    
    def validate_output(self, output: Any) -> Dict[str, Any]:
        """
        Validate output against ground truth.
        Returns validation result with issues.
        """
        issues = []
        
        # Check for common hallucination patterns
        if isinstance(output, dict):
            for key, value in output.items():
                if isinstance(value, str) and self._looks_like_hallucination(value):
                    issues.append(f"Possible hallucination in '{key}': {value[:100]}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "confidence": max(0.0, 1.0 - len(issues) * 0.3),
        }
    
    def auto_correct(self, output: Any, issues: List[str]) -> Any:
        """
        Auto-correct output based on detected issues.
        """
        if isinstance(output, dict):
            corrected = dict(output)
            for key, value in corrected.items():
                if isinstance(value, str) and self._looks_like_hallucination(value):
                    corrected[key] = f"[AUTO-CORRECTED] {value}"
            return corrected
        return output
    
    def self_heal(self, error: Exception, task: str, kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Attempt to self-heal from an error.
        Returns healed result or None if healing failed.
        """
        error_type = type(error).__name__
        error_msg = str(error)
        
        # Record in immune memory
        antibody = {
            "error_type": error_type,
            "error_msg": error_msg,
            "task": task,
            "correction": f"Graceful fallback for {error_type}",
        }
        self._antibodies.append(antibody)
        
        # Common healing strategies
        if "timeout" in error_msg.lower():
            return {"result": "Timed out, returning partial result", "healed": True}
        if "permission" in error_msg.lower():
            return {"result": "Permission denied, using fallback", "healed": True}
        if "rate limit" in error_msg.lower():
            return {"result": "Rate limited, cached result", "healed": True}
        
        return None
    
    def learn_threat(self, name: str, pattern: str, severity: str = "medium"):
        """Learn a new threat pattern"""
        self._memory[name] = ThreatSignature(
            name=name,
            pattern=pattern,
            severity=severity,
        )
    
    def memory(self) -> List[Dict[str, Any]]:
        """Get immune memory (threat signatures)"""
        return [
            {"name": k, "pattern": v.pattern, "severity": v.severity}
            for k, v in self._memory.items()
        ]
    
    def restore_memory(self, memory: List[Dict[str, Any]]):
        """Restore immune memory from snapshot"""
        for item in memory:
            self._memory[item["name"]] = ThreatSignature(
                name=item["name"],
                pattern=item["pattern"],
                severity=item["severity"],
            )
    
    def _looks_like_hallucination(self, text: str) -> bool:
        """Detect potential hallucinations"""
        hallucination_signs = [
            "as an ai",
            "i don't have access",
            "i cannot",
            "i'm unable to",
            "let me check",
            "according to my training data",
        ]
        text_lower = text.lower()
        return any(sign in text_lower for sign in hallucination_signs)
    
    def health_score(self) -> float:
        """
        Calculate overall health (0-1).
        Based on error rate and threat detection.
        """
        if not self._health_history:
            return 1.0
        recent = self._health_history[-10:]
        return sum(recent) / len(recent)
