"""Type system — types, generics, protocols, type checking."""

from .type_system import Type, TypeKind, TypeChecker, TypeEnvironment
from .protocols import Protocol, ProtocolChecker
from .generics import GenericType, TypeParameter, GenericChecker

__all__ = [
    "Type",
    "TypeKind",
    "TypeChecker",
    "TypeEnvironment",
    "Protocol",
    "ProtocolChecker",
    "GenericType",
    "TypeParameter",
    "GenericChecker",
]
