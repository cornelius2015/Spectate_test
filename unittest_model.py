import unittest
import sqlite3
import model


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class TestSportsModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test database in memory
        cls.conn = sqlite3.connect(':memory:')
        cls.conn.row_factory = dict_factory
        c = cls.conn.cursor()

        # Create Sports table
        c.execute('''
            CREATE TABLE Sports(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                active BOOLEAN NOT NULL
            )
        ''')

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_create_and_read_sport(self):
        model.create_sport(self.conn, 'Basketball', 'basketball', 1)
        sport = model.read_sport(self.conn, 1)
        self.assertEqual(sport['name'], 'Basketball')
        self.assertEqual(sport['slug'], 'basketball')
        self.assertEqual(sport['active'], 1)

    def test_update_sport(self):
        model.create_sport(self.conn, 'Basketball', 'basketball', 1)
        model.update_sport(self.conn, 1, 'Football', 'football', 0)
        sport = model.read_sport(self.conn, 1)
        self.assertEqual(sport['name'], 'Football')
        self.assertEqual(sport['slug'], 'football')
        self.assertEqual(sport['active'], 0)

    def test_delete_sport(self):
        model.delete_sport(self.conn, 1)
        sport = model.read_sport(self.conn, 1)
        self.assertIsNone(sport)


class TestEventsModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a test database in memory
        cls.conn = sqlite3.connect(':memory:')
        cls.conn.row_factory = dict_factory
        c = cls.conn.cursor()

        # Create Events table
        c.execute('''
            CREATE TABLE Events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                active BOOLEAN NOT NULL,
                type TEXT NOT NULL,
                sport_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                scheduled_start TEXT NOT NULL,
                actual_start TEXT NOT NULL
            )
        ''')

        c.execute('''
             CREATE TABLE Sports(
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 slug TEXT NOT NULL,
                 active BOOLEAN NOT NULL
             )
         ''')

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_create_and_read_event(self):
        model.create_event(self.conn, 'NBA Finals', 'nba-finals', True, 'inplay', 1, 'Scheduled',
                           '2023-01-01T00:00:00Z', '2023-01-01T00:00:00Z')
        event = model.read_event(self.conn, 1)
        self.assertEqual(event['name'], 'NBA Finals')
        self.assertEqual(event['slug'], 'nba-finals')
        self.assertEqual(event['active'], True)
        self.assertEqual(event['type'], 'inplay')
        self.assertEqual(event['sport_id'], 1)
        self.assertEqual(event['status'], 'Scheduled')
        self.assertEqual(event['scheduled_start'], '2023-01-01T00:00:00Z')
        self.assertEqual(event['actual_start'], '2023-01-01T00:00:00Z')

    def test_update_event(self):
        # Arrange
        model.create_sport(self.conn, 'Basketball', 'basketball', 1)
        # sport = model.read_sport(self.conn, 1)
        data = {'name': 'NBA Finals',
                'slug': 'nba-finals',
                'active': False,
                'type': 'inplay',
                'sport_id': 1,
                'status': 'Started',
                'scheduled_start': '2023-01-01T00:00:00Z',
                'actual_start': '2023-01-01T00:00:00Z'}

        model.create_event(self.conn, **data)

        event = model.read_event(self.conn, 1)
        self.assertEqual(event['name'], 'NBA Finals')
        self.assertEqual(event['status'], 'Started')
        self.assertEqual(event['active'], False)

        # Act
        updated_data = {'name': 'NBA Finals', 'active': False, 'type': 'inplay', 'sport_id': 0, 'status': 'Started',
                        'scheduled_start': '2023-01-01T00:00:00Z', 'actual_start': '2023-01-01T00:00:00Z'}
        model.update_event(self.conn, 1, updated_data)

        # Assert
        updated_event = model.read_event(self.conn, 1)
        self.assertEqual(updated_event['name'], 'NBA Finals')
        self.assertFalse(updated_event['active'])

    def test_delete_event(self):
        model.delete_event(self.conn, 1)
        event = model.read_event(self.conn, 1)
        self.assertIsNone(event)


class TestSelectionsModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(':memory:')
        cls.conn.row_factory = dict_factory
        c = cls.conn.cursor()
        c.execute('''CREATE TABLE Selections
                             (id INTEGER PRIMARY KEY,
                              name TEXT,
                              event_id INTEGER,
                              price REAL, 
                              active BOOLEAN,
                              outcome TEXT)''')

        # Create Events table
        c.execute('''
            CREATE TABLE Events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                active BOOLEAN NOT NULL,
                type TEXT NOT NULL,
                sport_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                scheduled_start TEXT NOT NULL,
                actual_start TEXT NOT NULL
            )
        ''')

        c.execute('''
             CREATE TABLE Sports(
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 slug TEXT NOT NULL,
                 active BOOLEAN NOT NULL
             )
         ''')

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        self.conn.execute("DELETE FROM Selections")

    def tearDown(self):
        pass

    def test_create_and_read_selection(self):
        model.create_selection(self.conn, 'Lakers Win', 1, 1.5, True, 'Unsettled')
        selection = model.read_selection(self.conn, 1)
        self.assertEqual(selection['name'], 'Lakers Win')

    def test_update_selection(self):
        model.create_selection(self.conn, 'Lakers Win', 1, 1.5, True, 'Unsettled')
        data = {'name': 'Lakers Win', 'event_id': 0, 'price': 2.0, 'active': False, 'outcome': 'Unsettled'}
        model.update_selection(self.conn, 1, data)
        selection = model.read_selection(self.conn, 1)
        self.assertEqual(selection['price'], 2.0)
        self.assertEqual(selection['active'], False)

    def test_delete_selection(self):
        model.create_selection(self.conn, 'Lakers Win', 1, 1.5, True, 'Unsettled')
        model.delete_selection(self.conn, 1)
        selection = model.read_selection(self.conn, 1)
        self.assertIsNone(selection)

    def test_search_selections(self):
        model.create_selection(self.conn, 'Lakers Win', 1, 1.5, True, 'Unsettled')
        model.create_selection(self.conn, 'Raptors Win', 1, 2.5, True, 'Unsettled')
        filters = {'active': True}
        selections = model.search_selections(self.conn, filters)
        self.assertEqual(len(selections), 2)
        self.assertEqual(selections[0]['name'], 'Lakers Win')
        self.assertEqual(selections[1]['name'], 'Raptors Win')


if __name__ == '__main__':
    unittest.main()
