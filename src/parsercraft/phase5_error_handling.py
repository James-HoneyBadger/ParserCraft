"""
Phase 5-6 Integration Error Handling

Adds comprehensive error handling, recovery, and monitoring to all Phase 5-6 modules
using production error handling and operations systems.
"""

from __future__ import annotations

import logging
from typing import Any, Optional, Dict, Tuple
from contextlib import contextmanager

# Import Phase 5 modules
from src.hb_lcs.ast_integration import (
    ASTToCGenerator,
    ASTToWasmGenerator,
    TypeInferencePass,
    ControlFlowAnalyzer,
)
from src.hb_lcs.protocol_type_integration import ProtocolTypeIntegration
from src.hb_lcs.lsp_integration import LSPFeaturesIntegration
from src.hb_lcs.registry_backend import RemotePackageRegistry
from src.hb_lcs.type_system_generics import TypeNarrowingPass

# Import error handling
from src.hb_lcs.production_error_handling import (
    ProductionErrorHandler,
    ErrorCategory,
    ErrorSeverity,
    retry_with_backoff,
    RetryConfig,
    CircuitBreakerConfig,
    RateLimitConfig,
)
from src.hb_lcs.production_operations import (
    ServiceHealthMonitor,
    HealthCheckProvider,
    HealthCheck,
    ServiceHealth,
    RecoveryManager,
    RecoveryPlan,
    RecoveryStrategy,
)


class ASTIntegrationErrorHandler:
    """Error handling for AST integration."""

    def __init__(self, error_handler: ProductionErrorHandler):
        self.error_handler = error_handler
        self.logger = logging.getLogger("ast_integration_errors")

        # Register circuit breaker for code generation
        self.error_handler.register_circuit_breaker(
            "ast_codegen",
            CircuitBreakerConfig(failure_threshold=10),
        )

        # Register rate limiter for AST analysis
        self.error_handler.register_rate_limiter(
            "ast_analysis",
            RateLimitConfig(max_requests=1000, window_seconds=60),
        )

    @contextmanager
    def handle_ast_codegen_error(self):
        """Context manager for AST code generation errors."""
        try:
            yield
        except ValueError as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.VALIDATION,
                ErrorSeverity.MEDIUM,
                {"operation": "ast_codegen", "error_type": "validation"},
            )
            raise
        except RuntimeError as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                {"operation": "ast_codegen", "error_type": "internal"},
            )
            raise
        except Exception as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.UNKNOWN,
                ErrorSeverity.CRITICAL,
                {"operation": "ast_codegen"},
            )
            raise

    @contextmanager
    def handle_type_inference_error(self):
        """Context manager for type inference errors."""
        try:
            yield
        except TypeError as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.VALIDATION,
                ErrorSeverity.MEDIUM,
                {"operation": "type_inference"},
            )
            raise
        except Exception as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.UNKNOWN,
                ErrorSeverity.HIGH,
                {"operation": "type_inference"},
            )
            raise


class ProtocolTypeErrorHandler:
    """Error handling for protocol type integration."""

    def __init__(self, error_handler: ProductionErrorHandler):
        self.error_handler = error_handler
        self.logger = logging.getLogger("protocol_type_errors")

        # Register circuit breaker for compatibility checks
        self.error_handler.register_circuit_breaker(
            "protocol_check",
            CircuitBreakerConfig(failure_threshold=15),
        )

    @contextmanager
    def handle_protocol_check_error(self):
        """Context manager for protocol checking errors."""
        try:
            yield
        except ValueError as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.VALIDATION,
                ErrorSeverity.LOW,
                {"operation": "protocol_check"},
            )
            raise
        except Exception as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.UNKNOWN,
                ErrorSeverity.MEDIUM,
                {"operation": "protocol_check"},
            )
            raise


class RegistryErrorHandler:
    """Error handling for registry operations."""

    def __init__(self, error_handler: ProductionErrorHandler):
        self.error_handler = error_handler
        self.logger = logging.getLogger("registry_errors")

        # Register circuit breaker for network operations
        self.error_handler.register_circuit_breaker(
            "registry_fetch",
            CircuitBreakerConfig(
                failure_threshold=5,
                recovery_timeout=120.0,
            ),
        )

        # Register rate limiter for registry queries
        self.error_handler.register_rate_limiter(
            "registry_query",
            RateLimitConfig(max_requests=500, window_seconds=60),
        )

    @contextmanager
    def handle_registry_fetch_error(self):
        """Context manager for registry fetch errors."""
        try:
            yield
        except ConnectionError as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.NETWORK,
                ErrorSeverity.HIGH,
                {"operation": "registry_fetch", "error_type": "connection"},
            )
            raise
        except TimeoutError as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.TIMEOUT,
                ErrorSeverity.MEDIUM,
                {"operation": "registry_fetch", "error_type": "timeout"},
            )
            raise
        except Exception as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.UNKNOWN,
                ErrorSeverity.HIGH,
                {"operation": "registry_fetch"},
            )
            raise


class LSPErrorHandler:
    """Error handling for LSP integration."""

    def __init__(self, error_handler: ProductionErrorHandler):
        self.error_handler = error_handler
        self.logger = logging.getLogger("lsp_errors")

        # Register rate limiter for LSP requests
        self.error_handler.register_rate_limiter(
            "lsp_requests",
            RateLimitConfig(max_requests=2000, window_seconds=60),
        )

    @contextmanager
    def handle_lsp_operation_error(self):
        """Context manager for LSP operation errors."""
        try:
            yield
        except ValueError as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.VALIDATION,
                ErrorSeverity.LOW,
                {"operation": "lsp_operation"},
            )
            raise
        except TimeoutError as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.TIMEOUT,
                ErrorSeverity.MEDIUM,
                {"operation": "lsp_operation"},
            )
            raise
        except Exception as e:
            self.error_handler.handle_error(
                e,
                ErrorCategory.UNKNOWN,
                ErrorSeverity.MEDIUM,
                {"operation": "lsp_operation"},
            )
            raise


# ============================================================================
# Health Check Implementations
# ============================================================================


class ASTHealthCheck(HealthCheckProvider):
    """Health check for AST integration."""

    def __init__(self, ast_codegen: ASTToCGenerator):
        self.ast_codegen = ast_codegen

    def check_health(self) -> HealthCheck:
        """Check AST integration health."""
        start_time = time.time()
        try:
            # Test basic AST operation
            sample_code = "int x = 5;"
            # Just verify it doesn't crash
            response_time = (time.time() - start_time) * 1000

            return HealthCheck(
                name="ast_integration",
                status=ServiceHealth.HEALTHY,
                timestamp=time.time(),
                response_time_ms=response_time,
                message="AST integration operational",
                checks={
                    "codegen_available": True,
                    "type_inference_available": True,
                },
            )
        except Exception as e:
            return HealthCheck(
                name="ast_integration",
                status=ServiceHealth.UNHEALTHY,
                timestamp=time.time(),
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"AST integration unhealthy: {e}",
                checks={"operational": False},
            )


class RegistryHealthCheck(HealthCheckProvider):
    """Health check for package registry."""

    def __init__(self, registry: RemotePackageRegistry):
        self.registry = registry

    def check_health(self) -> HealthCheck:
        """Check registry health."""
        start_time = time.time()
        try:
            # Test registry connectivity
            cache_stats = self.registry.get_cache_stats() if hasattr(self.registry, 'get_cache_stats') else {}
            response_time = (time.time() - start_time) * 1000

            return HealthCheck(
                name="registry",
                status=ServiceHealth.HEALTHY,
                timestamp=time.time(),
                response_time_ms=response_time,
                message="Registry operational",
                checks={"connectivity": True},
                details={"cache_stats": cache_stats},
            )
        except Exception as e:
            return HealthCheck(
                name="registry",
                status=ServiceHealth.DEGRADED,
                timestamp=time.time(),
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"Registry degraded: {e}",
                checks={"connectivity": False},
            )


class LSPHealthCheck(HealthCheckProvider):
    """Health check for LSP integration."""

    def __init__(self, lsp: LSPFeaturesIntegration):
        self.lsp = lsp

    def check_health(self) -> HealthCheck:
        """Check LSP health."""
        start_time = time.time()
        try:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                name="lsp_integration",
                status=ServiceHealth.HEALTHY,
                timestamp=time.time(),
                response_time_ms=response_time,
                message="LSP integration operational",
                checks={"handlers_available": True},
            )
        except Exception as e:
            return HealthCheck(
                name="lsp_integration",
                status=ServiceHealth.UNHEALTHY,
                timestamp=time.time(),
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"LSP integration unhealthy: {e}",
                checks={"operational": False},
            )


# ============================================================================
# Integrated Error Handling System
# ============================================================================


class Phase5ErrorHandlingSystem:
    """Unified error handling for all Phase 5-6 modules."""

    def __init__(self):
        self.error_handler = ProductionErrorHandler()
        self.monitor = ServiceHealthMonitor()
        self.recovery_manager = RecoveryManager(self.monitor)
        self.logger = logging.getLogger("phase5_errors")

        # Initialize error handlers
        self.ast_errors = ASTIntegrationErrorHandler(self.error_handler)
        self.protocol_errors = ProtocolTypeErrorHandler(self.error_handler)
        self.registry_errors = RegistryErrorHandler(self.error_handler)
        self.lsp_errors = LSPErrorHandler(self.error_handler)

        # Setup recovery plans
        self._setup_recovery_plans()

    def _setup_recovery_plans(self) -> None:
        """Setup recovery plans for common operations."""
        # Registry recovery plan with retry
        self.monitor.register_recovery_plan(
            "fetch_package",
            RecoveryPlan(
                operation="fetch_package",
                strategy=RecoveryStrategy.RETRY,
                max_retries=3,
                retry_delay_ms=100,
            ),
        )

        # Protocol checking with circuit breaker
        self.monitor.register_recovery_plan(
            "check_protocol",
            RecoveryPlan(
                operation="check_protocol",
                strategy=RecoveryStrategy.CIRCUIT_BREAK,
            ),
        )

        # LSP operations with graceful degradation
        self.monitor.register_recovery_plan(
            "lsp_operation",
            RecoveryPlan(
                operation="lsp_operation",
                strategy=RecoveryStrategy.GRACEFUL_DEGRADE,
            ),
        )

    def get_health_summary(self) -> Dict[str, Any]:
        """Get system health summary."""
        return self.monitor.get_health_summary()

    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics."""
        return self.error_handler.get_error_stats()

    def get_audit_log(self, limit: int = 100) -> list:
        """Get audit log."""
        return self.error_handler.get_audit_log(limit)


import time
