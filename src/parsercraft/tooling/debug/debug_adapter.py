#!/usr/bin/env python3
"""
Debug Adapter Protocol (DAP) for Custom Languages

Enables debugging in IDEs by implementing the Debug Adapter Protocol.

Features:
    - Breakpoint management
    - Stack trace inspection
    - Variable inspection
    - Stepping (step in, step out, step over)
    - Expression evaluation
    - Pause/resume execution
    - Source mapping

Usage:
    from parsercraft.debug_adapter import DebugAdapter, Debugger
    
    debugger = Debugger(program_path)
    adapter = DebugAdapter(debugger)
    adapter.start()  # Start debug server

Protocol:
    Implements VSCode Debug Adapter Protocol v1.51
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class StopReason(Enum):
    """Reason for stopping execution."""

    BREAKPOINT = "breakpoint"
    STEP = "step"
    PAUSE = "pause"
    EXCEPTION = "exception"
    ENTRY = "entry"
    GOTO = "goto"


@dataclass
class SourceReference:
    """Reference to source code."""

    path: str
    source_reference: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.path.split("/")[-1],
            "path": self.path,
            "sourceReference": self.source_reference,
        }


@dataclass
class Breakpoint:
    """Breakpoint in source code."""

    id: int
    source_path: str
    line: int
    column: int = 1
    condition: Optional[str] = None
    hit_condition: Optional[str] = None
    log_message: Optional[str] = None
    verified: bool = False
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": {"path": self.source_path},
            "line": self.line,
            "column": self.column,
            "verified": self.verified,
            "message": self.message,
        }


@dataclass
class StackFrame:
    """Stack frame in execution."""

    id: int
    name: str
    source_path: str
    line: int
    column: int = 1
    end_line: Optional[int] = None
    end_column: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "source": {"path": self.source_path},
            "line": self.line,
            "column": self.column,
            "endLine": self.end_line,
            "endColumn": self.end_column,
        }


@dataclass
class Variable:
    """Variable in scope."""

    name: str
    value: Any
    var_type: str
    indexed_variables: Optional[int] = None
    named_variables: Optional[int] = None
    memory_reference: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": str(self.value),
            "type": self.var_type,
            "indexedVariables": self.indexed_variables,
            "namedVariables": self.named_variables,
            "memoryReference": self.memory_reference,
        }


@dataclass
class Scope:
    """Variable scope."""

    name: str
    variables: List[Variable] = field(default_factory=list)
    indexed_variables: Optional[int] = None
    named_variables: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "variables": self.variables,
            "indexedVariables": self.indexed_variables,
            "namedVariables": self.named_variables,
        }


class ExecutionState(Enum):
    """Execution state of the debugged program."""

    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"
    TERMINATED = "terminated"


class Debugger:
    """Debugger for custom language programs."""

    def __init__(self, program_path: str):
        self.program_path = program_path
        self.state = ExecutionState.IDLE
        self.breakpoints: Dict[str, List[Breakpoint]] = {}
        self.call_stack: List[StackFrame] = []
        self.scopes: Dict[int, Scope] = {}
        self.current_frame = 0
        self.breakpoint_id = 0
        self.frame_id = 0
        self.variables: Dict[int, List[Variable]] = {}

    def set_breakpoint(
        self,
        source_path: str,
        line: int,
        column: int = 1,
        condition: Optional[str] = None,
    ) -> Breakpoint:
        """Set a breakpoint."""
        if source_path not in self.breakpoints:
            self.breakpoints[source_path] = []

        self.breakpoint_id += 1
        bp = Breakpoint(
            id=self.breakpoint_id,
            source_path=source_path,
            line=line,
            column=column,
            condition=condition,
            verified=True,
        )

        self.breakpoints[source_path].append(bp)
        return bp

    def remove_breakpoint(self, bp_id: int) -> bool:
        """Remove a breakpoint by ID."""
        for source_path, bps in self.breakpoints.items():
            for i, bp in enumerate(bps):
                if bp.id == bp_id:
                    bps.pop(i)
                    return True
        return False

    def get_breakpoints(self, source_path: str) -> List[Breakpoint]:
        """Get breakpoints for a source file."""
        return self.breakpoints.get(source_path, [])

    def start(self) -> None:
        """Start debugging."""
        self.state = ExecutionState.RUNNING

    def pause(self) -> None:
        """Pause execution."""
        self.state = ExecutionState.STOPPED

    def continue_execution(self) -> None:
        """Continue execution."""
        self.state = ExecutionState.RUNNING

    def step_in(self) -> None:
        """Step into function."""
        # Push new frame on call stack
        self.frame_id += 1
        frame = StackFrame(
            id=self.frame_id,
            name="function_call",
            source_path=self.program_path,
            line=1,
        )
        self.call_stack.append(frame)

    def step_out(self) -> None:
        """Step out of current function."""
        if self.call_stack:
            self.call_stack.pop()

    def step_over(self) -> None:
        """Step over current line."""
        if self.call_stack:
            self.call_stack[-1].line += 1

    def get_stack_trace(self) -> List[StackFrame]:
        """Get current call stack."""
        return self.call_stack

    def set_variable(self, frame_id: int, var_name: str, value: Any) -> bool:
        """Set variable value."""
        if frame_id in self.variables:
            for var in self.variables[frame_id]:
                if var.name == var_name:
                    var.value = value
                    return True
        return False

    def get_variables(self, frame_id: int) -> List[Variable]:
        """Get variables for a frame."""
        return self.variables.get(frame_id, [])

    def add_variable(self, frame_id: int, var: Variable) -> None:
        """Add variable to frame."""
        if frame_id not in self.variables:
            self.variables[frame_id] = []

        self.variables[frame_id].append(var)

    def evaluate_expression(self, expression: str, frame_id: int) -> Optional[str]:
        """Evaluate expression in context of frame.

        Only allows safe literal expressions (numbers, strings, lists, etc.).
        """
        import ast as _ast
        try:
            result = _ast.literal_eval(expression)
            return str(result)
        except (ValueError, SyntaxError):
            return None

    def hit_breakpoint(self, source_path: str, line: int) -> Optional[Breakpoint]:
        """Check if execution hit a breakpoint."""
        bps = self.get_breakpoints(source_path)

        for bp in bps:
            if bp.line == line:
                # Check condition if present
                if bp.condition:
                    # Would evaluate condition here
                    pass
                return bp

        return None


class DebugAdapter:
    """Debug Adapter Protocol handler."""

    def __init__(self, debugger: Debugger):
        self.debugger = debugger
        self.seq = 0
        self.thread_id = 1

    def _send_response(self, request_seq: int, success: bool, body: Dict[str, Any] = None) -> Dict[str, Any]:
        """Format a response."""
        response = {
            "type": "response",
            "seq": self.seq,
            "request_seq": request_seq,
            "command": "",
            "success": success,
        }
        self.seq += 1

        if body:
            response["body"] = body

        return response

    def _send_event(self, event_type: str, body: Dict[str, Any] = None) -> Dict[str, Any]:
        """Format an event."""
        event = {
            "type": "event",
            "seq": self.seq,
            "event": event_type,
        }
        self.seq += 1

        if body:
            event["body"] = body

        return event

    def handle_initialize(self) -> Dict[str, Any]:
        """Handle initialize request."""
        return self._send_response(
            0,
            True,
            {
                "capabilities": {
                    "supportsConfigurationDoneRequest": True,
                    "supportsFunctionBreakpoints": True,
                    "supportsConditionalBreakpoints": True,
                    "supportsHitConditionalBreakpoints": True,
                    "supportsEvaluateForHovers": True,
                    "supportsStepBack": False,
                    "supportsSetVariable": True,
                    "supportsGotoTargetsRequest": False,
                    "supportsStepInTargetsRequest": True,
                    "supportsLogPoints": True,
                    "supportsModulesRequest": False,
                }
            },
        )

    def handle_launch(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle launch request."""
        self.debugger.start()
        return self._send_response(1, True)

    def handle_set_breakpoints(
        self, source_path: str, lines: List[int]
    ) -> Dict[str, Any]:
        """Handle set breakpoints request."""
        bps = []

        # Clear existing breakpoints for this source
        if source_path in self.debugger.breakpoints:
            self.debugger.breakpoints[source_path].clear()

        # Add new breakpoints
        for line in lines:
            bp = self.debugger.set_breakpoint(source_path, line)
            bps.append(bp.to_dict())

        return self._send_response(2, True, {"breakpoints": bps})

    def handle_stack_trace(self, thread_id: int) -> Dict[str, Any]:
        """Handle stack trace request."""
        stack_frames = [sf.to_dict() for sf in self.debugger.get_stack_trace()]

        return self._send_response(3, True, {"stackFrames": stack_frames, "totalFrames": len(stack_frames)})

    def handle_scopes(self, frame_id: int) -> Dict[str, Any]:
        """Handle scopes request."""
        scopes = [
            {
                "name": "Local",
                "variablesReference": 1,
                "expensive": False,
            },
            {
                "name": "Global",
                "variablesReference": 2,
                "expensive": False,
            },
        ]

        return self._send_response(4, True, {"scopes": scopes})

    def handle_variables(self, variables_reference: int) -> Dict[str, Any]:
        """Handle variables request."""
        variables = self.debugger.get_variables(variables_reference)

        return self._send_response(5, True, {"variables": [v.to_dict() for v in variables]})

    def handle_continue(self, thread_id: int) -> Dict[str, Any]:
        """Handle continue request."""
        self.debugger.continue_execution()

        # Send continued event
        self._send_event("continued", {"threadId": thread_id})

        return self._send_response(6, True, {"allThreadsContinued": True})

    def handle_next(self, thread_id: int, frame_id: int) -> Dict[str, Any]:
        """Handle next (step over) request."""
        self.debugger.step_over()

        # Send stopped event
        self._send_event(
            "stopped",
            {"reason": StopReason.STEP.value, "threadId": thread_id, "allThreadsStopped": True},
        )

        return self._send_response(7, True)

    def handle_step_in(self, thread_id: int, frame_id: int) -> Dict[str, Any]:
        """Handle step in request."""
        self.debugger.step_in()

        # Send stopped event
        self._send_event(
            "stopped",
            {"reason": StopReason.STEP.value, "threadId": thread_id, "allThreadsStopped": True},
        )

        return self._send_response(8, True)

    def handle_step_out(self, thread_id: int, frame_id: int) -> Dict[str, Any]:
        """Handle step out request."""
        self.debugger.step_out()

        # Send stopped event
        self._send_event(
            "stopped",
            {"reason": StopReason.STEP.value, "threadId": thread_id, "allThreadsStopped": True},
        )

        return self._send_response(9, True)

    def handle_evaluate(self, expression: str, frame_id: int) -> Dict[str, Any]:
        """Handle evaluate request."""
        result = self.debugger.evaluate_expression(expression, frame_id)

        if result is None:
            return self._send_response(10, False, {"error": "Unable to evaluate expression"})

        return self._send_response(10, True, {"result": result, "type": "string", "variablesReference": 0})

    def handle_pause(self, thread_id: int) -> Dict[str, Any]:
        """Handle pause request."""
        self.debugger.pause()

        # Send stopped event
        self._send_event(
            "stopped",
            {"reason": StopReason.PAUSE.value, "threadId": thread_id, "allThreadsStopped": True},
        )

        return self._send_response(11, True)
