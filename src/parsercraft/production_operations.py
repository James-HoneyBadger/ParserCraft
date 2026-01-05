"""
Production Operations and Recovery

Provides operational health checks, graceful degradation, recovery procedures,
and monitoring capabilities for production deployments.
"""

from __future__ import annotations

import time
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Tuple
from abc import ABC, abstractmethod


class ServiceHealth(Enum):
    """Service health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class RecoveryStrategy(Enum):
    """Recovery strategy for failed services."""
    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAK = "circuit_break"
    GRACEFUL_DEGRADE = "graceful_degrade"


@dataclass
class HealthCheck:
    """Result of a health check."""
    name: str
    status: ServiceHealth
    timestamp: float
    response_time_ms: float
    message: str
    checks: Dict[str, bool] = field(default_factory=dict)
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "response_time_ms": self.response_time_ms,
            "message": self.message,
            "checks": self.checks,
            "details": self.details,
        }


@dataclass
class RecoveryPlan:
    """Recovery plan for a failed operation."""
    operation: str
    strategy: RecoveryStrategy
    max_retries: int = 3
    retry_delay_ms: int = 100
    fallback_handler: Optional[Callable] = None
    timeout_ms: int = 5000


class HealthCheckProvider(ABC):
    """Base class for health check providers."""

    @abstractmethod
    def check_health(self) -> HealthCheck:
        """Check service health."""
        pass


class ServiceHealthMonitor:
    """Monitors health of multiple services."""

    def __init__(self):
        self.providers: Dict[str, HealthCheckProvider] = {}
        self.health_history: Dict[str, List[HealthCheck]] = {}
        self.recovery_plans: Dict[str, RecoveryPlan] = {}
        self.logger = logging.getLogger("health_monitor")

    def register_provider(self, name: str, provider: HealthCheckProvider) -> None:
        """Register a health check provider."""
        self.providers[name] = provider
        self.health_history[name] = []

    def register_recovery_plan(self, operation: str, plan: RecoveryPlan) -> None:
        """Register a recovery plan."""
        self.recovery_plans[operation] = plan

    def check_all(self) -> Dict[str, HealthCheck]:
        """Check health of all services."""
        results = {}
        for name, provider in self.providers.items():
            try:
                check = provider.check_health()
                results[name] = check
                self.health_history[name].append(check)

                self.logger.info(f"Health check {name}: {check.status.value}")
            except Exception as e:
                self.logger.error(f"Health check {name} failed: {e}")
                results[name] = HealthCheck(
                    name=name,
                    status=ServiceHealth.UNHEALTHY,
                    timestamp=time.time(),
                    response_time_ms=-1,
                    message=str(e),
                )

        return results

    def get_overall_health(self) -> ServiceHealth:
        """Get overall system health."""
        checks = self.check_all()
        if not checks:
            return ServiceHealth.HEALTHY

        statuses = [check.status for check in checks.values()]

        if any(s == ServiceHealth.UNHEALTHY for s in statuses):
            return ServiceHealth.UNHEALTHY
        elif any(s == ServiceHealth.DEGRADED for s in statuses):
            return ServiceHealth.DEGRADED
        else:
            return ServiceHealth.HEALTHY

    def get_health_summary(self) -> Dict[str, Any]:
        """Get health summary."""
        checks = self.check_all()
        return {
            "timestamp": time.time(),
            "overall_status": self.get_overall_health().value,
            "services": {name: check.to_dict() for name, check in checks.items()},
        }

    def get_health_history(self, service: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get health history for a service."""
        if service not in self.health_history:
            return []
        return [h.to_dict() for h in self.health_history[service][-limit:]]


class RecoveryManager:
    """Manages recovery operations."""

    def __init__(self, monitor: ServiceHealthMonitor):
        self.monitor = monitor
        self.logger = logging.getLogger("recovery_manager")
        self.recovery_history: List[Dict[str, Any]] = []

    def execute_recovery(
        self,
        operation: str,
        func: Callable,
        *args,
        **kwargs,
    ) -> Tuple[bool, Any]:
        """Execute operation with recovery."""
        plan = self.monitor.recovery_plans.get(operation)
        if not plan:
            # No recovery plan, just execute
            try:
                return True, func(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Operation {operation} failed: {e}")
                return False, e

        # Execute with recovery strategy
        if plan.strategy == RecoveryStrategy.RETRY:
            return self._execute_with_retry(operation, plan, func, *args, **kwargs)
        elif plan.strategy == RecoveryStrategy.FALLBACK:
            return self._execute_with_fallback(operation, plan, func, *args, **kwargs)
        elif plan.strategy == RecoveryStrategy.CIRCUIT_BREAK:
            return self._execute_with_circuit_break(operation, plan, func, *args, **kwargs)
        elif plan.strategy == RecoveryStrategy.GRACEFUL_DEGRADE:
            return self._execute_with_degradation(operation, plan, func, *args, **kwargs)

        return True, func(*args, **kwargs)

    def _execute_with_retry(
        self,
        operation: str,
        plan: RecoveryPlan,
        func: Callable,
        *args,
        **kwargs,
    ) -> Tuple[bool, Any]:
        """Execute with retry."""
        for attempt in range(plan.max_retries):
            try:
                result = func(*args, **kwargs)
                self._log_recovery(operation, "retry", "success", attempt)
                return True, result
            except Exception as e:
                if attempt < plan.max_retries - 1:
                    time.sleep(plan.retry_delay_ms / 1000.0)
                else:
                    self._log_recovery(operation, "retry", "failed", attempt, str(e))
                    return False, e

    def _execute_with_fallback(
        self,
        operation: str,
        plan: RecoveryPlan,
        func: Callable,
        *args,
        **kwargs,
    ) -> Tuple[bool, Any]:
        """Execute with fallback."""
        try:
            result = func(*args, **kwargs)
            self._log_recovery(operation, "fallback", "primary_success")
            return True, result
        except Exception as e:
            if plan.fallback_handler:
                try:
                    result = plan.fallback_handler(*args, **kwargs)
                    self._log_recovery(operation, "fallback", "fallback_success")
                    return True, result
                except Exception as fallback_error:
                    self._log_recovery(
                        operation, "fallback", "fallback_failed", error=str(fallback_error)
                    )
                    return False, fallback_error
            else:
                self._log_recovery(operation, "fallback", "no_fallback", error=str(e))
                return False, e

    def _execute_with_circuit_break(
        self,
        operation: str,
        plan: RecoveryPlan,
        func: Callable,
        *args,
        **kwargs,
    ) -> Tuple[bool, Any]:
        """Execute with circuit breaker."""
        try:
            result = func(*args, **kwargs)
            self._log_recovery(operation, "circuit_break", "success")
            return True, result
        except Exception as e:
            self._log_recovery(operation, "circuit_break", "circuit_open", error=str(e))
            return False, e

    def _execute_with_degradation(
        self,
        operation: str,
        plan: RecoveryPlan,
        func: Callable,
        *args,
        **kwargs,
    ) -> Tuple[bool, Any]:
        """Execute with graceful degradation."""
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            # Degrade gracefully
            self._log_recovery(operation, "degradation", "degraded", error=str(e))
            return False, {"degraded": True, "error": str(e)}

    def _log_recovery(
        self,
        operation: str,
        strategy: str,
        status: str,
        attempt: int = 0,
        error: Optional[str] = None,
    ) -> None:
        """Log recovery event."""
        event = {
            "timestamp": time.time(),
            "operation": operation,
            "strategy": strategy,
            "status": status,
            "attempt": attempt,
            "error": error,
        }
        self.recovery_history.append(event)
        self.logger.info(f"Recovery [{operation}] {strategy}: {status}")

    def get_recovery_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recovery history."""
        return self.recovery_history[-limit:]


class GracefulShutdown:
    """Manages graceful shutdown of services."""

    def __init__(self):
        self.shutdown_handlers: List[Callable] = []
        self.logger = logging.getLogger("graceful_shutdown")

    def register_handler(self, handler: Callable) -> None:
        """Register a shutdown handler."""
        self.shutdown_handlers.append(handler)

    def execute_shutdown(self) -> None:
        """Execute graceful shutdown."""
        self.logger.info(f"Starting graceful shutdown ({len(self.shutdown_handlers)} handlers)")

        for handler in reversed(self.shutdown_handlers):  # LIFO order
            try:
                self.logger.info(f"Executing shutdown handler: {handler.__name__}")
                if callable(handler):
                    handler()
            except Exception as e:
                self.logger.error(f"Shutdown handler failed: {e}")

        self.logger.info("Graceful shutdown complete")


class OperationsGuide:
    """Reference guide for operations."""

    RUNBOOK = {
        "high_memory_usage": {
            "description": "System using excessive memory",
            "steps": [
                "Check memory usage: `ps aux`",
                "Identify large processes: `top -o %MEM`",
                "Check cache sizes in audit logs",
                "Consider rate limiting or circuit breakers",
                "Restart service if necessary",
            ],
        },
        "slow_response": {
            "description": "Operations taking longer than expected",
            "steps": [
                "Check service health: `GET /health`",
                "Review response times in audit logs",
                "Check rate limiter stats",
                "Check for timeouts",
                "Consider increasing timeouts or adding parallelization",
            ],
        },
        "circuit_breaker_open": {
            "description": "Circuit breaker has opened",
            "steps": [
                "Check underlying service health",
                "Review recent errors in audit logs",
                "Wait for recovery timeout (typically 60s)",
                "Circuit breaker will automatically recover",
                "Monitor for repeated failures",
            ],
        },
        "rate_limit_exceeded": {
            "description": "Rate limiting is active",
            "steps": [
                "Check rate limiter stats",
                "Reduce request rate or increase limits",
                "Check for thundering herd patterns",
                "Review request patterns in audit logs",
                "Consider implementing request batching",
            ],
        },
        "persistent_errors": {
            "description": "Errors persisting across retries",
            "steps": [
                "Collect error details from audit logs",
                "Check error context and categories",
                "Verify all dependencies are healthy",
                "Check network connectivity",
                "Review application logs for root cause",
                "Consider manual intervention",
            ],
        },
    }

    @classmethod
    def get_runbook(cls, issue: str) -> Optional[Dict[str, Any]]:
        """Get runbook for an issue."""
        return cls.RUNBOOK.get(issue)

    @classmethod
    def list_runbooks(cls) -> List[str]:
        """List available runbooks."""
        return list(cls.RUNBOOK.keys())

    @classmethod
    def print_guide(cls) -> str:
        """Print full operations guide."""
        guide = "# Production Operations Guide\n\n"
        for issue, details in cls.RUNBOOK.items():
            guide += f"## {issue.upper()}\n"
            guide += f"{details['description']}\n\n"
            guide += "### Steps\n"
            for step in details['steps']:
                guide += f"- {step}\n"
            guide += "\n"
        return guide
