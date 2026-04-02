"""
LIFE Vibe Example — Emotional Communication Between Agents

This demonstrates the REVOLUTIONARY feature:
Agents communicate EMOTIONALLY, not just logically.

Like agents are "for AI", LIFE Vibe is "for agents".
"""

from life import LifeAgent, Vibe, VibeProtocol


def example_emotional_collaboration():
    """
    Two agents collaborate with emotional awareness.
    
    AgentA is stressed and needs help.
    AgentB senses the stress and responds empathicallyallly.
    """
    
    print("=" * 60)
    print("LIFE Vibe — Emotional Agent Communication")
    print("=" * 60)
    
    # Create agents
    worker = LifeAgent(name="Worker")
    helper = LifeAgent(name="Helper")
    
    # Worker is stressed
    print("\n📊 Worker starts stressed:")
    worker.hormones.inject("cortisol", 0.4)
    worker.hormones.inject("adrenaline", 0.3)
    worker.state.energy = 0.6
    print(f"  Cortisol: {worker.hormones.get('cortisol'):.2f}")
    print(f"  Adrenaline: {worker.hormones.get('adrenaline'):.2f}")
    print(f"  Energy: {worker.state.energy:.2f}")
    
    # Worker emits vibe
    print("\n📡 Worker emits vibe to Helper:")
    worker_vibe_proto = VibeProtocol(worker)
    worker_vibe = worker_vibe_proto.emit_vibe(
        "Helper",
        message="I need help with this urgent task"
    )
    print(f"  Vibe: {worker_vibe.to_signal()}")
    print(f"  Interpretation: energy={worker_vibe.energy:.1f}, mood={worker_vibe.mood:.1f}, urgency={worker_vibe.urgency:.1f}")
    
    # Helper receives and reacts
    print("\n🧠 Helper receives vibe and responds emotionally:")
    helper_vibe_proto = VibeProtocol(helper)
    response_vibe = helper_vibe_proto.receive_vibe(
        "Worker",
        worker_vibe,
        message="I need help"
    )
    print(f"  Helper's response vibe: {response_vibe.to_signal()}")
    print(f"  Helper's new hormones:")
    print(f"    Adrenaline: {helper.hormones.get('adrenaline'):.2f} (sensed urgency)")
    print(f"    Oxytocin: {helper.hormones.get('oxytocin'):.2f} (trust increased)")
    
    # Calculate resonance
    resonance = worker_vibe.resonance_with(response_vibe)
    print(f"\n💕 Resonance between agents: {resonance:.2f}")
    print(f"  {'Good communication!' if resonance > 0.6 else 'Some friction'}")
    
    # Get emotional context
    print("\n📈 Helper's emotional context:")
    context = helper_vibe_proto.get_emotional_context()
    print(f"  Current vibe: {context['current']}")
    print(f"  Resonance with incoming: {context['resonance_with_incoming']:.2f}")
    
    print("\n" + "=" * 60)
    print("This is REVOLUTIONARY:")
    print("Agents don't just exchange data.")
    print("They exchange EMOTIONAL STATES.")
    print("=" * 60)
    
    return worker, helper


def example_multi_agent_empathy():
    """
    Multiple agents form an emotional network.
    """
    
    print("\n" + "=" * 60)
    print("Multi-Agent Emotional Network")
    print("=" * 60)
    
    # Create team
    leader = LifeAgent(name="Leader")
    dev1 = LifeAgent(name="Dev1")
    dev2 = LifeAgent(name="Dev2")
    
    # Leader is confident and energetic
    leader.hormones.inject("dopamine", 0.3)
    leader.hormones.inject("serotonin", 0.2)
    leader.state.energy = 0.9
    
    # Dev1 is stressed
    dev1.hormones.inject("cortisol", 0.5)
    dev1.state.energy = 0.5
    
    # Dev2 is neutral
    dev2.state.energy = 0.7
    
    # Leader broadcasts vibe
    print("\n📡 Leader broadcasts to team:")
    leader_proto = VibeProtocol(leader)
    leader_vibe = leader_proto.emit_vibe("Team", message="Let's ship this!")
    print(f"  Leader vibe: {leader_vibe.to_signal()}")
    print(f"  Interpretation: High energy, positive mood, confident")
    
    # Team receives
    print("\n👥 Team receives leader's vibe:")
    
    dev1_proto = VibeProtocol(dev1)
    dev1_response = dev1_proto.receive_vibe("Leader", leader_vibe)
    print(f"  Dev1 response: {dev1_response.to_signal()}")
    print(f"    Stress reduced: cortisol={dev1.hormones.get('cortisol'):.2f}")
    
    dev2_proto = VibeProtocol(dev2)
    dev2_response = dev2_proto.receive_vibe("Leader", leader_vibe)
    print(f"  Dev2 response: {dev2_response.to_signal()}")
    print(f"    Energy boosted: energy={dev2.state.energy:.2f}")
    
    # Team emotional context
    print("\n📊 Team emotional states:")
    for agent, proto in [(leader, leader_proto), (dev1, dev1_proto), (dev2, dev2_proto)]:
        context = proto.get_emotional_context()
        vibe = Vibe.from_signal(context["current"])
        print(f"  {agent.dna.name}: mood={vibe.mood:+.1f}, energy={vibe.energy:.1f}, trust={vibe.trust:.1f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    example_emotional_collaboration()
    example_multi_agent_empathy()
