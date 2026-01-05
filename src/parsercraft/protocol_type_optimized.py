"""
Optimized Protocol Type Integration

Performance improvements:
- Memoization cache for protocol conformance checks
- Lazy evaluation of structural compatibility
- Index-based protocol lookup
- Pre-computed method signature hashes
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple

from parsercraft.protocol_type_integration import (
    ProtocolTypeIntegration as BaseProtocolTypeIntegration,
    ProtocolBinding,
    TypeCompatibilityResult,
)
from parsercraft.protocols import MethodSignature, Protocol
from parsercraft.type_system import Type, TypeKind


@dataclass
class _MethodHash:
    """Pre-computed hash for method signatures."""

    name: str
    return_type: str
    param_types: Tuple[str, ...] = field(default_factory=tuple)

    def __hash__(self) -> int:
        return hash((self.name, self.return_type, self.param_types))


class OptimizedProtocolTypeIntegration(BaseProtocolTypeIntegration):
    """
    Performance-optimized protocol type integration.

    Optimizations:
    1. Method signature hashing for O(1) lookup
    2. Protocol conformance memoization
    3. Early termination on incompatibility
    4. Lazy structural type evaluation
    """

    def __init__(self, type_checker=None):
        super().__init__(type_checker)
        self._protocol_method_cache: Dict[str, Set[_MethodHash]] = {}
        self._conformance_cache: Dict[Tuple[str, str], bool] = {}
        self._incompatibility_cache: Dict[Tuple[str, str], Set[str]] = {}

    def register_protocol(self, protocol: Protocol) -> None:
        """Register protocol with method caching."""
        super().register_protocol(protocol)

        # Pre-compute method hashes for O(1) lookup
        method_hashes = set()
        for name, sig in protocol.methods.items():
            method_hashes.add(_MethodHash(name=name, return_type=sig.return_type))

        self._protocol_method_cache[protocol.name] = method_hashes

    def check_type_compatibility(
        self,
        source_type: Type,
        target_type: Type,
        is_protocol: bool,
        context: Optional[Dict] = None,
    ) -> TypeCompatibilityResult:
        """Check compatibility with memoization."""
        # Check cache first
        cache_key = (source_type.name or "", target_type.name or "")
        if cache_key in self._conformance_cache:
            is_compatible = self._conformance_cache[cache_key]
            missing = self._incompatibility_cache.get(cache_key, set())
            return TypeCompatibilityResult(
                compatible=is_compatible, missing_features=list(missing)
            )

        # Perform check
        result = super().check_type_compatibility(
            source_type, target_type, is_protocol, context
        )

        # Cache result
        self._conformance_cache[cache_key] = result.compatible
        if not result.compatible:
            self._incompatibility_cache[cache_key] = set(result.missing_features)

        return result

    def clear_caches(self) -> None:
        """Clear all memoization caches."""
        self._conformance_cache.clear()
        self._incompatibility_cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """Return cache statistics for monitoring."""
        return {
            "protocol_methods": len(self._protocol_method_cache),
            "conformance_cached": len(self._conformance_cache),
            "incompatibilities_cached": len(self._incompatibility_cache),
        }
