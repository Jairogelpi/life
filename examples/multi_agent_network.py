"""
LIFE + ClawNet Multi-Agent Network
Example of multiple LIFE agents collaborating
"""

from typing import List, Dict, Any
from life import LifeAgent, DNA, ClawNetContext


class AgentNetwork:
    """
    Network of LIFE agents that share context.
    
    This demonstrates the ClawNet portability layer:
    - Agents can share context
    - Context is lineage-tracked
    - Freshness prevents semantic drift
    """
    
    def __init__(self, name: str = "Network"):
        self.name = name
        self.agents: List[LifeAgent] = []
        self.shared_context = ClawNetContext(agent_id=f"network_{name}")
    
    def add_agent(self, agent: LifeAgent):
        """Add agent to network"""
        self.agents.append(agent)
        # Sync shared context to agent
        self.shared_context.migrate_to(agent.context)
    
    def broadcast(self, key: str, value: Any):
        """Broadcast value to all agents"""
        self.shared_context.set(key, value)
        for agent in self.agents:
            agent.context.set(key, value, lineage=True)
    
    def get_consensus(self, key: str) -> Any:
        """Get consensus value from all agents"""
        values = []
        for agent in self.agents:
            val = agent.context.get(key)
            if val is not None:
                values.append({
                    "value": val,
                    "freshness": agent.context._entries.get(key, ClawNetContext("")._entries.get("dummy", None)).freshness if key in agent.context._entries else 0.0,
                })
        
        if not values:
            return None
        
        # Prefer freshest value
        values.sort(key=lambda x: x["freshness"], reverse=True)
        return values[0]["value"]
    
    def execute_parallel(self, task: str) -> List[Dict]:
        """Execute task across all agents in parallel"""
        results = []
        for agent in self.agents:
            result = agent.execute(task)
            results.append({
                "agent": agent.dna.name,
                "result": result,
                "state": agent.state.model_dump(),
            })
        return results


def example_multi_agent_network():
    """Example of LIFE agent network"""
    
    # Create network
    network = AgentNetwork(name="ResearchNetwork")
    
    # Add specialized agents
    researcher = LifeAgent(
        name="Researcher",
        dna=DNA(
            name="Researcher",
            values=["thoroughness", "accuracy"],
            capabilities=["search", "analysis"],
        ),
    )
    
    writer = LifeAgent(
        name="Writer",
        dna=DNA(
            name="Writer",
            values=["clarity", "engagement"],
            capabilities=["writing", "editing"],
        ),
    )
    
    reviewer = LifeAgent(
        name="Reviewer",
        dna=DNA(
            name="Reviewer",
            values=["quality", "completeness"],
            capabilities=["review", "feedback"],
        ),
    )
    
    network.add_agent(researcher)
    network.add_agent(writer)
    network.add_agent(reviewer)
    
    # Broadcast shared context
    network.broadcast("project", "LIFE Framework Paper")
    network.broadcast("deadline", "2026-04-15")
    
    # Execute parallel
    results = network.execute_parallel("Analyze requirements")
    
    print("Network results:")
    for r in results:
        print(f"  {r['agent']}: {r['state']['energy']:.2f} energy")
    
    # Get consensus
    project = network.get_consensus("project")
    print(f"Consensus project: {project}")
    
    return network


if __name__ == "__main__":
    example_multi_agent_network()
