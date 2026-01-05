"""Phase 10 Enterprise Security and Collaboration tests."""

import unittest

from src.hb_lcs.enterprise_security import (
    AIAssistanceType,
    AICodeAssistant,
    CollaborationAction,
    ComplianceManager,
    EncryptionManager,
    Permission,
    RBACManager,
    RealtimeCollaborationManager,
    Role,
    SSOAuthenticationManager,
    SSOProvider,
    VulnerabilityLevel,
    VulnerabilityScanner,
)


class TestSSOAuthentication(unittest.TestCase):
    """Tests for SSO authentication."""

    def test_register_and_authenticate_okta(self) -> None:
        manager = SSOAuthenticationManager()
        
        config = manager.register_provider(
            provider=SSOProvider.OKTA,
            client_id="okta_client_123",
            client_secret="okta_secret_456",
            domain="company.okta.com",
            redirect_uri="https://app.example.com/callback",
        )
        
        assert config.provider == SSOProvider.OKTA
        assert config.client_id == "okta_client_123"
        assert config.domain == "company.okta.com"
        assert "openid" in config.scopes
        
        # Test authentication
        result = manager.authenticate(SSOProvider.OKTA, "auth_code_123")
        assert result["status"] == "success"
        assert "session_id" in result
        assert result["provider"] == "okta"

    def test_register_multiple_providers(self) -> None:
        manager = SSOAuthenticationManager()
        
        manager.register_provider(
            SSOProvider.AZURE_AD, "azure_client", "azure_secret",
            "tenant.onmicrosoft.com", "https://app.example.com/callback"
        )
        
        manager.register_provider(
            SSOProvider.GOOGLE, "google_client", "google_secret",
            "accounts.google.com", "https://app.example.com/callback"
        )
        
        assert SSOProvider.AZURE_AD in manager.providers
        assert SSOProvider.GOOGLE in manager.providers
        assert len(manager.providers) == 2

    def test_session_validation_and_logout(self) -> None:
        manager = SSOAuthenticationManager()
        manager.register_provider(
            SSOProvider.GITHUB, "gh_client", "gh_secret",
            "github.com", "https://app.example.com/callback"
        )
        
        result = manager.authenticate(SSOProvider.GITHUB, "code")
        session_id = result["session_id"]
        
        assert manager.validate_session(session_id) is True
        
        logout_result = manager.logout(session_id)
        assert logout_result["status"] == "success"
        assert manager.validate_session(session_id) is False

    def test_get_supported_providers(self) -> None:
        manager = SSOAuthenticationManager()
        providers = manager.get_supported_providers()
        
        assert "okta" in providers
        assert "azure_ad" in providers
        assert "google" in providers
        assert "github" in providers


class TestRBAC(unittest.TestCase):
    """Tests for Role-Based Access Control."""

    def test_create_user_with_roles(self) -> None:
        rbac = RBACManager()
        
        user = rbac.create_user(
            username="john_doe",
            email="john@example.com",
            roles={Role.DEVELOPER, Role.REVIEWER},
        )
        
        assert user.username == "john_doe"
        assert Role.DEVELOPER in user.roles
        assert Role.REVIEWER in user.roles
        assert len(rbac.audit_log) == 1

    def test_assign_and_revoke_roles(self) -> None:
        rbac = RBACManager()
        user = rbac.create_user("alice", "alice@example.com")
        
        result = rbac.assign_role(user.user_id, Role.ADMIN)
        assert result["status"] == "success"
        assert "admin" in result["roles"]
        
        result = rbac.revoke_role(user.user_id, Role.ADMIN)
        assert result["status"] == "success"
        assert "admin" not in result["roles"]

    def test_check_permissions(self) -> None:
        rbac = RBACManager()
        
        admin = rbac.create_user("admin_user", "admin@example.com", roles={Role.ADMIN})
        viewer = rbac.create_user("viewer_user", "viewer@example.com", roles={Role.VIEWER})
        
        assert rbac.check_permission(admin.user_id, Permission.MANAGE_USERS) is True
        assert rbac.check_permission(admin.user_id, Permission.DEPLOY) is True
        assert rbac.check_permission(viewer.user_id, Permission.READ_CONFIG) is True
        assert rbac.check_permission(viewer.user_id, Permission.DEPLOY) is False

    def test_mfa_enable_and_verify(self) -> None:
        rbac = RBACManager()
        user = rbac.create_user("mfa_user", "mfa@example.com")
        
        result = rbac.enable_mfa(user.user_id)
        assert result["status"] == "success"
        assert "mfa_secret" in result
        assert "qr_code_url" in result
        
        # Get user and verify MFA status
        stored_user = rbac.users[user.user_id]
        assert stored_user.mfa_enabled is True

    def test_audit_log(self) -> None:
        rbac = RBACManager()
        user = rbac.create_user("test_user", "test@example.com")
        rbac.assign_role(user.user_id, Role.DEVELOPER)
        rbac.enable_mfa(user.user_id)
        
        audit_log = rbac.get_audit_log()
        assert len(audit_log) >= 3
        assert audit_log[0]["action"] == "user_created"
        assert audit_log[1]["action"] == "role_assigned"


class TestVulnerabilityScanner(unittest.TestCase):
    """Tests for vulnerability scanning."""

    def test_scan_sql_injection(self) -> None:
        scanner = VulnerabilityScanner()
        
        code = '''
        query = "SELECT * FROM users WHERE id = " + user_input
        cursor.execute(query)
        '''
        
        vulns = scanner.scan_code(code, "test.py")
        assert len(vulns) > 0
        assert any(v.title == "Potential SQL Injection" for v in vulns)
        assert any(v.level == VulnerabilityLevel.HIGH for v in vulns)

    def test_scan_hardcoded_secrets(self) -> None:
        scanner = VulnerabilityScanner()
        
        code = '''
        api_key = "sk-1234567890abcdef"
        password = "my_secret_password"
        '''
        
        vulns = scanner.scan_code(code, "config.py")
        assert len(vulns) > 0
        assert any(v.title == "Hardcoded Secret" for v in vulns)
        assert any(v.level == VulnerabilityLevel.CRITICAL for v in vulns)

    def test_scan_command_injection(self) -> None:
        scanner = VulnerabilityScanner()
        
        code = '''
        import os
        os.system("rm -rf " + user_input)
        '''
        
        vulns = scanner.scan_code(code, "utils.py")
        assert len(vulns) > 0
        assert any(v.title == "Potential Command Injection" for v in vulns)

    def test_vulnerability_summary(self) -> None:
        scanner = VulnerabilityScanner()
        
        scanner.scan_code('api_key = "secret"', "file1.py")
        scanner.scan_code('os.system("cmd " + input)', "file2.py")
        
        summary = scanner.get_summary()
        assert summary["total_scans"] == 2
        assert summary["total_vulnerabilities"] >= 2
        assert "critical" in summary["by_level"]

    def test_get_vulnerabilities_by_level(self) -> None:
        scanner = VulnerabilityScanner()
        
        scanner.scan_code('password = "secret"', "file.py")
        
        critical_vulns = scanner.get_vulnerabilities_by_level(VulnerabilityLevel.CRITICAL)
        assert len(critical_vulns) > 0


class TestAICodeAssistant(unittest.TestCase):
    """Tests for AI code assistance."""

    def test_code_completion(self) -> None:
        assistant = AICodeAssistant()
        
        code = "def"
        suggestions = assistant.get_code_completion(code, len(code))
        
        assert len(suggestions) > 0
        assert any("def" in s for s in suggestions)

    def test_error_explanation(self) -> None:
        assistant = AICodeAssistant()
        
        explanation = assistant.explain_error("NameError: name 'x' is not defined")
        assert "NameError" in explanation
        assert "variable" in explanation.lower()

    def test_refactoring_suggestions(self) -> None:
        assistant = AICodeAssistant()
        
        long_code = "\n".join([f"line {i}" for i in range(60)])
        suggestions = assistant.suggest_refactoring(long_code)
        
        assert len(suggestions) > 0
        assert any(s["type"] == "function_length" for s in suggestions)

    def test_performance_optimization(self) -> None:
        assistant = AICodeAssistant()
        
        code = '''
        result = []
        for item in items:
            result.append(item * 2)
        '''
        
        optimizations = assistant.optimize_performance(code)
        assert len(optimizations) > 0
        assert any("comprehension" in o["type"] for o in optimizations)

    def test_security_analysis(self) -> None:
        assistant = AICodeAssistant()
        
        code = "result = eval(user_input)"
        issues = assistant.analyze_security(code)
        
        assert len(issues) > 0
        assert any(i["severity"] == "high" for i in issues)

    def test_documentation_generation(self) -> None:
        assistant = AICodeAssistant()
        
        code = '''
        def calculate(x, y):
            return x + y
        
        class Calculator:
            pass
        '''
        
        doc = assistant.generate_documentation(code)
        assert "Functions" in doc
        assert "Classes" in doc
        assert "calculate" in doc

    def test_assistance_stats(self) -> None:
        assistant = AICodeAssistant()
        
        assistant.get_code_completion("def", 3)
        assistant.explain_error("TypeError")
        assistant.analyze_security("eval(x)")
        
        stats = assistant.get_assistance_stats()
        assert stats["total_requests"] == 3
        assert stats["by_type"]["code_completion"] == 1


class TestRealtimeCollaboration(unittest.TestCase):
    """Tests for real-time collaboration."""

    def test_create_and_join_session(self) -> None:
        collab = RealtimeCollaborationManager(max_users=50)
        
        result = collab.create_session("Test Session", "user1")
        assert result["status"] == "success"
        session_id = result["session_id"]
        
        result = collab.join_session(session_id, "user2")
        assert result["status"] == "success"
        assert result["user_count"] == 2
        assert "color" in result

    def test_max_users_limit(self) -> None:
        collab = RealtimeCollaborationManager(max_users=2)
        
        result = collab.create_session("Limited Session", "user1")
        session_id = result["session_id"]
        
        collab.join_session(session_id, "user2")
        result = collab.join_session(session_id, "user3")
        
        assert result["status"] == "error"
        assert "full" in result["message"].lower()

    def test_cursor_update(self) -> None:
        collab = RealtimeCollaborationManager()
        
        result = collab.create_session("Cursor Test", "user1")
        session_id = result["session_id"]
        
        result = collab.update_cursor(session_id, "user1", line=10, column=5)
        assert result["status"] == "success"
        
        state = collab.get_session_state(session_id)
        session = collab.sessions[session_id]
        assert session["users"]["user1"]["cursor"]["line"] == 10

    def test_text_insert_and_delete(self) -> None:
        collab = RealtimeCollaborationManager()
        
        result = collab.create_session("Edit Test", "user1")
        session_id = result["session_id"]
        
        result = collab.insert_text(session_id, "user1", 0, "Hello World")
        assert result["status"] == "success"
        assert result["document_length"] == 11
        
        result = collab.delete_text(session_id, "user1", 0, 6)
        assert result["status"] == "success"
        assert result["document_length"] == 5

    def test_leave_session(self) -> None:
        collab = RealtimeCollaborationManager()
        
        result = collab.create_session("Leave Test", "user1")
        session_id = result["session_id"]
        
        collab.join_session(session_id, "user2")
        
        result = collab.leave_session(session_id, "user2")
        assert result["status"] == "success"
        
        state = collab.get_session_state(session_id)
        assert state["user_count"] == 1

    def test_session_cleanup(self) -> None:
        collab = RealtimeCollaborationManager()
        
        result = collab.create_session("Cleanup Test", "user1")
        session_id = result["session_id"]
        
        collab.leave_session(session_id, "user1")
        
        # Session should be deleted when last user leaves
        assert session_id not in collab.sessions


class TestEncryption(unittest.TestCase):
    """Tests for encryption and security."""

    def test_encrypt_and_decrypt(self) -> None:
        manager = EncryptionManager()
        
        data = "sensitive information"
        encrypted, key = manager.encrypt_data(data)
        
        assert encrypted != data
        assert len(key) == 64  # 32 bytes in hex
        
        decrypted = manager.decrypt_data(encrypted, key)
        assert decrypted is not None

    def test_password_hashing(self) -> None:
        manager = EncryptionManager()
        
        password = "secure_password_123"
        hashed = manager.hash_password(password)
        
        assert hashed != password
        assert "$" in hashed  # Salt separator
        
        assert manager.verify_password(password, hashed) is True
        assert manager.verify_password("wrong_password", hashed) is False

    def test_tls_config(self) -> None:
        manager = EncryptionManager()
        
        config = manager.get_tls_config()
        assert config["version"] == "TLS 1.3"
        assert config["cipher_suite"] == "AES-256-GCM"
        assert "TLSv1.3" in config["protocols"]


class TestCompliance(unittest.TestCase):
    """Tests for compliance management."""

    def test_run_compliance_check(self) -> None:
        manager = ComplianceManager()
        
        result = manager.run_compliance_check("SOC2")
        assert result["framework"] == "SOC2"
        assert "controls_passed" in result
        assert "compliance_percentage" in result
        assert result["status"] in ["pass", "fail"]

    def test_enable_framework(self) -> None:
        manager = ComplianceManager()
        
        result = manager.enable_framework("HIPAA")
        assert result["status"] == "success"
        assert result["framework"] == "HIPAA"

    def test_get_supported_frameworks(self) -> None:
        manager = ComplianceManager()
        
        frameworks = manager.get_supported_frameworks()
        assert "SOC2" in frameworks
        assert "ISO27001" in frameworks
        assert "GDPR" in frameworks
        assert "HIPAA" in frameworks

    def test_compliance_status(self) -> None:
        manager = ComplianceManager()
        
        manager.run_compliance_check("SOC2")
        manager.run_compliance_check("GDPR")
        
        status = manager.get_compliance_status()
        assert "enabled_frameworks" in status
        assert "recent_checks" in status
        assert status["total_checks_run"] >= 2


if __name__ == "__main__":
    unittest.main()
