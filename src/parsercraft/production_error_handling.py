"""
Production Error Handling and Recovery

Provides comprehensive error handling, retry logic, circuit breaker, and recovery mechanisms
for all Phase 5-6 integration modules.
"""

from __future__ import annotations

import time
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar
from functools import wraps

# Type variables
T = TypeVar('T')
E = TypeVar('E', bound=Exception)


# ============================================================================
# Error Classification
# ============================================================================


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification and handling."""
    VALIDATION = "validation"
    NETWORK = "network"
    TIMEOUT = "timeout"
    RESOURCE = "resource"
    INTERNAL = "internal"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    """Context information for errors."""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    timestamp: float
    context: Dict[str, Any]
    retry_count: int = 0
    last_error: Optional[Exception] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "error_id": self.error_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "message": self.message,
            "timestamp": self.timestamp,
            "retry_count": self.retry_count,
            "context": self.context,
        }


# ============================================================================
# Retry Logic with Exponential Backoff
# ============================================================================


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    initial_delay: float = 0.1  # seconds
    max_delay: float = 30.0  # seconds
    exponential_base: float = 2.0
    jitter: bool = True  # Add randomness to prevent thundering herd
    retryable_exceptions: Tuple[type, ...] = (
        ConnectionError,
        TimeoutError,
        OSError,
    )

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt."""
        delay = min(
            self.initial_delay * (self.exponential_base ** attempt),
            self.max_delay,
        )
        if self.jitter:
            import random
            delay *= random.uniform(0.8, 1.2)
        return delay


class RetryableError(Exception):
    """Wrapper for errors that should be retried."""
    def __init__(self, original_error: Exception, context: Optional[ErrorContext] = None):
        self.original_error = original_error
        self.context = context
        super().__init__(f"Retryable error: {original_error}")


def retry_with_backoff(config: Optional[RetryConfig] = None) -> Callable:
    """Decorator for automatic retry with exponential backoff."""
    cfg = config or RetryConfig()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_error = None
            for attempt in range(cfg.max_attempts):
                try:
                    return func(*args, **kwargs)
                except cfg.retryable_exceptions as e:
                    last_error = e
                    if attempt < cfg.max_attempts - 1:
                        delay = cfg.get_delay(attempt)
                        logging.warning(
                            f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}"
                        )
                        time.sleep(delay)
                    else:
                        logging.error(f"All {cfg.max_attempts} attempts failed")

            raise RetryableError(last_error)
        return wrapper
    return decorator


# ============================================================================
# Circuit Breaker Pattern
# ============================================================================


class CircuitBreakerState(Enum):
    """State of circuit breaker."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5  # Failures before opening
    recovery_timeout: float = 60.0  # Seconds before trying to recover
    expected_exceptions: Tuple[type, ...] = (Exception,)


class CircuitBreaker:
    """Circuit breaker for resilient operations."""

    def __init__(self, config: Optional[CircuitBreakerConfig] = None, name: str = "default"):
        self.config = config or CircuitBreakerConfig()
        self.name = name
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.success_count = 0

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with circuit breaker protection."""
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitBreakerState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception(f"Circuit breaker '{self.name}' is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.config.expected_exceptions as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        return (time.time() - self.last_failure_time) > self.config.recovery_timeout

    def _on_success(self) -> None:
        """Handle successful execution."""
        self.failure_count = 0
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 2:  # Need consecutive successes to close
                self.state = CircuitBreakerState.CLOSED
                logging.info(f"Circuit breaker '{self.name}' CLOSED (recovered)")

    def _on_failure(self) -> None:
        """Handle failed execution."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitBreakerState.OPEN
            logging.warning(f"Circuit breaker '{self.name}' OPEN (too many failures)")

    def get_state(self) -> Dict[str, Any]:
        """Get circuit breaker state."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time,
        }


# ============================================================================
# Rate Limiting
# ============================================================================


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""
    max_requests: int = 100
    window_seconds: float = 60.0
    burst_allowed: int = 10  # Allow temporary bursts


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self.tokens = self.config.max_requests
        self.last_refill = time.time()
        self.requests_in_window: List[float] = []

    def acquire(self, tokens: int = 1) -> bool:
        """Acquire tokens. Returns True if allowed."""
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            self.requests_in_window.append(time.time())
            return True

        return False

    def acquire_or_wait(self, tokens: int = 1, max_wait: float = 10.0) -> bool:
        """Try to acquire tokens, wait if necessary."""
        start_time = time.time()
        while time.time() - start_time < max_wait:
            if self.acquire(tokens):
                return True
            time.sleep(0.01)
        return False

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = (elapsed / self.config.window_seconds) * self.config.max_requests
        self.tokens = min(
            self.config.max_requests,
            self.tokens + refill_amount,
        )
        self.last_refill = now

        # Clean up old requests
        cutoff = now - self.config.window_seconds
        self.requests_in_window = [t for t in self.requests_in_window if t > cutoff]

    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics."""
        return {
            "available_tokens": self.tokens,
            "max_tokens": self.config.max_requests,
            "requests_in_window": len(self.requests_in_window),
            "refill_rate": self.config.max_requests / self.config.window_seconds,
        }


# ============================================================================
# Audit Logging
# ============================================================================


class AuditLogger:
    """Centralized audit logging for production operations."""

    def __init__(self, name: str = "audit"):
        self.logger = logging.getLogger(name)
        self.events: List[Dict[str, Any]] = []

    def log_event(
        self,
        event_type: str,
        action: str,
        resource: str,
        status: str,
        details: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        """Log an audit event."""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "action": action,
            "resource": resource,
            "status": status,
            "details": details or {},
            "error": error,
        }

        self.events.append(event)

        log_level = logging.ERROR if error else logging.INFO
        self.logger.log(
            log_level,
            f"[{event_type}] {action} {resource}: {status}" + (f" - {error}" if error else ""),
        )

    def get_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent audit events."""
        return self.events[-limit:]

    def clear_events(self) -> None:
        """Clear audit log."""
        self.events.clear()


# ============================================================================
# Unified Error Handler
# ============================================================================


class ProductionErrorHandler:
    """Unified error handling for production systems."""

    def __init__(self):
        self.audit_logger = AuditLogger("production")
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.error_contexts: List[ErrorContext] = []

    def register_circuit_breaker(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None,
    ) -> CircuitBreaker:
        """Register a circuit breaker."""
        cb = CircuitBreaker(config, name)
        self.circuit_breakers[name] = cb
        return cb

    def register_rate_limiter(
        self,
        name: str,
        config: Optional[RateLimitConfig] = None,
    ) -> RateLimiter:
        """Register a rate limiter."""
        rl = RateLimiter(config)
        self.rate_limiters[name] = rl
        return rl

    def handle_error(
        self,
        error: Exception,
        category: ErrorCategory,
        severity: ErrorSeverity,
        context: Optional[Dict[str, Any]] = None,
    ) -> ErrorContext:
        """Handle an error with full context."""
        import uuid
        error_id = f"err_{uuid.uuid4().hex[:8]}"
        error_ctx = ErrorContext(
            error_id=error_id,
            category=category,
            severity=severity,
            message=str(error),
            timestamp=time.time(),
            context=context or {},
            last_error=error,
        )

        self.error_contexts.append(error_ctx)

        self.audit_logger.log_event(
            event_type="error",
            action="handle_error",
            resource=category.value,
            status="logged",
            details={"error_id": error_id, "severity": severity.value},
            error=str(error),
        )

        return error_ctx

    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics."""
        return {
            "total_errors": len(self.error_contexts),
            "circuit_breakers": {
                name: cb.get_state() for name, cb in self.circuit_breakers.items()
            },
            "rate_limiters": {
                name: rl.get_stats() for name, rl in self.rate_limiters.items()
            },
        }

    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log."""
        return self.audit_logger.get_events(limit)
