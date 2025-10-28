import unittest
from unittest.mock import Mock

# import the callback from your module
from main import on_connect, on_disconnect


class TestOnConnect(unittest.TestCase):

    def test_on_connect_success(self):
        # Mock parameters
        client = Mock()
        userdata = None
        flags = {}
        rc = 0  # success
        properties = None

        connected = on_connect(client, userdata, flags, rc, properties)

        self.assertTrue(connected)

    def test_on_connect_failure(self):
        client = Mock()
        userdata = None
        flags = {}
        rc = 1  # failure code
        properties = None

        connected = on_connect(client, userdata, flags, rc, properties)

        self.assertFalse(connected)


class TestOnDisconncet(unittest.TestCase):
    def test_disconnect(self):
        client = Mock()
        userdata = None
        flags = {}
        rc = 0
        properties = None

        running = on_disconnect(client, userdata, flags, rc, properties)

        self.assertFalse(running)


if __name__ == "__main__":
    unittest.main()
