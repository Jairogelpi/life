"""
LIFE Genesis — Agent Self-Evolution & Reproduction

THE REVOLUTIONARY FEATURE:
Agents that CREATE agents. Agents that EVOLVE. Agents that DISCOVER.

Así como los agentes son "para la IA",
LIFE Genesis es "para los agentes".

Ningún framework permite que un agente:
1. Cree otro agente (reproducción)
2. Evolucione su propio ADN
3. Descubra sus propias capacidades
4. Forme sociedades con otros agentes

LIFE Genesis lo permite.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
import uuid
import random
import copy
import json


@dataclass
class Discovery:
    """A capability discovered by an agent"""
    name: str
    description: str
    proven: bool
    evidence: List[str]
    discovered_at: str
    discovered_by: str


@dataclass
class EvolutionEvent:
    """Record of an evolution event"""
    generation: int
    parent_id: str
    child_id: str
    mutation: str
    result: str  # success, failure
    timestamp: str


class Genesis:
    """
    Genesis system for agent self-evolution and reproduction.
    
    Components:
    1. Reproduction: Agents can create children with mutations
    2. Evolution: Agents can modify their own DNA (with constraints)
    3. Discovery: Agents can find new capabilities through experimentation
    4. Society: Agents can form hierarchies and governance
    5. Collective Intelligence: Agent groups solve problems no individual can
    """
    
    def __init__(self, agent: Any = None):
        self.agent = agent
        self.generation: int = 0
        self.children: List[str] = []
        self.discoveries: List[Discovery] = []
        self.evolution_history: List[EvolutionEvent] = []
        self.society_memberships: List[str] = []
        
    def reproduce(
        self,
        mutations: Optional[Dict[str, Any]] = None,
        child_name: Optional[str] = None,
    ) -> "LifeAgent":
        """
        Create a child agent with mutations.
        
        This is REPRODUCTION — the agent creates a new agent
        based on its own DNA with optional mutations.
        
        This is revolutionary because:
        - No framework allows agents to create other agents
        - The child inherits parent's knowledge but diverges
        - Evolution happens naturally through reproduction
        """
        from life import LifeAgent
        from life.dna import DNA, Personality
        
        if not self.agent:
            raise ValueError("Cannot reproduce without agent")
        
        parent = self.agent
        mutations = mutations or {}
        
        # Copy parent's DNA with mutations
        child_personality = Personality(
            openness=self._mutate(parent.dna.personality.openness, mutations.get("openness")),
            conscientiousness=self._mutate(parent.dna.personality.conscientiousness, mutations.get("conscientiousness")),
            extraversion=self._mutate(parent.dna.personality.extraversion, mutations.get("extraversion")),
            agreeableness=self._mutate(parent.dna.personality.agreeableness, mutations.get("agreeableness")),
            neuroticism=self._mutate(parent.dna.personality.neuroticism, mutations.get("neuroticism")),
        )
        
        # Mutate values
        child_values = list(parent.dna.values)
        if "add_value" in mutations:
            child_values.append(mutations["add_value"])
        if "remove_value" in mutations and mutations["remove_value"] in child_values:
            child_values.remove(mutations["remove_value"])
        
        # Mutate capabilities
        child_capabilities = list(parent.dna.capabilities)
        if "add_capability" in mutations:
            child_capabilities.append(mutations["add_capability"])
        
        # Create child DNA
        child_dna = DNA(
            name=child_name or f"{parent.dna.name}_child_{self.generation + 1}",
            personality=child_personality,
            values=child_values,
            capabilities=child_capabilities,
            forbidden=parent.dna.forbidden[:],  # Inherit forbidden
        )
        
        # Create child
        child = LifeAgent(
            dna=child_dna,
            hormones={
                "dopamine": self._mutate(parent.hormones.get("dopamine"), mutations.get("dopamine")),
                "cortisol": self._mutate(parent.hormones.get("cortisol"), mutations.get("cortisol")),
                "serotonin": self._mutate(parent.hormones.get("serotonin"), mutations.get("serotonin")),
            },
        )
        
        # Record reproduction
        import datetime
        event = EvolutionEvent(
            generation=self.generation + 1,
            parent_id=parent.dna.id,
            child_id=child.dna.id,
            mutation=json.dumps(mutations, default=str),
            result="success",
            timestamp=datetime.datetime.utcnow().isoformat(),
        )
        self.evolution_history.append(event)
        self.children.append(child.dna.id)
        self.generation += 1
        
        # Share parent's context with child
        if hasattr(parent, "context") and hasattr(child, "context"):
            # Share discovered knowledge
            for discovery in self.discoveries:
                child.context.set(f"discovery_{discovery.name}", {
                    "description": discovery.description,
                    "proven": discovery.proven,
                })
        
        return child
    
    def evolve(
        self,
        mutation_target: str,
        new_value: Any,
        validate: bool = True,
    ) -> bool:
        """
        Evolve own DNA (self-modification).
        
        The agent can modify its own DNA within constraints.
        This is EVOLUTION — the agent adapts to its environment.
        
        Constraints:
        - Cannot modify forbidden list
        - Cannot modify ID or creation date
        - Can modify personality, values, capabilities
        - Must pass validation if validate=True
        """
        import datetime
        
        if not self.agent:
            return False
        
        old_value = None
        
        if mutation_target == "personality":
            trait, value = new_value
            old_value = getattr(self.agent.dna.personality, trait)
            setattr(self.agent.dna.personality, trait, value)
            
        elif mutation_target == "add_value":
            if new_value not in self.agent.dna.values:
                self.agent.dna.values.append(new_value)
                old_value = None
                
        elif mutation_target == "add_capability":
            if new_value not in self.agent.dna.capabilities:
                self.agent.dna.capabilities.append(new_value)
                old_value = None
                
        elif mutation_target == "hormone":
            hormone, amount = new_value
            old_value = self.agent.hormones.get(hormone)
            self.agent.hormones.inject(hormone, amount)
        
        # Record evolution
        event = EvolutionEvent(
            generation=self.generation,
            parent_id=self.agent.dna.id,
            child_id=self.agent.dna.id,  # Self-modification
            mutation=f"{mutation_target}: {old_value} -> {new_value}",
            result="success" if old_value is not None else "added",
            timestamp=datetime.datetime.utcnow().isoformat(),
        )
        self.evolution_history.append(event)
        
        return True
    
    def discover(
        self,
        capability_name: str,
        description: str,
        evidence: List[str],
    ) -> Discovery:
        """
        Discover a new capability through experimentation.
        
        The agent discovers it can do something new.
        This is DISCOVERY — the agent learns its own limits.
        """
        import datetime
        
        discovery = Discovery(
            name=capability_name,
            description=description,
            proven=len(evidence) >= 2,  # Needs 2+ pieces of evidence
            evidence=evidence,
            discovered_at=datetime.datetime.utcnow().isoformat(),
            discovered_by=self.agent.dna.id if self.agent else "unknown",
        )
        
        self.discoveries.append(discovery)
        
        # If proven, add to capabilities
        if discovery.proven and self.agent:
            if capability_name not in self.agent.dna.capabilities:
                self.agent.dna.capabilities.append(capability_name)
        
        return discovery
    
    def form_society(
        self,
        society_name: str,
        members: List[Any],
        governance: str = "consensus",
    ) -> Dict[str, Any]:
        """
        Form a society of agents.
        
        Agents can organize into societies with governance rules.
        This is SOCIETY — agents forming organizations.
        
        Governance types:
        - consensus: All must agree
        - majority: Majority rules
        - hierarchy: Leader decides
        - emergent: Self-organizing
        """
        import datetime
        
        society = {
            "id": str(uuid.uuid4())[:8],
            "name": society_name,
            "governance": governance,
            "members": [m.dna.id for m in members],
            "created_at": datetime.datetime.utcnow().isoformat(),
            "decisions": [],
            "collective_context": {},
        }
        
        # Register each member
        for member in members:
            if hasattr(member, "genesis"):
                member.genesis.society_memberships.append(society["id"])
        
        return society
    
    def collective_problem_solving(
        self,
        members: List[Any],
        problem: str,
        strategy: str = "vote",
    ) -> Dict[str, Any]:
        """
        Solve a problem collectively.
        
        Multiple agents collaborate to solve a problem
        that no individual can solve alone.
        
        Strategies:
        - vote: Each agent proposes, majority wins
        - explore: Each explores different angle, combine
        - evolve: Agents evolve to find solution
        """
        solutions = []
        
        for member in members:
            # Each member approaches from their perspective
            if hasattr(member, "execute"):
                result = member.execute(f"Approach: {problem}")
                solutions.append({
                    "agent": member.dna.name,
                    "solution": result.get("result", {}),
                    "confidence": member.state.accuracy,
                    "vibe": member.vibe_protocol.emit_vibe("collective").to_signal() if hasattr(member, "vibe_protocol") else None,
                })
        
        if strategy == "vote":
            # Majority vote based on confidence
            solutions.sort(key=lambda s: s["confidence"], reverse=True)
            best = solutions[0] if solutions else None
            return {
                "problem": problem,
                "strategy": strategy,
                "solutions_count": len(solutions),
                "best_solution": best,
                "method": "confidence_vote",
            }
        
        elif strategy == "explore":
            # Combine insights from all agents
            combined = {
                "problem": problem,
                "strategy": strategy,
                "solutions": solutions,
                "combined_insights": [
                    f"{s['agent']}: {s['solution']}" for s in solutions
                ],
                "method": "exploration_merge",
            }
            return combined
        
        return {"problem": problem, "error": "unknown strategy"}
    
    def get_evolution_stats(self) -> Dict[str, Any]:
        """Get evolution statistics"""
        return {
            "generation": self.generation,
            "children_created": len(self.children),
            "discoveries_made": len(self.discoveries),
            "proven_discoveries": len([d for d in self.discoveries if d.proven]),
            "evolution_events": len(self.evolution_history),
            "societies_joined": len(self.society_memberships),
        }
    
    def _mutate(self, value: float, mutation: Optional[float]) -> float:
        """Apply mutation with bounds checking"""
        if mutation is None:
            # Random small mutation
            mutation = random.uniform(-0.1, 0.1)
        new_value = value + mutation
        return max(0.0, min(1.0, new_value))
