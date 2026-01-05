"""Phase 9 Mobile, Cloud, and Analytics tests."""

import unittest
from datetime import datetime, timezone

from src.hb_lcs.mobile_cloud_analytics import (
    AnalyticsTracker,
    CloudDeploymentManager,
    CloudProvider,
    DistributedMetricsAggregator,
    MetricType,
    MobilePlatform,
    MobilePlatformManager,
    PerformanceMetric,
)


class TestMobilePlatformManager(unittest.TestCase):
    """Tests for mobile platform management."""

    def test_create_and_package_ios_app(self) -> None:
        manager = MobilePlatformManager()
        config = manager.create_mobile_config(
            platform=MobilePlatform.IOS,
            app_name="TestApp",
            bundle_id="com.example.testapp",
            version="1.0.0",
        )

        assert config.platform == MobilePlatform.IOS
        assert config.app_name == "TestApp"
        assert config.min_sdk_version == "13.0"
        assert "camera" in config.permissions
        assert "push_notifications" in config.features

        build_result = manager.package_app(config)
        assert build_result["status"] == "success"
        assert "TestApp.ipa" in build_result["artifacts"]
        assert len(manager.build_history) == 1

    def test_create_and_package_android_app(self) -> None:
        manager = MobilePlatformManager()
        config = manager.create_mobile_config(
            platform=MobilePlatform.ANDROID,
            app_name="AndroidApp",
            bundle_id="com.example.androidapp",
        )

        assert config.platform == MobilePlatform.ANDROID
        assert config.min_sdk_version == "21"
        assert config.target_sdk_version == "33"
        assert "CAMERA" in config.permissions

        build_result = manager.package_app(config)
        assert build_result["status"] == "success"
        assert "AndroidApp.apk" in build_result["artifacts"]
        assert "AndroidApp-release.aab" in build_result["artifacts"]

    def test_create_progressive_web_app(self) -> None:
        manager = MobilePlatformManager()
        config = manager.create_mobile_config(
            platform=MobilePlatform.PROGRESSIVE_WEB_APP,
            app_name="PWA_App",
            bundle_id="com.example.pwa",
        )

        assert config.platform == MobilePlatform.PROGRESSIVE_WEB_APP
        assert "offline_mode" in config.features
        assert "web_share" in config.features

        build_result = manager.package_app(config)
        assert "service-worker.js" in build_result["artifacts"]
        assert "manifest.json" in build_result["artifacts"]

    def test_get_supported_platforms(self) -> None:
        manager = MobilePlatformManager()
        platforms = manager.get_supported_platforms()

        assert "ios" in platforms
        assert "android" in platforms
        assert "web" in platforms
        assert "pwa" in platforms


class TestCloudDeploymentManager(unittest.TestCase):
    """Tests for cloud deployment management."""

    def test_deploy_to_aws(self) -> None:
        manager = CloudDeploymentManager()
        config = manager.create_deployment_config(
            provider=CloudProvider.AWS,
            region="us-east-1",
            instance_type="t3.medium",
        )

        assert config.provider == CloudProvider.AWS
        assert config.region == "us-east-1"
        assert config.auto_scaling is True
        assert "AWS_REGION" in config.environment_vars

        deployment = manager.deploy(config, app_name="test-app", version="1.0.0")
        assert deployment["status"] == "deployed"
        assert deployment["provider"] == "aws"
        assert "elasticbeanstalk.com" in deployment["endpoints"][0]
        assert "ec2_instances" in deployment["resources"]

    def test_deploy_to_azure(self) -> None:
        manager = CloudDeploymentManager()
        config = manager.create_deployment_config(
            provider=CloudProvider.AZURE,
            region="eastus",
            instance_type="Standard_B2s",
        )

        assert config.provider == CloudProvider.AZURE
        assert "AZURE_REGION" in config.environment_vars

        deployment = manager.deploy(config, app_name="azure-app")
        assert deployment["status"] == "deployed"
        assert "azurewebsites.net" in deployment["endpoints"][0]
        assert "app_service" in deployment["resources"]

    def test_deploy_to_gcp(self) -> None:
        manager = CloudDeploymentManager()
        config = manager.create_deployment_config(
            provider=CloudProvider.GCP,
            region="us-central1",
            instance_type="e2-medium",
        )

        deployment = manager.deploy(config, app_name="gcp-app")
        assert deployment["status"] == "deployed"
        assert "run.app" in deployment["endpoints"][0]
        assert "cloud_run_service" in deployment["resources"]

    def test_get_deployment_status(self) -> None:
        manager = CloudDeploymentManager()
        config = manager.create_deployment_config(
            provider=CloudProvider.AWS,
            region="us-west-2",
            instance_type="t3.small",
        )

        deployment = manager.deploy(config, app_name="status-test")
        deployment_id = deployment["deployment_id"]

        status = manager.get_deployment_status(deployment_id)
        assert status["status"] == "deployed"
        assert status["deployment_id"] == deployment_id
        assert status["provider"] == "aws"

    def test_get_supported_providers(self) -> None:
        manager = CloudDeploymentManager()
        providers = manager.get_supported_providers()

        assert "aws" in providers
        assert "azure" in providers
        assert "gcp" in providers


class TestAnalyticsTracker(unittest.TestCase):
    """Tests for analytics tracking."""

    def test_track_event(self) -> None:
        tracker = AnalyticsTracker()
        event = tracker.track_event(
            event_type="page_view",
            user_id="user123",
            properties={"page": "/home", "referrer": "/landing"},
            metrics={"load_time": 1.5},
        )

        assert event.event_type == "page_view"
        assert event.user_id == "user123"
        assert event.properties["page"] == "/home"
        assert event.metrics["load_time"] == 1.5
        assert len(tracker.events) == 1

    def test_record_metric(self) -> None:
        tracker = AnalyticsTracker()
        metric = tracker.record_metric(
            metric_name="response_time",
            metric_type=MetricType.TIMER,
            value=125.5,
            tags={"endpoint": "/api/users", "method": "GET"},
            unit="ms",
        )

        assert metric.metric_name == "response_time"
        assert metric.metric_type == MetricType.TIMER
        assert metric.value == 125.5
        assert metric.tags["endpoint"] == "/api/users"
        assert len(tracker.metrics) == 1

    def test_session_management(self) -> None:
        tracker = AnalyticsTracker()
        session_id = tracker.start_session(user_id="user456")

        assert session_id in tracker.sessions
        assert tracker.sessions[session_id]["active"] is True
        assert tracker.sessions[session_id]["user_id"] == "user456"

        # Track some events in the session
        tracker.track_event("login", user_id="user456", session_id=session_id)
        tracker.track_event("page_view", user_id="user456", session_id=session_id)

        session = tracker.end_session(session_id)
        assert session["active"] is False
        assert session["event_count"] == 2
        assert len(session["events"]) == 2

    def test_analytics_report(self) -> None:
        tracker = AnalyticsTracker()

        # Track multiple events
        tracker.track_event("login", user_id="user1")
        tracker.track_event("page_view", user_id="user1")
        tracker.track_event("login", user_id="user2")
        tracker.track_event("purchase", user_id="user1")

        # Record metrics
        tracker.record_metric("api_latency", MetricType.TIMER, 100.0)
        tracker.record_metric("api_latency", MetricType.TIMER, 150.0)
        tracker.record_metric("api_latency", MetricType.TIMER, 200.0)

        report = tracker.get_analytics_report()
        assert report["total_events"] == 4
        assert report["event_counts"]["login"] == 2
        assert report["event_counts"]["page_view"] == 1
        assert report["event_counts"]["purchase"] == 1
        assert report["unique_users"] == 2

        # Check metric stats
        stats = report["metric_stats"]["api_latency"]
        assert stats["count"] == 3
        assert stats["avg"] == 150.0
        assert stats["min"] == 100.0
        assert stats["max"] == 200.0


class TestDistributedMetricsAggregator(unittest.TestCase):
    """Tests for distributed metrics aggregation."""

    def test_register_source(self) -> None:
        aggregator = DistributedMetricsAggregator()
        source = aggregator.register_source(
            source_id="server1",
            source_type="web_server",
            metadata={"region": "us-east-1", "instance_type": "t3.medium"},
        )

        assert source["source_id"] == "server1"
        assert source["source_type"] == "web_server"
        assert source["metadata"]["region"] == "us-east-1"
        assert "server1" in aggregator.sources

    def test_ingest_and_aggregate_metrics(self) -> None:
        aggregator = DistributedMetricsAggregator()
        aggregator.register_source("server1", "web_server")
        aggregator.register_source("server2", "web_server")

        # Ingest metrics from server1
        metrics1 = [
            PerformanceMetric(
                metric_name="cpu_usage",
                metric_type=MetricType.GAUGE,
                value=45.0,
                timestamp=datetime.now(timezone.utc).isoformat(),
                unit="%",
            ),
            PerformanceMetric(
                metric_name="memory_usage",
                metric_type=MetricType.GAUGE,
                value=60.0,
                timestamp=datetime.now(timezone.utc).isoformat(),
                unit="%",
            ),
        ]

        result1 = aggregator.ingest_metrics("server1", metrics1)
        assert result1["status"] == "success"
        assert result1["ingested_count"] == 2

        # Ingest metrics from server2
        metrics2 = [
            PerformanceMetric(
                metric_name="cpu_usage",
                metric_type=MetricType.GAUGE,
                value=55.0,
                timestamp=datetime.now(timezone.utc).isoformat(),
                unit="%",
            ),
        ]

        result2 = aggregator.ingest_metrics("server2", metrics2)
        assert result2["status"] == "success"

        # Check aggregated stats
        stats = aggregator.get_aggregated_stats("cpu_usage")
        assert stats["status"] == "success"
        assert "cpu_usage_gauge" in stats["stats"]
        cpu_stats = stats["stats"]["cpu_usage_gauge"]
        assert cpu_stats["count"] == 2
        assert cpu_stats["avg"] == 50.0
        assert cpu_stats["min"] == 45.0
        assert cpu_stats["max"] == 55.0

    def test_source_health_monitoring(self) -> None:
        aggregator = DistributedMetricsAggregator()
        aggregator.register_source("server1", "web_server")
        aggregator.register_source("server2", "web_server")
        aggregator.register_source("server3", "web_server")

        # Ingest metrics from server1 and server2
        metric = PerformanceMetric(
            metric_name="test_metric",
            metric_type=MetricType.COUNTER,
            value=1.0,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        aggregator.ingest_metrics("server1", [metric])
        aggregator.ingest_metrics("server2", [metric])

        health = aggregator.get_source_health()
        assert health["total_sources"] == 3
        assert health["healthy_sources"] == 2
        assert health["inactive_sources"] == 1


if __name__ == "__main__":
    unittest.main()
