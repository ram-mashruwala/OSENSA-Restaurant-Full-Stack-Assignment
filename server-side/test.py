import unittest
import json
from unittest.mock import Mock, MagicMock

# import the callback from your module
from main import on_connect, on_disconnect, on_message


class TestOnConnect(unittest.TestCase):

    # Test on_connect when it is successful
    def test_on_connect_success(self):
        # Mock parameters
        client = Mock()
        userdata = None
        flags = {}
        rc = 0  # success
        properties = None

        connected = on_connect(client, userdata, flags, rc, properties)

        self.assertTrue(connected)

    # Test on_connect with failure
    def test_on_connect_failure(self):
        client = Mock()
        userdata = None
        flags = {}
        rc = 1  # failure code
        properties = None

        connected = on_connect(client, userdata, flags, rc, properties)

        self.assertFalse(connected)


class TestOnDisconnect(unittest.TestCase):
    # Test on_disconnect
    def test_disconnect(self):
        client = Mock()
        userdata = None
        flags = {}
        rc = 0
        properties = None

        running = on_disconnect(client, userdata, flags, rc, properties)

        self.assertFalse(running)


class TestOnMessage(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()

    # Test on_message with valid input
    def test_on_message_valid(self):
        message = MagicMock()
        message.payload = json.dumps({"id": 1, "order": "Pizza"}).encode("utf-8")

        result = on_message(self.client, None, message)
        self.assertTrue(result)

    # Test on_message with missing keys
    def test_on_message_missing_keys(self):
        message = MagicMock()
        message.payload = json.dumps({"id": 1}).encode("utf-8")

        result = on_message(self.client, None, message)
        self.assertFalse(result)

    # Test on_message with invalid id type
    def test_on_message_invalid_id(self):
        message = MagicMock()
        message.payload = json.dumps({"id": "abc", "order": "Pizza"}).encode("utf-8")

        result = on_message(self.client, None, message)
        self.assertFalse(result)

    # Test on_message when id out of bounds
    def test_on_message_id_out_of_bounds(self):
        message = MagicMock()
        message.payload = json.dumps({"id": 10, "order": "Pizza"}).encode("utf-8")

        result = on_message(self.client, None, message)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
