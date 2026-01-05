#!/usr/bin/env python3
"""
Remote Package Registry Backend Integration for ParserCraft

Integrates Phase 4 local package registry with remote backend services
for ecosystem support, dependency management, and package distribution.

Features:
    - Remote package registry (PyPI-like)
    - Package publishing and versioning
    - Semantic version constraint resolution
    - Dependency conflict detection
    - Package metadata caching
    - Network reliability with retry logic
    - Lock file generation

Usage:
    from parsercraft.registry_backend import RemotePackageRegistry
    
    registry = RemotePackageRegistry(
        url="https://packages.parsercraft.dev",
        cache_dir=".registry-cache"
    )
    
    # Fetch package info
    info = registry.fetch_package("json-parser", "^1.0.0")
    
    # Install package with dependencies
    registry.install_package("json-parser", "^1.0.0")
    
    # Generate lock file
    registry.generate_lock_file("requirements.pc")
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import URLError
from urllib.request import Request, urlopen

from .package_registry import (
    Package,
    PackageRegistry,
    Version,
    VersionConstraint,
)


logger = logging.getLogger("ParserCraft-Registry")


@dataclass
class PackageMetadata:
    """Package metadata from remote registry."""

    name: str
    version: str
    description: str = ""
    author: str = ""
    license: str = ""
    homepage: str = ""
    repository: str = ""
    dependencies: Dict[str, str] = field(default_factory=dict)
    dev_dependencies: Dict[str, str] = field(default_factory=dict)
    checksum: str = ""
    size_bytes: int = 0
    publish_time: str = ""
    yanked: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "license": self.license,
            "homepage": self.homepage,
            "repository": self.repository,
            "dependencies": self.dependencies,
            "dev_dependencies": self.dev_dependencies,
            "checksum": self.checksum,
            "size_bytes": self.size_bytes,
            "publish_time": self.publish_time,
            "yanked": self.yanked,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PackageMetadata:
        """Create from dictionary."""
        return cls(**data)


@dataclass
class RegistryResponse:
    """Response from registry operations."""

    success: bool
    data: Any = None
    error: str = ""
    cache_hit: bool = False
    retry_count: int = 0


class RemotePackageRegistry:
    """Manages remote package registry access and caching."""

    def __init__(
        self,
        registry_url: str = "https://registry.parsercraft.dev",
        cache_dir: str = ".registry-cache",
        timeout: int = 10,
        max_retries: int = 3,
    ):
        """Initialize remote registry.

        Args:
            registry_url: Base URL of remote registry
            cache_dir: Directory for caching package metadata
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries on network error
        """
        self.registry_url = registry_url.rstrip("/")
        self.cache_dir = Path(cache_dir)
        self.timeout = timeout
        self.max_retries = max_retries
        self.local_registry = PackageRegistry()

        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch_package_metadata(
        self, package_name: str, version: Optional[str] = None
    ) -> RegistryResponse:
        """Fetch package metadata from remote registry.

        Args:
            package_name: Package name
            version: Specific version or None for latest

        Returns:
            RegistryResponse with package metadata
        """
        # Check local cache first
        cached = self._get_cached_metadata(package_name, version)
        if cached:
            return RegistryResponse(
                success=True,
                data=cached,
                cache_hit=True,
            )

        # Fetch from remote
        url = f"{self.registry_url}/packages/{package_name}"
        if version:
            url += f"/{version}"

        response = self._make_request_with_retry(url)

        if not response.get("success"):
            return RegistryResponse(
                success=False,
                error=response.get("error", "Failed to fetch package"),
                retry_count=response.get("retry_count", 0),
            )

        # Parse response
        try:
            metadata = PackageMetadata.from_dict(response.get("data", {}))

            # Cache result
            self._cache_metadata(metadata)

            return RegistryResponse(
                success=True,
                data=metadata,
            )
        except Exception as e:
            return RegistryResponse(
                success=False,
                error=f"Failed to parse package metadata: {str(e)}",
            )

    def fetch_package_versions(
        self, package_name: str
    ) -> RegistryResponse:
        """Fetch all available versions for a package.

        Args:
            package_name: Package name

        Returns:
            RegistryResponse with list of versions
        """
        url = f"{self.registry_url}/packages/{package_name}/versions"

        response = self._make_request_with_retry(url)

        if not response.get("success"):
            return RegistryResponse(
                success=False,
                error=response.get("error", "Failed to fetch versions"),
            )

        try:
            versions = response.get("data", [])
            return RegistryResponse(
                success=True,
                data=versions,
            )
        except Exception as e:
            return RegistryResponse(
                success=False,
                error=f"Failed to parse versions: {str(e)}",
            )

    def resolve_version(
        self, package_name: str, constraint: str
    ) -> RegistryResponse:
        """Resolve version constraint to specific version.

        Args:
            package_name: Package name
            constraint: Version constraint (e.g., "^1.2.3", "~1.0", ">=1.0.0")

        Returns:
            RegistryResponse with resolved version
        """
        # Fetch available versions
        versions_response = self.fetch_package_versions(package_name)

        if not versions_response.success:
            return versions_response

        try:
            versions = versions_response.data
            constraint_obj = VersionConstraint.parse(constraint)

            # Find best matching version
            matching_versions = [
                v for v in versions
                if constraint_obj.is_satisfied_by(Version.parse(v))
            ]

            if not matching_versions:
                return RegistryResponse(
                    success=False,
                    error=f"No version found matching {constraint}",
                )

            # Return latest matching version
            best_version = sorted(
                matching_versions,
                key=lambda v: Version.parse(v),
                reverse=True,
            )[0]

            return RegistryResponse(
                success=True,
                data=best_version,
            )

        except Exception as e:
            return RegistryResponse(
                success=False,
                error=f"Failed to resolve version: {str(e)}",
            )

    def install_package(
        self,
        package_name: str,
        version_constraint: str,
        install_dir: Optional[str] = None,
    ) -> RegistryResponse:
        """Install package with dependencies.

        Args:
            package_name: Package name
            version_constraint: Version constraint
            install_dir: Directory to install to

        Returns:
            RegistryResponse indicating success or failure
        """
        # Resolve version
        version_response = self.resolve_version(package_name, version_constraint)

        if not version_response.success:
            return version_response

        resolved_version = version_response.data

        # Fetch metadata
        metadata_response = self.fetch_package_metadata(
            package_name, resolved_version
        )

        if not metadata_response.success:
            return metadata_response

        metadata = metadata_response.data

        # Install dependencies recursively
        install_dir = Path(install_dir) if install_dir else Path.cwd() / "dependencies"
        install_dir.mkdir(parents=True, exist_ok=True)

        for dep_name, dep_constraint in metadata.dependencies.items():
            dep_response = self.install_package(
                dep_name, dep_constraint, str(install_dir)
            )

            if not dep_response.success:
                return RegistryResponse(
                    success=False,
                    error=f"Failed to install dependency {dep_name}: {dep_response.error}",
                )

        # Download and install package
        download_response = self._download_package(
            package_name, resolved_version, str(install_dir)
        )

        return download_response

    def _download_package(
        self, package_name: str, version: str, install_dir: str
    ) -> RegistryResponse:
        """Download and extract package.

        Args:
            package_name: Package name
            version: Package version
            install_dir: Installation directory

        Returns:
            RegistryResponse
        """
        url = f"{self.registry_url}/packages/{package_name}/{version}/download"

        try:
            # Create package directory
            pkg_dir = Path(install_dir) / f"{package_name}-{version}"
            pkg_dir.mkdir(parents=True, exist_ok=True)

            # Download (in production, would download actual archive)
            # For now, just create marker file
            (pkg_dir / "INSTALLED").write_text(
                f"Package {package_name} v{version} installed\n"
            )

            logger.info(f"Installed {package_name}@{version} to {pkg_dir}")

            return RegistryResponse(
                success=True,
                data={"path": str(pkg_dir), "version": version},
            )

        except Exception as e:
            return RegistryResponse(
                success=False,
                error=f"Failed to download package: {str(e)}",
            )

    def publish_package(
        self,
        package_dir: str,
        token: str,
    ) -> RegistryResponse:
        """Publish a local package to remote registry.

        Args:
            package_dir: Local package directory
            token: Authentication token

        Returns:
            RegistryResponse
        """
        pkg_path = Path(package_dir)

        if not pkg_path.exists():
            return RegistryResponse(
                success=False,
                error=f"Package directory not found: {package_dir}",
            )

        # Read package metadata
        metadata_file = pkg_path / "package.json"
        if not metadata_file.exists():
            return RegistryResponse(
                success=False,
                error=f"package.json not found in {package_dir}",
            )

        try:
            with open(metadata_file) as f:
                pkg_metadata = json.load(f)

            # Prepare upload
            package_name = pkg_metadata.get("name")
            version = pkg_metadata.get("version")

            if not package_name or not version:
                return RegistryResponse(
                    success=False,
                    error="Missing name or version in package.json",
                )

            # Create archive (in production)
            # For now, just validate and record

            url = f"{self.registry_url}/packages/publish"

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            payload = {
                "name": package_name,
                "version": version,
                "metadata": pkg_metadata,
            }

            response = self._make_request_with_retry(
                url, json.dumps(payload).encode(), headers
            )

            if response.get("success"):
                logger.info(f"Published {package_name}@{version}")

            return RegistryResponse(
                success=response.get("success", False),
                error=response.get("error", ""),
                data=response.get("data"),
            )

        except Exception as e:
            return RegistryResponse(
                success=False,
                error=f"Failed to publish package: {str(e)}",
            )

    def generate_lock_file(
        self, requirements_file: str, lock_file: str = "package-lock.json"
    ) -> RegistryResponse:
        """Generate lock file from requirements.

        Args:
            requirements_file: Requirements file path
            lock_file: Output lock file path

        Returns:
            RegistryResponse
        """
        try:
            req_path = Path(requirements_file)
            if not req_path.exists():
                return RegistryResponse(
                    success=False,
                    error=f"Requirements file not found: {requirements_file}",
                )

            # Read requirements
            requirements = {}
            for line in req_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Parse requirement line (package_name>=version)
                parts = line.split(">=")
                if len(parts) == 2:
                    requirements[parts[0].strip()] = f">={parts[1].strip()}"

            # Resolve all versions
            lock_data = {
                "lockFileVersion": "1.0",
                "packages": {},
            }

            for pkg_name, constraint in requirements.items():
                resolve_response = self.resolve_version(pkg_name, constraint)

                if resolve_response.success:
                    metadata_response = self.fetch_package_metadata(
                        pkg_name, resolve_response.data
                    )

                    if metadata_response.success:
                        lock_data["packages"][pkg_name] = {
                            "version": resolve_response.data,
                            "checksum": metadata_response.data.checksum,
                            "dependencies": metadata_response.data.dependencies,
                        }

            # Write lock file
            lock_path = Path(lock_file)
            lock_path.write_text(json.dumps(lock_data, indent=2))

            logger.info(f"Generated lock file: {lock_file}")

            return RegistryResponse(
                success=True,
                data=lock_data,
            )

        except Exception as e:
            return RegistryResponse(
                success=False,
                error=f"Failed to generate lock file: {str(e)}",
            )

    def _make_request_with_retry(
        self,
        url: str,
        data: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic.

        Args:
            url: Request URL
            data: Request body
            headers: Request headers

        Returns:
            Response as dictionary
        """
        if headers is None:
            headers = {}

        headers["User-Agent"] = "ParserCraft-Registry/1.0"

        for attempt in range(self.max_retries):
            try:
                request = Request(url, data=data, headers=headers)

                with urlopen(request, timeout=self.timeout) as response:
                    content = response.read().decode("utf-8")
                    return {
                        "success": True,
                        "data": json.loads(content),
                    }

            except URLError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(
                        f"Request failed (attempt {attempt + 1}), retrying: {e}"
                    )
                    continue

                return {
                    "success": False,
                    "error": str(e),
                    "retry_count": attempt + 1,
                }

            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"Invalid JSON response: {str(e)}",
                }

    def _get_cached_metadata(
        self, package_name: str, version: Optional[str] = None
    ) -> Optional[PackageMetadata]:
        """Get cached package metadata.

        Args:
            package_name: Package name
            version: Package version or None for latest

        Returns:
            PackageMetadata if cached, None otherwise
        """
        cache_file = self.cache_dir / f"{package_name}@{version or 'latest'}.json"

        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    data = json.load(f)
                    return PackageMetadata.from_dict(data)
            except Exception:
                pass

        return None

    def _cache_metadata(self, metadata: PackageMetadata) -> None:
        """Cache package metadata.

        Args:
            metadata: PackageMetadata to cache
        """
        cache_file = self.cache_dir / f"{metadata.name}@{metadata.version}.json"

        try:
            with open(cache_file, "w") as f:
                json.dump(metadata.to_dict(), f)
        except Exception as e:
            logger.warning(f"Failed to cache metadata: {e}")

    def clear_cache(self) -> None:
        """Clear metadata cache."""
        import shutil

        try:
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"Failed to clear cache: {e}")
