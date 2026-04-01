#!/usr/bin/env python3
"""
LIFE Quick Start Script
Run this to verify LIFE is working correctly
"""

import sys


def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required = ["pydantic", "numpy"]
    missing = []
    
    for dep in required:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} (missing)")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("   Run: pip install " + " ".join(missing))
        return False
    
    return True


def test_imports():
    """Test that all LIFE modules can be imported"""
    print("\n🔍 Testing imports...")
    
    try:
        from life import LifeAgent, DNA, Personality
        print("  ✅ LifeAgent")
        print("  ✅ DNA")
        print("  ✅ Personality")
        
        from life import EndocrineSystem, ImmuneSystem
        print("  ✅ EndocrineSystem")
        print("  ✅ ImmuneSystem")
        
        from life import NervousSystem, Homeostasis
        print("  ✅ NervousSystem")
        print("  ✅ Homeostasis")
        
        from life import ClawNetContext
        print("  ✅ ClawNetContext")
        
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_basic_functionality():
    """Test basic LIFE functionality"""
    print("\n🧪 Testing basic functionality...")
    
    from life import LifeAgent, DNA, Personality
    
    # Create agent
    print("  Creating agent...")
    agent = LifeAgent(
        name="TestBot",
        dna=DNA(
            name="TestBot",
            personality=Personality(openness=0.8, conscientiousness=0.9),
            values=["test"],
            capabilities=["test"],
        ),
    )
    print("  ✅ Agent created")
    
    # Execute task
    print("  Executing task...")
    result = agent.execute("test task")
    print(f"  ✅ Task executed: {result['result']['task']}")
    
    # Check state
    print(f"  ✅ Energy: {agent.state.energy:.2f}")
    print(f"  ✅ Accuracy: {agent.state.accuracy:.2f}")
    
    # Test hormones
    agent.hormones.inject("dopamine", 0.1)
    print(f"  ✅ Dopamine: {agent.hormones.get('dopamine'):.2f}")
    
    # Test context
    agent.context.set("test_key", "test_value")
    val = agent.context.get("test_key")
    print(f"  ✅ Context: {val}")
    
    return True


def run_quick_start():
    """Run all checks and tests"""
    print("=" * 60)
    print("LIFE Framework - Quick Start")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Test functionality
    if not test_basic_functionality():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! LIFE is ready to use.")
    print("=" * 60)
    print("\nNext steps:")
    print("  from life import LifeAgent")
    print("  agent = LifeAgent(name='MyAgent')")
    print("  result = agent.execute('my task')")
    print()


if __name__ == "__main__":
    run_quick_start()
