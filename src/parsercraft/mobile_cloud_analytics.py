#!/usr/bin/env python3
"""
Phase 9: Mobile Native Apps, Cloud Integration, and Advanced Analytics

This module provides mobile platform support, multi-cloud deployment capabilities,
and comprehensive analytics for the ParserCraft framework.

Features:
- Mobile platform packaging (iOS, Android, Web)
- Multi-cloud deployment (AWS, Azure, GCP)
- Event tracking and analytics
- Performance metrics and monitoring
- Distributed metrics aggregation
"""

import datetime as dt
import json
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class MobilePlatform(Enum):
    """Supported mobile platforms."""
    
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"
    PROGRESSIVE_WEB_APP = "pwa"


class CloudProvider(Enum):
    """Supported cloud providers."""
    
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    HEROKU = "heroku"
    DIGITAL_OCEAN = "digitalocean"


class MetricType(Enum):
    """Types of metrics that can be tracked."""
    
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class MobileAppConfig:
    """Configuration for mobile app packaging."""
    
    platform: MobilePlatform
    app_name: str
    bundle_id: str
    version: str
    min_sdk_version: Optional[str] = None
    target_sdk_version: Optional[str] = None
    permissions: List[str] = field(default_factory=list)
    icons: Dict[str, str] = field(default_factory=dict)
    splash_screens: Dict[str, str] = field(default_factory=dict)
    features: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "platform": self.platform.value,
            "app_name": self.app_name,
            "bundle_id": self.bundle_id,
            "version": self.version,
            "min_sdk_version": self.min_sdk_version,
            "target_sdk_version": self.target_sdk_version,
            "permissions": self.permissions,
            "icons": self.icons,
            "splash_screens": self.splash_screens,
            "features": self.features,
        }


@dataclass
class CloudDeploymentConfig:
    """Configuration for cloud deployment."""
    
    provider: CloudProvider
    region: str
    instance_type: str
    auto_scaling: bool = True
    min_instances: int = 1
    max_instances: int = 10
    health_check_path: str = "/health"
    environment_vars: Dict[str, str] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "provider": self.provider.value,
            "region": self.region,
            "instance_type": self.instance_type,
            "auto_scaling": self.auto_scaling,
            "min_instances": self.min_instances,
            "max_instances": self.max_instances,
            "health_check_path": self.health_check_path,
            "environment_vars": self.environment_vars,
            "tags": self.tags,
        }


@dataclass
class AnalyticsEvent:
    """An analytics event."""
    
    event_id: str
    event_type: str
    timestamp: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "properties": self.properties,
            "metrics": self.metrics,
        }


@dataclass
class PerformanceMetric:
    """A performance metric measurement."""
    
    metric_name: str
    metric_type: MetricType
    value: float
    timestamp: str
    tags: Dict[str, str] = field(default_factory=dict)
    unit: str = "ms"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_name": self.metric_name,
            "metric_type": self.metric_type.value,
            "value": self.value,
            "timestamp": self.timestamp,
            "tags": self.tags,
            "unit": self.unit,
        }


class MobilePlatformManager:
    """Manages mobile platform packaging and configuration."""
    
    def __init__(self) -> None:
        """Initialize the mobile platform manager."""
        self.configs: Dict[str, MobileAppConfig] = {}
        self.build_history: List[Dict[str, Any]] = []
    
    def create_mobile_config(
        self,
        platform: MobilePlatform,
        app_name: str,
        bundle_id: str,
        version: str = "1.0.0",
    ) -> MobileAppConfig:
        """Create a new mobile app configuration."""
        config = MobileAppConfig(
            platform=platform,
            app_name=app_name,
            bundle_id=bundle_id,
            version=version,
        )
        
        # Add platform-specific defaults
        if platform == MobilePlatform.IOS:
            config.min_sdk_version = "13.0"
            config.permissions = ["camera", "location"]
            config.features = ["push_notifications", "in_app_purchases"]
        elif platform == MobilePlatform.ANDROID:
            config.min_sdk_version = "21"
            config.target_sdk_version = "33"
            config.permissions = ["CAMERA", "ACCESS_FINE_LOCATION"]
            config.features = ["push_notifications", "in_app_billing"]
        elif platform in (MobilePlatform.WEB, MobilePlatform.PROGRESSIVE_WEB_APP):
            config.features = ["offline_mode", "push_notifications", "web_share"]
        
        self.configs[f"{platform.value}_{app_name}"] = config
        return config
    
    def package_app(self, config: MobileAppConfig) -> Dict[str, Any]:
        """Package an app for the specified platform."""
        build_id = f"build_{uuid.uuid4().hex[:8]}"
        timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
        
        # Simulate build process
        build_result = {
            "build_id": build_id,
            "platform": config.platform.value,
            "app_name": config.app_name,
            "version": config.version,
            "timestamp": timestamp,
            "status": "success",
            "artifacts": [],
        }
        
        # Platform-specific artifacts
        if config.platform == MobilePlatform.IOS:
            build_result["artifacts"] = [
                f"{config.app_name}.ipa",
                f"{config.app_name}.dSYM.zip",
            ]
        elif config.platform == MobilePlatform.ANDROID:
            build_result["artifacts"] = [
                f"{config.app_name}.apk",
                f"{config.app_name}-release.aab",
            ]
        elif config.platform == MobilePlatform.WEB:
            build_result["artifacts"] = [
                "index.html",
                "app.js",
                "styles.css",
                "manifest.json",
            ]
        elif config.platform == MobilePlatform.PROGRESSIVE_WEB_APP:
            build_result["artifacts"] = [
                "index.html",
                "app.js",
                "service-worker.js",
                "manifest.json",
            ]
        
        self.build_history.append(build_result)
        return build_result
    
    def get_supported_platforms(self) -> List[str]:
        """Get list of supported platforms."""
        return [platform.value for platform in MobilePlatform]


class CloudDeploymentManager:
    """Manages multi-cloud deployments."""
    
    def __init__(self) -> None:
        """Initialize the cloud deployment manager."""
        self.deployments: Dict[str, CloudDeploymentConfig] = {}
        self.deployment_history: List[Dict[str, Any]] = []
    
    def create_deployment_config(
        self,
        provider: CloudProvider,
        region: str,
        instance_type: str,
    ) -> CloudDeploymentConfig:
        """Create a new cloud deployment configuration."""
        config = CloudDeploymentConfig(
            provider=provider,
            region=region,
            instance_type=instance_type,
        )
        
        # Add provider-specific defaults
        if provider == CloudProvider.AWS:
            config.tags = {"ManagedBy": "ParserCraft", "Environment": "production"}
            if not config.environment_vars:
                config.environment_vars = {"AWS_REGION": region}
        elif provider == CloudProvider.AZURE:
            config.tags = {"managed-by": "parsercraft", "environment": "production"}
            if not config.environment_vars:
                config.environment_vars = {"AZURE_REGION": region}
        elif provider == CloudProvider.GCP:
            config.tags = {"managed_by": "parsercraft", "environment": "production"}
            if not config.environment_vars:
                config.environment_vars = {"GCP_REGION": region}
        
        deployment_key = f"{provider.value}_{region}"
        self.deployments[deployment_key] = config
        return config
    
    def deploy(
        self,
        config: CloudDeploymentConfig,
        app_name: str,
        version: str = "1.0.0",
    ) -> Dict[str, Any]:
        """Deploy an application to the cloud."""
        deployment_id = f"deploy_{uuid.uuid4().hex[:8]}"
        timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
        region = config.region
        
        # Simulate deployment
        deployment_result = {
            "deployment_id": deployment_id,
            "provider": config.provider.value,
            "region": region,
            "app_name": app_name,
            "version": version,
            "timestamp": timestamp,
            "status": "deployed",
            "endpoints": [],
            "resources": {},
        }
        
        # Provider-specific endpoints
        if config.provider == CloudProvider.AWS:
            deployment_result["endpoints"] = [
                f"https://{app_name}.{region}.elasticbeanstalk.com",
                f"https://{deployment_id}.execute-api.{region}.amazonaws.com",
            ]
            deployment_result["resources"] = {
                "ec2_instances": config.min_instances,
                "load_balancer": f"{app_name}-lb",
                "auto_scaling_group": f"{app_name}-asg",
            }
        elif config.provider == CloudProvider.AZURE:
            deployment_result["endpoints"] = [
                f"https://{app_name}.azurewebsites.net",
                f"https://{app_name}.{region}.cloudapp.azure.com",
            ]
            deployment_result["resources"] = {
                "app_service": f"{app_name}-app",
                "resource_group": f"{app_name}-rg",
                "app_service_plan": f"{app_name}-plan",
            }
        elif config.provider == CloudProvider.GCP:
            deployment_result["endpoints"] = [
                f"https://{app_name}.{region}.run.app",
                f"https://{app_name}-{deployment_id}.appspot.com",
            ]
            deployment_result["resources"] = {
                "cloud_run_service": f"{app_name}-service",
                "load_balancer": f"{app_name}-lb",
                "managed_instance_group": f"{app_name}-mig",
            }
        
        self.deployment_history.append(deployment_result)
        return deployment_result
    
    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get the status of a deployment."""
        deployment = next(
            (d for d in self.deployment_history if d["deployment_id"] == deployment_id),
            None,
        )
        
        if not deployment:
            return {"status": "not_found", "deployment_id": deployment_id}
        
        return {
            "deployment_id": deployment_id,
            "status": deployment["status"],
            "provider": deployment["provider"],
            "region": deployment["region"],
            "endpoints": deployment["endpoints"],
        }
    
    def get_supported_providers(self) -> List[str]:
        """Get list of supported cloud providers."""
        return [provider.value for provider in CloudProvider]


class AnalyticsTracker:
    """Tracks analytics events and metrics."""
    
    def __init__(self) -> None:
        """Initialize the analytics tracker."""
        self.events: List[AnalyticsEvent] = []
        self.metrics: List[PerformanceMetric] = []
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def track_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, float]] = None,
    ) -> AnalyticsEvent:
        """Track an analytics event."""
        event = AnalyticsEvent(
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            event_type=event_type,
            timestamp=dt.datetime.now(dt.timezone.utc).isoformat(),
            user_id=user_id,
            session_id=session_id,
            properties=properties or {},
            metrics=metrics or {},
        )
        
        self.events.append(event)
        return event
    
    def record_metric(
        self,
        metric_name: str,
        metric_type: MetricType,
        value: float,
        tags: Optional[Dict[str, str]] = None,
        unit: str = "ms",
    ) -> PerformanceMetric:
        """Record a performance metric."""
        metric = PerformanceMetric(
            metric_name=metric_name,
            metric_type=metric_type,
            value=value,
            timestamp=dt.datetime.now(dt.timezone.utc).isoformat(),
            tags=tags or {},
            unit=unit,
        )
        
        self.metrics.append(metric)
        return metric
    
    def start_session(self, user_id: str) -> str:
        """Start a new analytics session."""
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        self.sessions[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "start_time": dt.datetime.now(dt.timezone.utc).isoformat(),
            "events": [],
            "active": True,
        }
        return session_id
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End an analytics session."""
        if session_id not in self.sessions:
            return {"status": "not_found", "session_id": session_id}
        
        session = self.sessions[session_id]
        session["end_time"] = dt.datetime.now(dt.timezone.utc).isoformat()
        session["active"] = False
        
        # Calculate session metrics
        session_events = [e for e in self.events if e.session_id == session_id]
        session["event_count"] = len(session_events)
        session["events"] = [e.event_id for e in session_events]
        
        return session
    
    def get_analytics_report(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate an analytics report."""
        # Filter events by time range if provided
        filtered_events = self.events
        if start_time or end_time:
            filtered_events = [
                e for e in self.events
                if (not start_time or e.timestamp >= start_time)
                and (not end_time or e.timestamp <= end_time)
            ]
        
        # Count events by type
        event_counts = {}
        for event in filtered_events:
            event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1
        
        # Calculate metric statistics
        metric_stats = {}
        for metric in self.metrics:
            if metric.metric_name not in metric_stats:
                metric_stats[metric.metric_name] = {
                    "count": 0,
                    "sum": 0.0,
                    "min": float("inf"),
                    "max": float("-inf"),
                }
            
            stats = metric_stats[metric.metric_name]
            stats["count"] += 1
            stats["sum"] += metric.value
            stats["min"] = min(stats["min"], metric.value)
            stats["max"] = max(stats["max"], metric.value)
        
        # Calculate averages
        for stats in metric_stats.values():
            stats["avg"] = stats["sum"] / stats["count"] if stats["count"] > 0 else 0.0
        
        return {
            "total_events": len(filtered_events),
            "event_counts": event_counts,
            "unique_users": len(set(e.user_id for e in filtered_events if e.user_id)),
            "unique_sessions": len(set(e.session_id for e in filtered_events if e.session_id)),
            "metric_stats": metric_stats,
            "active_sessions": sum(1 for s in self.sessions.values() if s["active"]),
            "total_sessions": len(self.sessions),
        }


class DistributedMetricsAggregator:
    """Aggregates metrics from multiple sources/instances."""
    
    def __init__(self) -> None:
        """Initialize the distributed metrics aggregator."""
        self.sources: Dict[str, Dict[str, Any]] = {}
        self.aggregated_metrics: Dict[str, List[float]] = {}
    
    def register_source(
        self,
        source_id: str,
        source_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Register a new metrics source."""
        source = {
            "source_id": source_id,
            "source_type": source_type,
            "metadata": metadata or {},
            "registered_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "last_update": None,
            "metrics_count": 0,
        }
        
        self.sources[source_id] = source
        return source
    
    def ingest_metrics(
        self,
        source_id: str,
        metrics: List[PerformanceMetric],
    ) -> Dict[str, Any]:
        """Ingest metrics from a source."""
        if source_id not in self.sources:
            return {"status": "error", "message": "Source not registered"}
        
        # Update source metadata
        source = self.sources[source_id]
        source["last_update"] = dt.datetime.now(dt.timezone.utc).isoformat()
        source["metrics_count"] += len(metrics)
        
        # Aggregate metrics
        for metric in metrics:
            key = f"{metric.metric_name}_{metric.metric_type.value}"
            if key not in self.aggregated_metrics:
                self.aggregated_metrics[key] = []
            self.aggregated_metrics[key].append(metric.value)
        
        return {
            "status": "success",
            "source_id": source_id,
            "ingested_count": len(metrics),
        }
    
    def get_aggregated_stats(self, metric_name: str) -> Dict[str, Any]:
        """Get aggregated statistics for a metric."""
        # Find all keys for this metric name
        matching_keys = [k for k in self.aggregated_metrics if k.startswith(metric_name)]
        
        if not matching_keys:
            return {"status": "not_found", "metric_name": metric_name}
        
        stats = {}
        for key in matching_keys:
            values = self.aggregated_metrics[key]
            if values:
                stats[key] = {
                    "count": len(values),
                    "sum": sum(values),
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "p50": self._percentile(values, 50),
                    "p95": self._percentile(values, 95),
                    "p99": self._percentile(values, 99),
                }
        
        return {
            "status": "success",
            "metric_name": metric_name,
            "stats": stats,
        }
    
    def _percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile value."""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int(len(sorted_values) * (percentile / 100.0))
        index = min(index, len(sorted_values) - 1)
        return sorted_values[index]
    
    def get_source_health(self) -> Dict[str, Any]:
        """Get health status of all sources."""
        now = dt.datetime.now(dt.timezone.utc)
        healthy_sources = 0
        stale_sources = 0
        
        for source in self.sources.values():
            if source["last_update"] is None:
                continue
            
            last_update = dt.datetime.fromisoformat(source["last_update"])
            age_seconds = (now - last_update).total_seconds()
            
            if age_seconds < 60:  # Updated within last minute
                healthy_sources += 1
            elif age_seconds < 300:  # Updated within last 5 minutes
                stale_sources += 1
        
        return {
            "total_sources": len(self.sources),
            "healthy_sources": healthy_sources,
            "stale_sources": stale_sources,
            "inactive_sources": len(self.sources) - healthy_sources - stale_sources,
        }
