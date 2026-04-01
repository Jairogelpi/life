"""
Observation System — Multi-agent observability
Solves: Gap #1 — Observability/Debugging cross-framework
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Trace:
    """Execution trace for a single action"""
    trace_id: str
    agent_id: str
    task: str
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    ended_at: Optional[str] = None
    success: Optional[bool] = None
    result: Any = None
    error: Optional[str] = None
    sub_traces: List["Trace"] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ObservationSystem:
    """
    Full observability for multi-agent systems.
    
    This solves the #1 gap: no cross-framework observability.
    Every action is traced, every state change is logged,
    and the full execution graph is queryable.
    """
    
    def __init__(self, agent_id: str = ""):
        self.agent_id = agent_id
        self._traces: Dict[str, Trace] = {}
        self._active_trace: Optional[Trace] = None
        self._trace_stack: List[Trace] = []
        self._events: List[Dict[str, Any]] = []
    
    def start_trace(self, task: str, metadata: Optional[Dict] = None) -> str:
        """Start a new trace"""
        import uuid
        trace_id = str(uuid.uuid4())[:8]
        
        trace = Trace(
            trace_id=trace_id,
            agent_id=self.agent_id,
            task=task,
            metadata=metadata or {},
        )
        
        self._traces[trace_id] = trace
        
        if self._trace_stack:
            # This is a sub-trace
            self._trace_stack[-1].sub_traces.append(trace)
        
        self._trace_stack.append(trace)
        self._active_trace = trace
        
        self._log_event("trace_start", trace_id, task)
        
        return trace_id
    
    def end_trace(self, success: bool, result: Any = None, error: Optional[str] = None):
        """End the current trace"""
        if not self._trace_stack:
            return
        
        trace = self._trace_stack.pop()
        trace.ended_at = datetime.utcnow().isoformat()
        trace.success = success
        trace.result = result
        trace.error = error
        
        self._log_event(
            "trace_end",
            trace.trace_id,
            "success" if success else f"error: {error}",
        )
        
        self._active_trace = self._trace_stack[-1] if self._trace_stack else None
    
    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get trace by ID"""
        return self._traces.get(trace_id)
    
    def get_traces(self, agent_id: Optional[str] = None, limit: int = 50) -> List[Trace]:
        """Get traces, optionally filtered by agent"""
        traces = list(self._traces.values())
        if agent_id:
            traces = [t for t in traces if t.agent_id == agent_id]
        return traces[-limit:]
    
    def get_failed_traces(self) -> List[Trace]:
        """Get all failed traces"""
        return [t for t in self._traces.values() if t.success is False]
    
    def get_execution_graph(self, trace_id: str) -> Dict[str, Any]:
        """
        Get full execution graph for a trace.
        This is what makes multi-agent debugging possible.
        """
        trace = self._traces.get(trace_id)
        if not trace:
            return {}
        
        return {
            "trace_id": trace.trace_id,
            "agent_id": trace.agent_id,
            "task": trace.task,
            "success": trace.success,
            "duration": self._calculate_duration(trace),
            "sub_traces": [
                self.get_execution_graph(st.trace_id)
                for st in trace.sub_traces
            ],
        }
    
    def stats(self) -> Dict[str, Any]:
        """Get observation statistics"""
        traces = list(self._traces.values())
        successful = sum(1 for t in traces if t.success is True)
        failed = sum(1 for t in traces if t.success is False)
        
        return {
            "total_traces": len(traces),
            "successful": successful,
            "failed": failed,
            "success_rate": successful / max(len(traces), 1),
            "events_logged": len(self._events),
        }
    
    def _calculate_duration(self, trace: Trace) -> Optional[float]:
        """Calculate trace duration in seconds"""
        if not trace.ended_at:
            return None
        start = datetime.fromisoformat(trace.started_at)
        end = datetime.fromisoformat(trace.ended_at)
        return (end - start).total_seconds()
    
    def _log_event(self, event_type: str, trace_id: str, message: str):
        """Log an observation event"""
        self._events.append({
            "type": event_type,
            "trace_id": trace_id,
            "agent_id": self.agent_id,
            "message": message,
            "at": datetime.utcnow().isoformat(),
        })
    
    def export(self) -> Dict[str, Any]:
        """Export observations for external consumption"""
        return {
            "agent_id": self.agent_id,
            "traces": len(self._traces),
            "events": len(self._events),
            "stats": self.stats(),
        }
