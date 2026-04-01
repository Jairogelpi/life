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
- **Observables** — full visibility de qué agente vio qué
- **Resilientes** — sistema inmune detecta y corrige errores
- **Válidos** — ADN inmutable + validación automática

## 📊 Los 10 GAPS que LIFE resuelve

| # | Gap | Solución LIFE |
|---|-----|---------------|
| 1 | Observability multi-agent | **Observation System** — traces cross-framework |
| 2 | Memory rot | **Homeostasis** — memoria que se autocorrige |
| 3 | Evaluación confiable | **DNA Validator** — validación automática |
| 4 | Coordinación multi-agent | **Endocrine System** — modulación hormonal |
| 5 | Pilot-to-production | **Immune System** — self-healing automático |
| 6 | Enforcement layer | **Nervous System** — validación previa de tool calls |
| 7 | Coste impredecible | **Metabolic Rate** — budget tracking biológico |
| 8 | Semantic drift | **Temporal Rhythm** — frescura en embeddings |
| 9 | Seguridad en cascada | **Immune Memory** — resistencia a ataques |
| 10 | Interoperabilidad | **Cell Protocol** — agentes intercambiables |

## 🔧 Quick Start

```python
from life import LifeAgent, DNA, Personality

# Crear agente con ADN personalizado
agent = LifeAgent(
    name="HelperBot",
    dna=DNA(
        name="HelperBot",
        personality=Personality(
            openness=0.8,
            conscientiousness=0.9,
        ),
        values=["helpfulness", "honesty"],
        capabilities=["research", "communication"],
    ),
)

# Ejecutar tarea con regulación biológica completa
result = agent.execute("Analyze this data")

# El agente se autorregula
print(f"Energy: {agent.state.energy:.2f}")
print(f"Accuracy: {agent.state.accuracy:.2f}")
print(f"Hormones: {agent.hormones.levels()}")
```

## 🧠 Componentes

### 1. DNA (Identity Layer)
Identidad inmutable del agente.

```python
dna = DNA(
    personality=Personality(openness=0.8, conscientiousness=0.9),
    values=["honesty", "privacy"],
    capabilities=["code", "research"],
    immutable=True  # No se puede cambiar después de crear
)
```

### 2. Endocrine System (Modulation Layer)
Modulación hormonal del comportamiento.

```python
agent.hormones.inject("dopamine", 0.3)  # Reward por éxito
agent.hormones.inject("cortisol", -0.1)  # Reducir stress
```

### 3. Immune System (Protection Layer)
Self-healing y protección contra amenazas.

```python
# Auto-detecta y corrige
threats = agent.immune.scan_input(user_input, {})
validation = agent.immune.validate_output(output)
```

### 4. Nervous System (Routing Layer)
Enforcement layer para tool calls.

```python
@agent.nervous.reflex("high_cortisol")
def calm_down(agent):
    agent.hormones.inject("serotonin", 0.2)
    return "Agent calmed down"
```

### 5. Homeostasis (Regulation Layer)
Auto-regulación mediante ecuaciones diferenciales.

```python
agent.homeostasis.set_target("accuracy", 0.9)
agent.homeostasis.regulate()  # Auto-adjust
```

### 6. ClawNet Context (Portability Layer)
Memoria portable entre agentes.

```python
# Migrar contexto a otro agente
agent.context.set("memory", data, lineage=True)
agent.context.lock("memory")
other_agent.context.sync_from(agent.context)
```

### 7. Observation System (Observability Layer)
Traces cross-framework para debugging.

```python
traces = agent.observation.get_traces()
graph = agent.observation.get_execution_graph(trace_id)
```

## 📈 Benchmarks

| Test | LIFE | LangChain | CrewAI |
|------|------|-----------|--------|
| Context Locking (100 concurrent) | ✅ | ❌ | ❌ |
| Memory Rot (100 turns) | ✅ Stable | ❌ Degrades | ❌ Degrades |
| Self-Healing (error recovery) | ✅ Auto | ❌ Manual | ❌ Manual |
| Cross-Framework Portability | ✅ | ❌ | ❌ |

## 📦 Estructura del Proyecto

```
life/
├── src/life/
│   ├── __init__.py
│   ├── core.py           # LifeAgent main class
│   ├── dna.py            # Identity layer
│   ├── hormones.py       # Endocrine system
│   ├── immune.py         # Self-healing
│   ├── nervous.py        # Enforcement layer
│   ├── homeostasis.py    # Self-regulation
│   ├── context.py        # ClawNet portability
│   └── observation.py    # Observability
├── tests/
│   └── test_life.py
├── examples/
│   ├── basic_usage.py
│   ├── langchain_integration.py
│   └── multi_agent_network.py
├── README.md
├── LICENSE
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

Inspirado por:
- OpenClaw (harness over model)
- Damasio (somatic markers)
- Tononi (integrated information)
- Buzsáki (hippocampal replay)

---

> *"Los agentes deberían ser como organismos vivos: se adaptan, se curan, y evolucionan."*
