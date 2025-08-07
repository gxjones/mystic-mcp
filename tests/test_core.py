"""
Tests for the core module.
"""

from mystic_mcp.core import MysticMCP


class TestMysticMCP:
    """Test cases for MysticMCP class."""

    def test_init_default(self):
        """Test MysticMCP initialization with default config."""
        mcp = MysticMCP()
        assert mcp.config == {}

    def test_init_with_config(self):
        """Test MysticMCP initialization with custom config."""
        config = {"host": "localhost", "port": 8080}
        mcp = MysticMCP(config)
        assert mcp.config == config

    def test_send_message(self):
        """Test sending a message."""
        mcp = MysticMCP()
        response = mcp.send_message("test message")
        assert response["status"] == "success"
        assert "message" in response

    def test_connect(self):
        """Test connection method."""
        mcp = MysticMCP()
        # Should not raise any exceptions
        mcp.connect()

    def test_disconnect(self):
        """Test disconnection method."""
        mcp = MysticMCP()
        # Should not raise any exceptions
        mcp.disconnect()
