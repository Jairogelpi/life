"""
LifeAgent — The main agent class combining ORGANISM + ClawNet
"""

from typing import Any, Optional, Dict, List
from pydantic import BaseModel, Field

from life.dna import DNA
from life.hormones import EndocrineSystem
from life.immune import ImmuneSystem
from life.nervous import NervousSystem
from life.homeostasis import Homeostasis
from life.context import ClawNetContext
from life.observation import ObservationSystem


class AgentState(BaseModel):
    """Current state of the agent"""
    energy: float = Field(default=0.8, ge=0.0, le=1.0)
    accuracy: float = Field(default=0.5, ge=0.0, le=1.0)
    stress: float = Field(default=0.1, ge=0.0, le=1.0)
    coherence: float = Field(default=0.9, ge=0.0, le=1.0)


class LifeAgent:
    """
    Living Agent with biological architecture + memory portability.
    
    This is the main class that combines:
    - DNA: Immutable identity
    - Endocrine System: Hormonal modulation
    - Immune System: Self-healing and protection
    - Nervous System: Signal routing and enforcement
    - Homeostasis: Self-regulation
    - ClawNet Context: Memory portability
    """
    
    def __init__(
        self,
        dna: Optional[DNA] = None,
        hormones: Optional[Dict[str, float]] = None,
        context: Optional[ClawNetContext] = None,
        name: Optional[str] = None,
    ):
        # DNA: Identity (immutable once set)
        self.dna = dna or DNA(name=name or "Agent")
        self.dna._lock()
        
        # Biological systems
        self.hormones = EndocrineSystem(initial=hormones)
        self.immune = ImmuneSystem(dna=self.dna)
        self.nervous = NervousSystem(agent=self)
        self.homeostasis = Homeostasis(agent=self)
        
        # Memory portability
        self.context = context or ClawNetContext(agent_id=self.dna.id)
        
        # Observation system (solves gap #1)
        self.observation = ObservationSystem(agent_id=self.dna.id)
        
        # Vibe Protocol (emotional communication)
        from life.vibe import VibeProtocol
        self.vibe_protocol = VibeProtocol(agent=self)
        
        # Genesis (self-evolution)
        from life.genesis import Genesis
        self.genesis = Genesis(agent=self)
        
        # State tracking
        self.state = AgentState()
        self._execution_count = 0
        self._error_count = 0
    
    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a task with full biological regulation.
        
        This method:
        1. Validates task against DNA capabilities
        2. Checks immune system for threats
        3. Regulates homeostasis
        4. Executes with enforcement layer
        5. Validates output
        6. Updates hormonal state
        """
        # Pre-execution validation
        if not self.dna.can_perform(task):
            raise ValueError(f"Task '{task}' not in DNA capabilities")
        
        # Nervous system enforcement
        self.nervous.validate_task(task, kwargs)
        
        # Homeostasis regulation before action
        self.homeostasis.regulate()
        
        # Check immune system
        threats = self.immune.scan_input(task, kwargs)
        if threats:
            self._error_count += 1
            self.hormones.inject("cortisol", 0.2)
            raise SecurityError(f"Threats detected: {threats}")
        
        # Execute with observation
        self.observation.start_trace(task)
        try:
            result = self._do_execute(task, **kwargs)
            
            # Post-execution validation
            validation = self.immune.validate_output(result)
            if not validation["valid"]:
                result = self.immune.auto_correct(result, validation["issues"])
            
            # Success: reward
            self.hormones.inject("dopamine", 0.1)
            self._execution_count += 1
            
            # Update state
            self.state.accuracy = self._calculate_accuracy()
            self.state.energy = max(0.1, self.state.energy - 0.02)
            
            # Record observation
            self.observation.end_trace(success=True, result=result)
            
            return {
                "result": result,
                "state": self.state.model_dump(),
                "hormones": self.hormones.levels(),
                "lineage": self.context.lineage(),
            }
            
        except Exception as e:
            # Error: stress response
            self.hormones.inject("cortisol", 0.3)
            self._error_count += 1
            self.state.stress = min(1.0, self.state.stress + 0.1)
            
            # Record failure
            self.observation.end_trace(success=False, error=str(e))
            
            # Attempt self-healing
            healed = self.immune.self_heal(e, task, kwargs)
            if healed:
                return healed
            
            raise
    
    def _do_execute(self, task: str, **kwargs) -> Any:
        """Internal execution - override in subclasses"""
        return {"task": task, "kwargs": kwargs, "status": "executed"}
    
    def _calculate_accuracy(self) -> float:
        """Calculate accuracy based on success rate"""
        total = self._execution_count + self._error_count
        if total == 0:
            return 0.5
        return self._execution_count / total
    
    def migrate_to(self, other_agent: "LifeAgent") -> None:
        """Migrate context to another agent (ClawNet portability)"""
        self.context.migrate_to(other_agent.context)
    
    @classmethod
    def from_dna(cls, dna: DNA, **kwargs) -> "LifeAgent":
        """Create agent from existing DNA"""
        return cls(dna=dna, **kwargs)
    
    def snapshot(self) -> Dict[str, Any]:
        """Create a complete snapshot of agent state"""
        return {
            "dna": self.dna.to_dict(),
            "hormones": self.hormones.levels(),
            "state": self.state.model_dump(),
            "context": self.context.export(),
            "immune_memory": self.immune.memory(),
            "execution_count": self._execution_count,
            "error_count": self._error_count,
        }
    
    def restore(self, snapshot: Dict[str, Any]) -> None:
        """Restore agent from snapshot"""
        # DNA is immutable, cannot restore
        self.hormones.set_levels(snapshot["hormones"])
        self.state = AgentState(**snapshot["state"])
        self.context.import_data(snapshot["context"])
        self.immune.restore_memory(snapshot["immune_memory"])
        self._execution_count = snapshot["execution_count"]
        self._error_count = snapshot["error_count"]


class SecurityError(Exception):
    """Raised when immune system detects a threat"""
    pass
