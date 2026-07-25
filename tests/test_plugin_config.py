from __future__ import annotations

import pytest

from kyvernex.plugin_config import PluginConfiguration, PluginConfigurationError
from kyvernex.plugin_runtime import KyvernexPluginRuntime


class Adapter:
    adapter_id = "test.adapter"
    adapter_version = "1.0.0"
    def capabilities(self):
        return {"governed.execute", "filesystem.read", "network.access", "process.execute"}
    def invoke(self, request, authority):
        return {"authority": authority}
    def health(self):
        return {"status": "HEALTHY"}
    def shutdown(self):
        return None


def test_defaults_grant_zero_authority():
    config = PluginConfiguration.load({})
    authority = dict(config.authority_summary())
    assert config.allowed_capabilities == ()
    assert authority["filesystem"] == {"read_roots": (), "write_roots": ()}
    assert authority["network"] == {"enabled": False, "allowed_hosts": ()}
    assert authority["process"] == {"enabled": False, "allowed_commands": ()}
    assert authority["repository"] == "FORBIDDEN"
    assert config.audit_required is True


def test_unknown_top_level_field_is_rejected():
    with pytest.raises(PluginConfigurationError) as error:
        PluginConfiguration.load({"magic_admin": True})
    assert error.value.code == "UNKNOWN_CONFIGURATION_FIELD"


def test_unknown_nested_field_is_rejected():
    with pytest.raises(PluginConfigurationError) as error:
        PluginConfiguration.load({"network": {"enabled": False, "proxy": "x"}})
    assert error.value.code == "UNKNOWN_CONFIGURATION_FIELD"


def test_relative_and_non_normalized_roots_are_rejected():
    with pytest.raises(PluginConfigurationError):
        PluginConfiguration.load({"filesystem": {"read_roots": ["relative/path"]}})
    with pytest.raises(PluginConfigurationError):
        PluginConfiguration.load({"filesystem": {"read_roots": ["/tmp/../tmp"]}})


def test_network_and_process_allowlists_require_explicit_enablement():
    with pytest.raises(PluginConfigurationError) as network_error:
        PluginConfiguration.load({"network": {"allowed_hosts": ["example.com"]}})
    assert network_error.value.code == "AUTHORITY_EXCEEDED"
    with pytest.raises(PluginConfigurationError) as process_error:
        PluginConfiguration.load({"process": {"allowed_commands": ["python"]}})
    assert process_error.value.code == "AUTHORITY_EXCEEDED"


def test_wildcard_hosts_and_disabled_audit_are_rejected():
    with pytest.raises(PluginConfigurationError):
        PluginConfiguration.load({"network": {"enabled": True, "allowed_hosts": ["*.example.com"]}})
    with pytest.raises(PluginConfigurationError) as error:
        PluginConfiguration.load({"audit": {"required": False}})
    assert error.value.code == "AUTHORITY_EXCEEDED"


def test_runtime_stores_immutable_configuration_and_reports_bounded_authority():
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0")
    runtime.initialize(
        {
            "allowed_capabilities": ["governed.execute", "filesystem.read"],
            "filesystem": {"read_roots": ["/tmp"], "write_roots": []},
            "network": {"enabled": True, "allowed_hosts": ["example.com"]},
            "process": {"enabled": False, "allowed_commands": []},
        },
        Adapter(),
    )
    assert runtime.configuration is not None
    assert runtime.configuration.filesystem_read_roots == ("/tmp",)
    status = runtime.status()
    assert status["authority"]["filesystem"]["read_roots"] == ("/tmp",)
    assert status["authority"]["network"] == {"enabled": True, "allowed_hosts": ("example.com",)}
    with pytest.raises(Exception):
        runtime.configuration.allowed_capabilities += ("network.admin",)


def test_runtime_rejects_configuration_after_initialization():
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0")
    adapter = Adapter()
    runtime.initialize({}, adapter)
    with pytest.raises(Exception) as error:
        runtime.initialize({"allowed_capabilities": ["governed.execute"]}, adapter)
    assert getattr(error.value, "code", None) == "INVALID_LIFECYCLE_TRANSITION"
