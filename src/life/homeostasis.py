"""
Homeostasis — Self-regulation via differential equations
Solves: Agent stability, automatic regulation, long-running session degradation
"""

from typing import Dict, Any, Optional
import math


class Homeostasis:
    """
    Biological homeostasis control system.
    
    Uses differential equation: dS/dt = α(I-S) - β(S-St) + γ(E)
    Where:
    - S = current state
    - I = input stimulus
    - St = target set point
    - E = external perturbation
    - α, β, γ = regulation coefficients
    
    This makes agents SELF-REGULATING:
    - Energy returns to optimal after exertion
    - Stress decreases over time
    - Accuracy improves with experience
    """
    
    def __init__(self, agent: Any = None, alpha: float = 0.1, beta: float = 0.05, gamma: float = 0.02):
        self.agent = agent
        self.alpha = alpha  # response to input
        self.beta = beta    # return to target
        self.gamma = gamma  # perturbation sensitivity
        
        # Target set points (optimal values)
        self._targets: Dict[str, float] = {
            "energy": 0.8,
            "accuracy": 0.9,
            "stress": 0.1,
            "coherence": 0.9,
        }
        
        # Current state
        self._state: Dict[str, float] = dict(self._targets)
        
        # History for trend analysis
        self._history: list = []
    
    def set_target(self, variable: str, target: float):
        """Set target value for a variable"""
        self._targets[variable] = max(0.0, min(1.0, target))
    
    def get_target(self, variable: str) -> float:
        """Get target value"""
        return self._targets.get(variable, 0.5)
    
    def get_state(self, variable: str) -> float:
        """Get current state"""
        return self._state.get(variable, 0.5)
    
    def regulate(self) -> Dict[str, float]:
        """
        Run one regulation step.
        Applies differential equation to all variables.
        Returns new state.
        """
        new_state = {}
        
        for variable, target in self._targets.items():
            current = self._state.get(variable, target)
            
            # Get input from agent state
            input_val = self._get_input(variable)
            
            # External perturbation
            perturbation = self._get_perturbation(variable)
            
            # Apply differential equation
            # dS/dt = α(I-S) - β(S-St) + γ(E)
            ds = (
                self.alpha * (input_val - current)
                - self.beta * (current - target)
                + self.gamma * perturbation
            )
            
            new_state[variable] = max(0.0, min(1.0, current + ds))
        
        self._state = new_state
        self._history.append(new_state)
        
        # Update agent state if available
        if self.agent and hasattr(self.agent, "state"):
            for key, value in new_state.items():
                if hasattr(self.agent.state, key):
                    setattr(self.agent.state, key, value)
        
        return new_state
    
    def _get_input(self, variable: str) -> float:
        """Get input stimulus from agent"""
        if not self.agent:
            return 0.5
        
        if variable == "energy":
            return 1.0 - (self.agent._error_count / max(self.agent._execution_count, 1)) * 0.5
        elif variable == "accuracy":
            return self.agent._calculate_accuracy()
        elif variable == "stress":
            return self.agent.hormones.get("cortisol")
        elif variable == "coherence":
            return self.agent.state.coherence if hasattr(self.agent, "state") else 0.9
        return 0.5
    
    def _get_perturbation(self, variable: str) -> float:
        """Get external perturbation"""
        if not self.agent:
            return 0.0
        
        if variable == "energy":
            return -self.agent.hormones.get("cortisol") * 0.1
        elif variable == "stress":
            return self.agent.hormones.get("adrenaline") * 0.2
        return 0.0
    
    def trajectory(self, steps: int = 10) -> list:
        """Predict future state trajectory"""
        state = dict(self._state)
        trajectory = [dict(state)]
        
        for _ in range(steps):
            new_state = {}
            for variable, target in self._targets.items():
                current = state[variable]
                input_val = 0.5
                perturbation = 0.0
                ds = (
                    self.alpha * (input_val - current)
                    - self.beta * (current - target)
                    + self.gamma * perturbation
                )
                new_state[variable] = max(0.0, min(1.0, current + ds))
            state = new_state
            trajectory.append(dict(state))
        
        return trajectory
    
    def is_stable(self) -> bool:
        """Check if system is stable"""
        if len(self._history) < 3:
            return True
        
        recent = self._history[-3:]
        for variable in self._targets:
            values = [h.get(variable, 0.5) for h in recent]
            variance = max(values) - min(values)
            if variance > 0.1:
                return False
        return True
    
    def snapshot(self) -> Dict[str, Any]:
        """Snapshot homeostasis state"""
        return {
            "targets": dict(self._targets),
            "state": dict(self._state),
            "stable": self.is_stable(),
        }
