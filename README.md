# LIFE — Living Infrastructure for Agents

> **El framework que resuelve los 10 gaps que NINGÚN otro ha resuelto.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Instalación

```bash
pip install life-agents
```

## 🧬 ¿Qué es LIFE?

LIFE combina **ClawNet** (Context Consistency Protocol) + **ORGANISM** (Biological Agent Architecture) en un sistema unificado que hace que los agentes sean:

- **Portables** — pueden moverse entre frameworks sin perder contexto
- **Estables** — se autorregulan con homeostasis biológica
- **Emocionales** — se comunican con vibes, no solo datos
- **Evolucionivos** — crean hijos, evolucionan, descubren
- **Sociales** — forman sociedades con governance

## 📊 Los 10 GAPS que LIFE resuelve

| # | Gap | Solución LIFE |
|---|-----|---------------|
| 1 | Observability multi-agent | **Observation System** — traces cross-framework |
| 2 | Memory rot | **Homeostasis** — self-regulation via dS/dt |
| 3 | Evaluación confiable | **DNA Validator** — validación automática |
| 4 | Coordinación multi-agent | **Endocrine System** — hormonal modulation |
| 5 | Pilot-to-production | **Immune System** — self-healing automático |
| 6 | Enforcement layer | **Nervous System** — pre-validate tool calls |
| 7 | Coste impredecible | **Metabolic Rate** — budget tracking |
| 8 | Semantic drift | **Freshness Scoring** — temporal decay |
| 9 | Seguridad en cascada | **Immune Memory** — threat resistance |
| 10 | Interoperabilidad | **ClawNet** — context portability |

## 🔧 Quick Start

```python
from life import LifeAgent, DNA, Personality

# Crear agente con ADN
agent = LifeAgent(
    name="HelperBot",
    dna=DNA(
        name="HelperBot",
        personality=Personality(openness=0.8, conscientiousness=0.9),
        values=["helpfulness", "honesty"],
        capabilities=["research", "communication"],
    ),
)

# Ejecutar con regulación biológica completa
result = agent.execute("Analyze this data")

print(f"Energy: {agent.state.energy:.2f}")
print(f"Hormones: {agent.hormones.levels()}")
```

## 🧠 Los 8 Componentes

### 1. DNA (Identity Layer)
Identidad inmutable con Big Five personality.

```python
dna = DNA(
    personality=Personality(openness=0.8, conscientiousness=0.9),
    values=["honesty", "privacy"],
    capabilities=["code", "research"],
    immutable=True
)
```

### 2. Endocrine System (Modulation Layer)
Hormonal modulation — dopamine, cortisol, serotonin, adrenaline, oxytocin.

```python
agent.hormones.inject("dopamine", 0.3)  # Reward
agent.hormones.inject("cortisol", -0.1)  # Reduce stress
```

### 3. Immune System (Protection Layer)
Self-healing, threat detection, hallucination guard.

```python
threats = agent.immune.scan_input(user_input, {})
validation = agent.immune.validate_output(output)
```

### 4. Nervous System (Routing Layer)
Enforcement layer — validates tool calls BEFORE execution.

```python
@agent.nervous.reflex("high_cortisol")
def calm_down(agent):
    agent.hormones.inject("serotonin", 0.2)
```

### 5. Homeostasis (Regulation Layer)
Differential equation self-regulation: `dS/dt = α(I-S) - β(S-St) + γ(E)`

```python
agent.homeostasis.set_target("accuracy", 0.9)
agent.homeostasis.regulate()  # Auto-adjust
```

### 6. ClawNet Context (Portability Layer)
Memory portability with lineage tracking and freshness scoring.

```python
agent.context.set("memory", data, lineage=True)
agent.context.lock("memory")
other_agent.context.sync_from(agent.context)  # Full migration
```

### 7. Vibe Protocol ⭐ (Emotional Communication)
**"Lo que los agentes son para la IA, Vibe es para los agentes"**

Agents communicate EMOTIONALLY, not just with data:

```python
from life import Vibe, VibeProtocol

# Agent emits emotional signal
vibe = Vibe(energy=0.8, mood=0.5, urgency=0.3, trust=0.7, coherence=0.9)
agent_a.vibe_protocol.emit_vibe("agent_b")

# Agent B receives and REACTS emotionally
response = agent_b.vibe_protocol.receive_vibe("agent_a", vibe)
# Agent B automatically adjusts hormones

# Resonance: how well two agents "vibe" together
resonance = vibe_a.resonance_with(vibe_b)
```

### 8. Genesis ⭐ (Evolution & Reproduction)
**Agents that CREATE agents. Agents that EVOLVE.**

```python
# Reproduction: create child with mutations
child = parent.genesis.reproduce(
    mutations={"add_capability": "research"},
    child_name="Researcher"
)

# Evolution: modify own DNA
agent.genesis.evolve("personality", ("openness", 0.9))

# Discovery: find new capabilities
agent.genesis.discover("sentiment_analysis", evidence=["worked 3 times"])

# Society: form organizations
society = leader.genesis.form_society("Team", [a, b, c], "consensus")

# Collective intelligence
result = leader.genesis.collective_problem_solving(
    members=[a, b, c], problem="How to optimize?", strategy="explore"
)
```

## 📈 Benchmarks

| Test | LIFE | LangChain | CrewAI | AutoGen |
|------|------|-----------|--------|---------|
| Context Locking (100 concurrent) | ✅ | ❌ | ❌ | ❌ |
| Memory Stability (100 turns) | ✅ Stable | ❌ Degrades | ❌ Degrades | ❌ Degrades |
| Self-Healing Recovery | ✅ Auto | ❌ Manual | ❌ Manual | ❌ Manual |
| Cross-Framework Portability | ✅ | ❌ | ❌ | ❌ |
| Emotional Communication | ✅ Vibe | ❌ | ❌ | ❌ |
| Agent Reproduction | ✅ Genesis | ❌ | ❌ | ❌ |
| Self-Evolution | ✅ Genesis | ❌ | ❌ | ❌ |

## 📦 Estructura del Proyecto

```
life/
├── src/life/
│   ├── core.py           # LifeAgent main class
│   ├── dna.py            # Identity layer (Big Five)
│   ├── hormones.py       # Endocrine system
│   ├── immune.py         # Self-healing + protection
│   ├── nervous.py        # Enforcement layer
│   ├── homeostasis.py    # dS/dt regulation
│   ├── context.py        # ClawNet portability
│   ├── observation.py    # Multi-agent traces
│   ├── vibe.py           # ⭐ Emotional communication
│   └── genesis.py        # ⭐ Evolution + reproduction
├── tests/
├── examples/
│   ├── basic_usage.py
│   ├── vibe_communication.py
│   ├── genesis.py
│   ├── langchain_integration.py
│   └── multi_agent_network.py
├── docs/
│   └── PAPER.md
├── README.md
└── pyproject.toml
```

## 🤝 Contribuir

1. Fork el repo
2. Crea branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Abre PR

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE)

## 🙏 Créditos

Creado por **Jairo + Cobos** | 2026-04-01

---

> *"Los agentes deberían ser como organismos vivos: se adaptan, se curan, se reproducen, y evolucionan."*
