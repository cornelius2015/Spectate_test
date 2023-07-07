import unittest
from flask import Flask, jsonify, abort, request, json
from unittest.mock import patch, Mock
import rest_application
import sqlite3
import model
from unittest.mock import patch, MagicMock


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = rest_application.app
        self.client = self.app.test_client()

    @patch('rest_application.get_db')
    def test_create_sport(self, mock_get_db):
        # Mock the database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Call the function with some example parameters
        model.create_sport(mock_conn, 'Football', 'football', True)

        # Assert the function made the expected database calls
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO Sports (name, slug, active) VALUES (?, ?, ?)",
            ('Football', 'football', True)
        )
        mock_conn.commit.assert_called_once()

    @patch('rest_application.get_db')
    def test_create_event(self, mock_get_db):
        # Mock the database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Define the data dictionary to match what the function expects
        data = {
            'name': 'NBA Finals',
            'slug': 'nba-finals',
            'active': True,
            'type': 'inplay',
            'sport_id': 1,
            'status': 'Started',
            'scheduled_start': '2023-01-01T00:00:00Z',
            'actual_start': '2023-01-01T00:00:00Z'
        }

        # Call the function with the example parameters
        model.create_event(mock_conn, **data)

        # Assert the function made the expected database calls
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO Events (name, slug, active, type, sport_id, status, scheduled_start, actual_start) VALUES ("
            "?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(data.values())
        )
        mock_conn.commit.assert_called_once()

    @patch('rest_application.get_db')
    def test_create_selection(self, mock_get_db):
        # Mock the database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Define the data dictionary to match what the function expects
        data = {
            'name': 'Lakers Win',
            'event_id': 1,
            'price': 1.5,
            'active': True,
            'outcome': 'Unsettled'
        }

        # Call the function with the example parameters
        model.create_selection(mock_conn, **data)

        # Assert the function made the expected database calls
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO Selections (name, event_id, price, active, outcome) VALUES (?, ?, ?, ?, ?)",
            tuple(data.values())
        )
        mock_conn.commit.assert_called_once()

    @patch('rest_application.get_db')
    def test_update_sport(self, mock_get_db):
        # Mock the database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Define the data dictionary to match what the function expects
        data = {
            'name': 'Basketball',
            'slug': 'basketball',
            'active': True
        }

        # Define the sport_id
        sport_id = 1

        # Call the function with the example parameters
        model.update_sport(mock_conn, sport_id, **data)

        # Assert the function made the expected database calls
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "UPDATE Sports SET name = ?, slug = ?, active = ? WHERE id = ?",
            (*data.values(), sport_id)
        )
        mock_conn.commit.assert_called_once()

    @patch('rest_application.get_db', autospec=True)
    @patch('rest_application.model.update_event', autospec=True)
    def test_update_event(self, mock_update_event, mock_get_db):
        # Mocking
        mock_db_conn = MagicMock()
        mock_get_db.return_value = mock_db_conn
        mock_update_event.return_value = None  # add appropriate return value here

        data = {
            'name': 'Test Event',
            'slug': 'test-event',
            'active': True,
            'type': 'Test Type',
            'sport_id': 1,
            'status': 'Ongoing',
            'scheduled_start': '2023-07-06T00:00:00.000Z',
            'actual_start': '2023-07-06T00:00:00.000Z',
        }

        # Call the function through the test client
        response = self.client.put('/events/1', json=data)

        # Check the function behaved as expected
        mock_get_db.assert_called_once()
        mock_update_event.assert_called_once_with(
            mock_db_conn, 1, data)
        self.assertEqual(response.status_code, 200)
        mock_db_conn.close.assert_called_once()

    @patch('rest_application.get_db', autospec=True)
    @patch('rest_application.model.update_selection', autospec=True)
    def test_update_selection(self, mock_update_selection, mock_get_db):
        # Mocking
        mock_db_conn = MagicMock()
        mock_get_db.return_value = mock_db_conn
        mock_update_selection.return_value = None

        data = {
            'name': 'Test Selection',
            'event_id': 1,
            'price': 10.0,
            'active': True,
            'outcome': 'Win',
        }

        # Call the function through the test client
        response = self.client.put('/selections/1', json=data)

        # Check the function behaved as expected
        mock_get_db.assert_called_once()
        mock_update_selection.assert_called_once_with(
            mock_db_conn, 1, data)
        self.assertEqual(response.status_code, 200)
        mock_db_conn.close.assert_called_once()

    @patch('rest_application.get_db', autospec=True)
    @patch('rest_application.model.search_sports', autospec=True)
    def test_get_sports(self, mock_search_sports, mock_get_db):
        # Mocking
        mock_db_conn = MagicMock()
        mock_get_db.return_value = mock_db_conn
        mock_search_sports.return_value = [{"id": 1, "name": "Test Sport", "active": True}]

        # Call the function through the test client with no filters
        response = self.client.get('/sports')

        # Check the function behaved as expected
        mock_get_db.assert_called_once()
        mock_search_sports.assert_called_once_with(mock_db_conn, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'sports': [{"id": 1, "name": "Test Sport", "active": True}]})
        mock_db_conn.close.assert_called_once()

        # Reset mocks
        mock_get_db.reset_mock()
        mock_search_sports.reset_mock()
        mock_db_conn.close.reset_mock()

        # Call the function through the test client with filters
        response = self.client.get('/sports', query_string={'active': 'true'})

        # Check the function behaved as expected
        mock_get_db.assert_called_once()
        mock_search_sports.assert_called_once_with(mock_db_conn, {'active': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'sports': [{"id": 1, "name": "Test Sport", "active": True}]})
        mock_db_conn.close.assert_called_once()

    @patch('rest_application.get_db', autospec=True)
    def test_get_sport_events(self, mock_get_db):
        # Mocking
        mock_db_conn = MagicMock()
        mock_get_db.return_value = mock_db_conn
        mock_db_conn.cursor().fetchall.return_value = [{"id": 1, "name": "Test Event"}]

        # Call the function through the test client with sport_id 1
        response = self.client.get('/sports/1/events')

        # Check the function behaved as expected
        mock_get_db.assert_called_once()
        mock_db_conn.cursor().execute.assert_called_once_with('SELECT * FROM Events WHERE sport_id = ?', (1,))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'events': [{"id": 1, "name": "Test Event"}]})
        mock_db_conn.close.assert_called_once()

        # Reset mocks
        mock_get_db.reset_mock()
        mock_db_conn.close.reset_mock()
        mock_db_conn.cursor().execute.reset_mock()
        mock_db_conn.cursor().fetchall.reset_mock()

        # Call the function through the test client with sport_id 2 and no events
        mock_db_conn.cursor().fetchall.return_value = []
        response = self.client.get('/sports/2/events')

        # Check the function behaved as expected
        mock_get_db.assert_called_once()
        mock_db_conn.cursor().execute.assert_called_once_with('SELECT * FROM Events WHERE sport_id = ?', (2,))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'No events found for this sport'})
        mock_db_conn.close.assert_called_once()

    @patch('rest_application.get_db', autospec=True)
    def test_get_events(self, mock_get_db):
        # Mocking
        mock_db_conn = MagicMock()
        mock_get_db.return_value = mock_db_conn
        mock_db_conn.cursor().fetchall.return_value = [{"id": 1, "name": "Test Event"}]

        # Call the function with a valid active filter
        with self.client as c:
            with c.get('/events?active=true') as response:
                # Check the function behaved as expected
                mock_get_db.assert_called_once()
                mock_db_conn.cursor().execute.assert_called_once_with(
                    'SELECT * FROM Events WHERE active = ?', (1,))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), {'events': [{"id": 1, "name": "Test Event"}]})
                mock_db_conn.close.assert_called_once()

        # Reset mocks
        mock_get_db.reset_mock()
        mock_db_conn.cursor().execute.reset_mock()
        mock_db_conn.close.reset_mock()

        # Call the function with an invalid filter
        with self.client as c:
            with c.get('/events?invalid_filter=true') as response:
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.get_json(), {'error': 'Invalid filter: invalid_filter'})

        # Reset mocks
        mock_get_db.reset_mock()

        # Call the function with an invalid active filter
        with self.client as c:
            with c.get('/events?active=invalid') as response:
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.get_json(), {'error': 'Invalid active value, must be true or false.'})

    @patch('rest_application.get_db', autospec=True)
    def test_get_event_selections(self, mock_get_db):
        # Mocking
        mock_db_conn = MagicMock()
        mock_get_db.return_value = mock_db_conn
        mock_db_conn.cursor().fetchall.return_value = [{"id": 1, "name": "Test Selection"}]

        # Call the function with a valid event id
        with self.client as c:
            with c.get('/events/1/selections') as response:
                # Check the function behaved as expected
                mock_get_db.assert_called_once()
                mock_db_conn.cursor().execute.assert_called_once_with(
                    'SELECT * FROM Selections WHERE event_id = ?', (1,))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), {'selections': [{"id": 1, "name": "Test Selection"}]})
                mock_db_conn.close.assert_called_once()

        # Reset mocks
        mock_get_db.reset_mock()
        mock_db_conn.cursor().execute.reset_mock()
        mock_db_conn.close.reset_mock()

        # Call the function with an event id that does not exist in the database
        mock_db_conn.cursor().fetchall.return_value = []

        with self.client as c:
            with c.get('/events/1/selections') as response:
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.get_json(), {'error': 'No selections found for the provided event id.'})

    @patch('rest_application.get_db', autospec=True)
    @patch('rest_application.model.search_selections', autospec=True)
    def test_get_selections(self, mock_search_selections, mock_get_db):
        # Mocking
        mock_db_conn = MagicMock()
        mock_get_db.return_value = mock_db_conn

        mock_search_selections.return_value = [
            {"id": 1, "name": "Test Selection", "event_id": 1, "price": 10.0, "active": True, "outcome": "won"}]

        # Create a test client using the Flask application configured for testing
        with self.client as client:
            response = client.get('/selections?active=true')
            json_data = response.get_json()

            # Check the function behaved as expected
            mock_get_db.assert_called_once()
            mock_search_selections.assert_called_once_with(mock_db_conn, {'active': 1})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json_data, {'selections': [
                {"id": 1, "name": "Test Selection", "event_id": 1, "price": 10.0, "active": True, "outcome": "won"}]})
            mock_db_conn.close.assert_called_once()

        # Reset mocks
        mock_get_db.reset_mock()
        mock_search_selections.reset_mock()
        mock_db_conn.close.reset_mock()

        # Testing when no selections are found
        mock_search_selections.return_value = []

        with self.client as client:
            response = client.get('/selections?active=false')
            json_data = response.get_json()

            mock_get_db.assert_called_once()
            mock_search_selections.assert_called_once_with(mock_db_conn, {'active': 0})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(json_data, {'error': 'No selections found for the provided filters.'})
            mock_db_conn.close.assert_called_once()

        # Reset mocks
        mock_get_db.reset_mock()
        mock_search_selections.reset_mock()
        mock_db_conn.close.reset_mock()

        # Testing for invalid active value
        with self.client as client:
            response = client.get('/selections?active=maybe')
            json_data = response.get_json()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(json_data, {'error': 'Invalid active value, must be true or false.'})

        # Testing for invalid filter
        with self.client as client:
            response = client.get('/selections?invalid_filter=value')
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
