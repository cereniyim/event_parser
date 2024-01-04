import datetime

from fastapi.testclient import TestClient
import unittest
from unittest.mock import patch, mock_open
from app.main import app


class TestReadCustomerEvents(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("glob.glob")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"timestamp":"2019-09-28T01:00:00"}',
    )
    @patch("json.loads")
    def test_read_customer_events(self, mock_json_loads, mock_open, mock_glob):
        # Define the mocked behavior
        mock_json_loads.return_value = {
            "customer_id": 1,
            "event_type": "email_open",
            "timestamp": "2023-10-24T11:30:00",
            "email_id": 998,
            "clicked_link": None,
            "product_id": None,
            "amount": None,
        }
        mock_glob.return_value = ["data/parsed/customer_id_1_2019.json"]

        # Make request and test response
        response = self.client.get("/customer_events?customer_id=1")
        assert response.status_code == 200
        assert response.json() == {
            "customer_id": 1,
            "event_type": "email_open",
            "timestamp": datetime.datetime(2023, 10, 24, 11, 30),
            "email_id": 998,
            "clicked_link": None,
            "product_id": None,
            "amount": None,
        }

    @patch("glob.glob")
    def test_read_customer_events_no_events(self, mock_glob):
        # Define what glob.glob should return
        mock_glob.return_value = []

        # Call function and assert HTTP status code and message
        response = self.client.get("/customer_events?customer_id=1")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer 1 is not found"
