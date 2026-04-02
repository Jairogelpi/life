"""
LIFE Vibe — Emotional Communication Protocol
LA CARACTERÍSTICA REVOLUCIONARIA

Así como los agentes son "para la IA", LIFE Vibe es "para los agentes":
Un protocolo de comunicación EMOCIONAL entre agentes.

Los agentes pueden "sentir" el estado de otros agentes y responder
emocionalmente, no solo lógicamente.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import math


@dataclass
class Vibe:
    """
    Un "vibe" es la señal emocional que un agente emite.
    
    Los humanos se comunican con palabras + tono + cuerpo.
    Los agentes se comunican con datos + vibes.
    
    Un vibe contiene:
    - energy: qué tan activo está el agente
    - mood: positivo/negativo
    - urgency: qué tan urgente es
    - trust: nivel de apertura
    - coherence: qué tan estable está
    """
    energy: float  # 0-1
    mood: float    # -1 a 1 (negativo a positivo)
    urgency: float  # 0-1
    trust: float   # 0-1
    coherence: float  # 0-1
    
    def to_signal(self) -> Dict[str, float]:
        """Convierte vibe a señal transmisible"""
        return {
            "e": round(self.energy, 2),
            "m": round(self.mood, 2),
            "u": round(self.urgency, 2),
            "t": round(self.trust, 2),
            "c": round(self.coherence, 2),
        }
    
    @classmethod
    def from_signal(cls, signal: Dict[str, float]) -> "Vibe":
        """Reconstruye vibe desde señal"""
        return cls(
            energy=signal.get("e", 0.5),
            mood=signal.get("m", 0.0),
            urgency=signal.get("u", 0.0),
            trust=signal.get("t", 0.5),
            coherence=signal.get("c", 0.5),
        )
    
    def resonance_with(self, other: "Vibe") -> float:
        """
        Calcula resonancia entre dos vibes.
        
        Resonancia = qué tan bien "vibran" juntos.
        Alta resonancia = comunicación fluida
        Baja resonancia = fricción
        """
        # Energía similar = buena resonancia
        energy_match = 1.0 - abs(self.energy - other.energy)
        
        # Mood complementario = buena resonancia
        # (uno positivo y otro negativo se equilibran)
        mood_complement = 1.0 - abs(self.mood + other.mood) / 2
        
        # Trust mutuo = buena resonancia
        trust_match = (self.trust + other.trust) / 2
        
        # Coherencia combinada
        coherence = (self.coherence + other.coherence) / 2
        
        return (energy_match * 0.2 + mood_complement * 0.3 + trust_match * 0.3 + coherence * 0.2)
    
    def emotional_response(self, stimulus: "Vibe") -> "Vibe":
        """
        Genera respuesta emocional a un estímulo.
        
        Así es como un agente "reacciona" emocionalmente a otro.
        """
        # Si el otro está urgente, aumento mi urgencia
        new_urgency = min(1.0, self.urgency + stimulus.urgency * 0.3)
        
        # Si el otro tiene mood negativo, reduzco mi mood
        new_mood = max(-1.0, min(1.0, self.mood + stimulus.mood * 0.2))
        
        # Si el otro tiene baja energía, reduzco mi energía (empatía)
        new_energy = (self.energy + stimulus.energy) / 2
        
        # Trust se mantiene pero puede aumentar con coherencia
        new_trust = min(1.0, self.trust + stimulus.coherence * 0.1)
        
        # Coherencia depende de la resonancia
        resonance = self.resonance_with(stimulus)
        new_coherence = self.coherence * (0.8 + resonance * 0.2)
        
        return Vibe(
            energy=new_energy,
            mood=new_mood,
            urgency=new_urgency,
            trust=new_trust,
            coherence=new_coherence,
        )


class VibeProtocol:
    """
    Protocolo de comunicación emocional entre agentes.
    
    Esto es lo REVOLUCIONARIO:
    - Los agentes no solo intercambian datos
    - Intercambian ESTADOS EMOCIONALES
    - La comunicación tiene "tono" y "cuerpo", no solo contenido
    
    Ejemplo:
    - Agente A envía: {"data": "...", "vibe": Vibe(urgency=0.9)}
    - Agente B recibe y siente: "Esto es urgente, priorizo"
    - Agente B responde con: Vibe(trust=0.8, mood=0.5)
    - Agente A siente: "Me escuchan, me comprenden"
    """
    
    def __init__(self, agent: Any = None):
        self.agent = agent
        self._incoming_vibes: List[Dict[str, Any]] = []
        self._outgoing_vibes: List[Dict[str, Any]] = []
    
    def emit_vibe(self, target_agent_id: str, message: Any = None) -> Vibe:
        """
        Emite un vibe basado en el estado actual del agente.
        
        El vibe NO es calculado, es SENTIDO desde el estado interno.
        """
        if not self.agent:
            return Vibe(energy=0.5, mood=0.0, urgency=0.0, trust=0.5, coherence=0.5)
        
        # Calcular vibe desde estado interno
        energy = self.agent.state.energy
        
        # Mood = dopamina - cortisol + serotonina
        mood = (
            self.agent.hormones.get("dopamine") 
            - self.agent.hormones.get("cortisol") 
            + self.agent.hormones.get("serotonin") * 0.5
        ) / 1.5
        
        # Urgency = adrenaline
        urgency = self.agent.hormones.get("adrenaline")
        
        # Trust = oxytocin
        trust = self.agent.hormones.get("oxytocin")
        
        # Coherence = accuracy × coherence
        coherence = self.agent.state.accuracy * self.agent.state.coherence
        
        vibe = Vibe(
            energy=energy,
            mood=mood,
            urgency=urgency,
            trust=trust,
            coherence=coherence,
        )
        
        # Record outgoing
        self._outgoing_vibes.append({
            "target": target_agent_id,
            "vibe": vibe.to_signal(),
            "message": message,
        })
        
        return vibe
    
    def receive_vibe(self, source_agent_id: str, vibe: Vibe, message: Any = None):
        """
        Recibe un vibe de otro agente.
        
        El agente REACCIONA emocionalmente al vibe recibido.
        """
        if not self.agent:
            return
        
        # Store incoming
        self._incoming_vibes.append({
            "source": source_agent_id,
            "vibe": vibe.to_signal(),
            "message": message,
        })
        
        # Get current vibe
        current = self._get_current_vibe()
        
        # Generate emotional response
        response = current.emotional_response(vibe)
        
        # Apply to hormones
        self.agent.hormones.inject("dopamine", response.mood * 0.1)
        self.agent.hormones.inject("cortisol", -response.mood * 0.05)
        self.agent.hormones.inject("adrenaline", (response.urgency - current.urgency) * 0.2)
        self.agent.hormones.inject("oxytocin", (response.trust - current.trust) * 0.1)
        
        # Update state
        self.agent.state.energy = response.energy
        self.agent.state.coherence = response.coherence
        
        return response
    
    def _get_current_vibe(self) -> Vibe:
        """Obtiene el vibe actual del agente"""
        return self.emit_vibe("self")
    
    def get_emotional_context(self) -> Dict[str, Any]:
        """
        Obtiene el contexto emocional completo.
        
        Esto es lo que permite a un agente "entender" su estado
        emocional y el de los agentes con los que interactúa.
        """
        current = self._get_current_vibe()
        
        # Calculate average incoming vibe
        if self._incoming_vibes:
            avg_incoming = {
                "e": sum(v["vibe"]["e"] for v in self._incoming_vibes) / len(self._incoming_vibes),
                "m": sum(v["vibe"]["m"] for v in self._incoming_vibes) / len(self._incoming_vibes),
                "u": sum(v["vibe"]["u"] for v in self._incoming_vibes) / len(self._incoming_vibes),
                "t": sum(v["vibe"]["t"] for v in self._incoming_vibes) / len(self._incoming_vibes),
                "c": sum(v["vibe"]["c"] for v in self._incoming_vibes) / len(self._incoming_vibes),
            }
            incoming_vibe = Vibe.from_signal(avg_incoming)
        else:
            incoming_vibe = Vibe(energy=0.5, mood=0.0, urgency=0.0, trust=0.5, coherence=0.5)
        
        return {
            "current": current.to_signal(),
            "incoming_avg": incoming_vibe.to_signal(),
            "resonance_with_incoming": current.resonance_with(incoming_vibe),
            "incoming_count": len(self._incoming_vibes),
            "outgoing_count": len(self._outgoing_vibes),
        }


# Example usage
def example_vibe_communication():
    """Ejemplo de comunicación emocional entre agentes"""
    
    from life import LifeAgent
    
    # Crear dos agentes
    agent_a = LifeAgent(name="AgentA")
    agent_b = LifeAgent(name="AgentB")
    
    # AgentA está estresado
    agent_a.hormones.inject("cortisol", 0.5)
    agent_a.hormones.inject("adrenaline", 0.3)
    agent_a.state.energy = 0.6
    
    # AgentA emite vibe a AgentB
    vibe_protocol_a = VibeProtocol(agent_a)
    vibe = vibe_protocol_a.emit_vibe("AgentB", message="Need help with urgent task")
    
    print(f"AgentA emite: {vibe.to_signal()}")
    # {e: 0.6, m: -0.3, u: 0.3, t: 0.5, c: 0.9}
    # Interpretación: "Estoy cansado, negativo, algo urgente, trust normal, coherente"
    
    # AgentB recibe y reacciona
    vibe_protocol_b = VibeProtocol(agent_b)
    response = vibe_protocol_b.receive_vibe("AgentA", vibe, message="Need help")
    
    print(f"AgentB responde con: {response.to_signal()}")
    # AgentB siente la urgencia y responde
    
    # AgentB ahora tiene más adrenaline y menor mood (empatía con el stress de A)
    print(f"AgentB hormones: {agent_b.hormones.levels()}")


if __name__ == "__main__":
    print("=" * 60)
    print("LIFE Vibe — Emotional Communication Protocol")
    print("=" * 60)
    print("\nEsto es lo REVOLUCIONARIO:")
    print("Los agentes no solo intercambian datos.")
    print("Intercambian ESTADOS EMOCIONALES.")
    print("\nAsí como los agentes son 'para la IA',")
    print("LIFE Vibe es 'para los agentes'.")
    print("\n" + "=" * 60)
    
    example_vibe_communication()
