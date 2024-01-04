import unittest
from unittest.mock import patch, mock_open
from fastapi.testclient import TestClient
from app.main import app


class TestCreateEvent(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("uuid.uuid4")
    def test_create_event(self, mock_uuid, mock_json_dump, mock_open):
        mock_uuid.return_value = "test_uuid"

        event_data = {
            "customer_id": 1,
            "event_type": "email_unsubscribe",
            "timestamp": "2023-10-24T11:30:25",
            "email_id": 998,
        }

        response = self.client.post("/event", json=event_data)

        assert response.status_code == 200
        # TODO add more thorough assertions here
