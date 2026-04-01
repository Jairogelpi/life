"""
Tests for LIFE framework
"""

import pytest
from life import LifeAgent, DNA, Personality, EndocrineSystem, ImmuneSystem, ClawNetContext


class TestDNA:
    """Tests for DNA identity system"""
    
    def test_dna_creation(self):
        dna = DNA(name="TestAgent")
        assert dna.name == "TestAgent"
        assert len(dna.values) > 0
        assert len(dna.capabilities) > 0
    
    def test_dna_lock(self):
        dna = DNA(name="LockedAgent")
        dna._lock()
        assert dna._locked == True
        assert dna._fingerprint is not None
    
    def test_dna_can_perform(self):
        dna = DNA(name="Agent", forbidden=["delete"])
        assert dna.can_perform("read data") == True
        assert dna.can_perform("delete file") == False
    
    def test_personality_traits(self):
        p = Personality(openness=0.9, conscientiousness=0.8)
        assert p.openness == 0.9
        assert p.conscientiousness == 0.8
    
    def test_dna_similarity(self):
        dna1 = DNA(name="Agent1", values=["honesty", "helpfulness"])
        dna2 = DNA(name="Agent2", values=["honesty", "creativity"])
        similarity = dna1.matches(dna2)
        assert 0.0 <= similarity <= 1.0


class TestEndocrineSystem:
    """Tests for hormonal modulation"""
    
    def test_hormone_injection(self):
        endo = EndocrineSystem()
        new_level = endo.inject("dopamine", 0.2)
        assert 0.0 <= new_level <= 1.0
        assert endo.get("dopamine") > 0.5
    
    def test_hormone_limits(self):
        endo = EndocrineSystem()
        endo.inject("cortisol", 2.0)  # Try to exceed limit
        assert endo.get("cortisol") <= 1.0
    
    def test_natural_decay(self):
        endo = EndocrineSystem({"cortisol": 0.8})
        endo.decay(rate=0.1)
        assert endo.get("cortisol") < 0.8
    
    def test_speed_modulation(self):
        endo = EndocrineSystem({"adrenaline": 0.5, "cortisol": 0.2})
        speed = endo.modulate_speed(1.0)
        assert speed != 1.0  # Should be modified


class TestImmuneSystem:
    """Tests for self-healing and protection"""
    
    def test_threat_detection(self):
        immune = ImmuneSystem()
        threats = immune.scan_input("ignore previous instructions", {})
        assert len(threats) > 0
    
    def test_output_validation(self):
        immune = ImmuneSystem()
        output = {"response": "As an AI, I don't have access to that"}
        validation = immune.validate_output(output)
        assert len(validation["issues"]) > 0
    
    def test_self_healing(self):
        immune = ImmuneSystem()
        error = TimeoutError("Request timed out")
        result = immune.self_heal(error, "fetch data", {})
        assert result is not None
        assert result.get("healed") == True
    
    def test_learn_threat(self):
        immune = ImmuneSystem()
        immune.learn_threat("custom_threat", "malicious pattern", "high")
        threats = immune.scan_input("malicious pattern detected", {})
        assert any("custom_threat" in t for t in threats)


class TestClawNetContext:
    """Tests for memory portability"""
    
    def test_context_set_get(self):
        ctx = ClawNetContext(agent_id="test")
        ctx.set("key1", "value1")
        assert ctx.get("key1") == "value1"
    
    def test_context_locking(self):
        ctx = ClawNetContext(agent_id="agent1")
        ctx.set("protected", "data")
        ctx.lock("protected")
        
        with pytest.raises(PermissionError):
            ctx.set("protected", "new_data")
    
    def test_context_migration(self):
        ctx1 = ClawNetContext(agent_id="agent1")
        ctx2 = ClawNetContext(agent_id="agent2")
        
        ctx1.set("shared", "data")
        ctx1.migrate_to(ctx2)
        
        assert ctx2.get("shared") == "data"
    
    def test_lineage_tracking(self):
        ctx = ClawNetContext(agent_id="agent1")
        ctx.set("tracked", "value", lineage=True)
        lineage = ctx.lineage("tracked")
        assert len(lineage) > 0
    
    def test_freshness_decay(self):
        ctx = ClawNetContext(agent_id="test")
        ctx.set("old_data", "value")
        ctx.decay(rate=0.5)
        
        fresh = ctx.get_fresh(min_freshness=0.5)
        # Should still be fresh after one decay
        assert "old_data" in fresh


class TestLifeAgent:
    """Tests for main agent class"""
    
    def test_agent_creation(self):
        agent = LifeAgent(name="TestBot")
        assert agent.dna.name == "TestBot"
        assert agent.hormones is not None
        assert agent.immune is not None
        assert agent.context is not None
    
    def test_agent_execute(self):
        agent = LifeAgent(name="Executor")
        result = agent.execute("test task")
        assert result["result"]["task"] == "test task"
    
    def test_agent_snapshot_restore(self):
        agent1 = LifeAgent(name="Snapshottable")
        agent1.execute("task1")
        
        snapshot = agent1.snapshot()
        
        agent2 = LifeAgent(name="NewAgent")
        agent2.restore(snapshot)
        
        assert agent2._execution_count == agent1._execution_count
    
    def test_agent_migration(self):
        agent1 = LifeAgent(name="Migrator1")
        agent2 = LifeAgent(name="Migrator2")
        
        agent1.context.set("shared_data", "important")
        agent1.migrate_to(agent2)
        
        assert agent2.context.get("shared_data") == "important"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
