"""
Nervous System — Signal routing and enforcement layer
Solves: Tool call enforcement, cross-module communication, reflex arcs
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Signal:
    """A signal passing through the nervous system"""
    source: str
    destination: str
    signal_type: str  # task, alert, request, response
    payload: Any
    priority: int = 0  # 0=normal, 1=high, 2=critical


@dataclass
class ReflexArc:
    """An automatic response to a specific condition"""
    condition: str  # e.g., "high_cortisol", "threat_detected"
    handler: Callable
    priority: int = 0


class NervousSystem:
    """
    Central nervous system for agent.
    
    Components:
    - Signal Router: routes messages between systems
    - Enforcement Layer: validates tool calls before execution
    - Reflex Arcs: automatic responses to stimuli
    """
    
    def __init__(self, agent: Any = None):
        self.agent = agent
        self._signals: List[Signal] = []
        self._reflexes: Dict[str, ReflexArc] = {}
        self._tool_validators: Dict[str, Callable] = {}
    
    def register_reflex(self, condition: str, handler: Callable, priority: int = 0):
        """Register a reflex arc for automatic response"""
        self._reflexes[condition] = ReflexArc(
            condition=condition,
            handler=handler,
            priority=priority,
        )
    
    def register_tool_validator(self, tool_name: str, validator: Callable):
        """
        Register a validator for a tool.
        Validator must return (valid: bool, reason: str)
        """
        self._tool_validators[tool_name] = validator
    
    def validate_task(self, task: str, kwargs: Dict[str, Any]) -> None:
        """
        Validate task before execution.
        Raises ValueError if task is invalid.
        """
        # Check DNA capabilities
        if self.agent and hasattr(self.agent, "dna"):
            if not self.agent.dna.can_perform(task):
                raise ValueError(f"Task violates DNA constraints: {task}")
    
    def validate_tool_call(self, tool_name: str, args: Dict[str, Any]) -> None:
        """
        Validate tool call before execution.
        This is the ENFORCEMENT LAYER that no framework has.
        Raises ValueError if tool call is invalid.
        """
        if tool_name in self._tool_validators:
            validator = self._tool_validators[tool_name]
            valid, reason = validator(args)
            if not valid:
                raise ValueError(f"Tool call '{tool_name}' invalid: {reason}")
    
    def route(self, signal: Signal) -> Optional[Any]:
        """Route a signal to its destination"""
        self._signals.append(signal)
        
        # Check reflex arcs
        for reflex in sorted(self._reflexes.values(), key=lambda r: r.priority, reverse=True):
            if reflex.condition == signal.signal_type:
                return reflex.handler(self.agent, signal)
        
        return None
    
    def send_alert(self, source: str, message: str, severity: str = "info"):
        """Send alert signal"""
        signal = Signal(
            source=source,
            destination="observation",
            signal_type="alert",
            payload={"message": message, "severity": severity},
            priority=2 if severity == "critical" else 1 if severity == "high" else 0,
        )
        return self.route(signal)
    
    def stats(self) -> Dict[str, Any]:
        """Get nervous system statistics"""
        return {
            "signals_processed": len(self._signals),
            "reflexes_registered": len(self._reflexes),
            "tool_validators": len(self._tool_validators),
        }
