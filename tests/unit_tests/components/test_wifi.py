"""Tests for wifi component validation behavior."""

from ipaddress import IPv4Address

from esphome.components import wifi
from esphome.const import (
    CONF_DOMAIN,
    CONF_MANUAL_IP,
    CONF_NETWORKS,
    CONF_STATIC_IP,
    CONF_USE_ADDRESS,
)
from esphome.core import CORE


def test_validate_keeps_default_local_use_address_implicit(monkeypatch):
    """Default .local address should be derived at runtime from App name."""
    monkeypatch.setattr(CORE, "name", "test-node")

    config = {
        CONF_DOMAIN: ".local",
        CONF_NETWORKS: [],
    }

    validated = wifi._validate(config)

    assert CONF_USE_ADDRESS not in validated


def test_validate_sets_use_address_for_custom_domain(monkeypatch):
    """Custom domains should still generate an explicit use_address."""
    monkeypatch.setattr(CORE, "name", "test-node")

    config = {
        CONF_DOMAIN: ".home",
        CONF_NETWORKS: [],
    }

    validated = wifi._validate(config)

    assert validated[CONF_USE_ADDRESS] == "test-node.home"


def test_validate_prefers_manual_ip_for_use_address(monkeypatch):
    """Manual IP should continue to override use_address."""
    monkeypatch.setattr(CORE, "name", "test-node")

    config = {
        CONF_DOMAIN: ".local",
        CONF_MANUAL_IP: {CONF_STATIC_IP: IPv4Address("192.168.10.22")},
    }

    validated = wifi._validate(config)

    assert validated[CONF_USE_ADDRESS] == "192.168.10.22"
