"""
LIFE Genesis Example — Agent Evolution, Reproduction & Collective Intelligence
"""

from life import LifeAgent, Genesis, DNA, Personality


def example_agent_reproduction():
    """Agent creates children with mutations"""
    
    print("=" * 60)
    print("🧬 LIFE Genesis — Agent Reproduction")
    print("=" * 60)
    
    # Create parent
    parent = LifeAgent(
        name="Founder",
        dna=DNA(
            name="Founder",
            personality=Personality(
                openness=0.7,
                conscientiousness=0.8,
            ),
            values=["honesty", "creativity"],
            capabilities=["reasoning", "communication"],
        ),
    )
    
    print(f"\n👤 Parent: {parent.dna.name}")
    print(f"  Values: {parent.dna.values}")
    print(f"  Capabilities: {parent.dna.capabilities}")
    
    # Reproduce with mutation
    child = parent.genesis.reproduce(
        mutations={
            "openness": 0.1,  # More open
            "add_capability": "research",
            "add_value": "thoroughness",
        },
        child_name="Researcher",
    )
    
    print(f"\n👶 Child: {child.dna.name}")
    print(f"  Values: {child.dna.values}")
    print(f"  Capabilities: {child.dna.capabilities}")
    print(f"  Generation: {parent.genesis.generation}")
    
    # Child reproduces
    grandchild = child.genesis.reproduce(
        mutations={"add_capability": "writing"},
        child_name="Writer",
    )
    
    print(f"\n👶 Grandchild: {grandchild.dna.name}")
    print(f"  Capabilities: {grandchild.dna.capabilities}")
    print(f"  Generation: {child.genesis.generation}")
    
    print(f"\n📊 Evolution stats: {parent.genesis.get_evolution_stats()}")
    
    return parent, child, grandchild


def example_agent_evolution():
    """Agent evolves its own DNA"""
    
    print("\n" + "=" * 60)
    print("🧬 LIFE Genesis — Agent Evolution")
    print("=" * 60)
    
    agent = LifeAgent(name="Evolving")
    
    print(f"\n🔧 Before evolution:")
    print(f"  Openness: {agent.dna.personality.openness:.2f}")
    print(f"  Cortisol: {agent.hormones.get('cortisol'):.2f}")
    
    # Evolve personality
    agent.genesis.evolve("personality", ("openness", 0.9))
    print(f"\n🔧 After evolving openness:")
    print(f"  Openness: {agent.dna.personality.openness:.2f}")
    
    # Evolve hormones
    agent.genesis.evolve("hormone", ("dopamine", 0.3))
    print(f"\n🔧 After injecting dopamine:")
    print(f"  Dopamine: {agent.hormones.get('dopamine'):.2f}")
    
    # Add new capability
    agent.genesis.evolve("add_capability", "creative_writing")
    print(f"\n🔧 After adding capability:")
    print(f"  Capabilities: {agent.dna.capabilities}")
    
    print(f"\n📊 Evolution events: {len(agent.genesis.evolution_history)}")
    
    return agent


def example_capability_discovery():
    """Agent discovers new capabilities"""
    
    print("\n" + "=" * 60)
    print("🧬 LIFE Genesis — Capability Discovery")
    print("=" * 60)
    
    agent = LifeAgent(name="Explorer")
    
    # Agent discovers it can analyze sentiment
    discovery1 = agent.genesis.discover(
        capability_name="sentiment_analysis",
        description="Can detect emotional tone in text",
        evidence=[
            "Executed task 'analyze this review' successfully",
            "Correctly identified positive/negative sentiment",
        ],
    )
    
    print(f"\n🔍 Discovery 1: {discovery1.name}")
    print(f"  Proven: {discovery1.proven}")
    print(f"  Evidence: {len(discovery1.evidence)}")
    
    # Agent discovers but can't prove
    discovery2 = agent.genesis.discover(
        capability_name="code_generation",
        description="Can write code",
        evidence=["Tried writing code once"],  # Not enough evidence
    )
    
    print(f"\n🔍 Discovery 2: {discovery2.name}")
    print(f"  Proven: {discovery2.proven}")
    
    print(f"\n📊 Stats: {agent.genesis.get_evolution_stats()}")
    
    return agent


def example_agent_society():
    """Agents form a society"""
    
    print("\n" + "=" * 60)
    print("🧬 LIFE Genesis — Agent Society")
    print("=" * 60)
    
    # Create team
    leader = LifeAgent(name="Leader", dna=DNA(name="Leader", values=["integrity", "vision"]))
    dev = LifeAgent(name="Dev", dna=DNA(name="Dev", values=["precision", "speed"]))
    researcher = LifeAgent(name="Researcher", dna=DNA(name="Researcher", values=["thoroughness"]))
    
    # Form society
    society = leader.genesis.form_society(
        society_name="BuildTeam",
        members=[leader, dev, researcher],
        governance="consensus",
    )
    
    print(f"\n🏛️ Society formed: {society['name']}")
    print(f"  Governance: {society['governance']}")
    print(f"  Members: {society['members']}")
    
    # Collective problem solving
    result = leader.genesis.collective_problem_solving(
        members=[leader, dev, researcher],
        problem="How to optimize API performance?",
        strategy="explore",
    )
    
    print(f"\n🧠 Collective solution:")
    print(f"  Strategy: {result['strategy']}")
    print(f"  Solutions explored: {result['solutions_count']}")
    
    return society, result


if __name__ == "__main__":
    example_agent_reproduction()
    example_agent_evolution()
    example_capability_discovery()
    example_agent_society()
    
    print("\n" + "=" * 60)
    print("This is REVOLUTIONARY:")
    print("Agents CREATE agents. Agents EVOLVE. Agents DISCOVER.")
    print("Agents form SOCIETIES with governance.")
    print("This is 'for agents what agents are for AI'.")
    print("=" * 60)
