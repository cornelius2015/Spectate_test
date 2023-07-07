import sqlite3


def create_database_and_tables():
    conn = sqlite3.connect('sportsbook.db')  # This creates the database file if it doesn't exist
    c = conn.cursor()

    # Create Sports table
    c.execute('''
        CREATE TABLE Sports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            active BOOLEAN NOT NULL
        )
    ''')

    # Create Events table
    c.execute('''
        CREATE TABLE Events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            active BOOLEAN NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('preplay', 'inplay')),
            sport_id INTEGER,
            status TEXT NOT NULL CHECK(status IN ('Pending', 'Started', 'Ended', 'Cancelled')),
            scheduled_start TEXT NOT NULL,
            actual_start TEXT,
            FOREIGN KEY(sport_id) REFERENCES Sports(id)
        )
    ''')

    # Create Selections table
    c.execute('''
        CREATE TABLE Selections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            event_id INTEGER,
            price REAL NOT NULL,
            active BOOLEAN NOT NULL,
            outcome TEXT NOT NULL CHECK(outcome IN ('Unsettled', 'Void', 'Lose', 'Win')),
            FOREIGN KEY(event_id) REFERENCES Events(id)
        )
    ''')

    conn.commit()
    conn.close()


def populate_database_with_sample_data():
    conn = sqlite3.connect('sportsbook.db')
    c = conn.cursor()

    # Insert sample data into Sports table
    sports_data = [
        ('Football', 'football', True),
        ('Basketball', 'basketball', True),
        ('Tennis', 'tennis', False),
    ]
    c.executemany('INSERT INTO Sports (name, slug, active) VALUES (?, ?, ?)', sports_data)

    # Insert sample data into Events table
    events_data = [
        ('UEFA Europa League', 'uefa-europa-league', True, 'preplay', 1, 'Pending', '2023-07-10 20:00:00', None),
        ('NBA Finals', 'nba-finals', True, 'inplay', 2, 'Started', '2023-06-01 19:30:00', '2023-06-01 19:35:00'),
    ]
    c.executemany('''
        INSERT INTO Events (name, slug, active, type, sport_id, status, scheduled_start, actual_start) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', events_data)

    # Insert sample data into Selections table
    selections_data = [
        ('Man Utd Win', 1, 1.9, True, 'Unsettled'),
        ('Draw', 1, 3.4, True, 'Unsettled'),
        ('AC Milan Win', 1, 4.0, True, 'Unsettled'),
        ('Lakers Win', 2, 1.6, True, 'Unsettled'),
        ('Heat Win', 2, 2.2, False, 'Unsettled'),
    ]
    c.executemany('''
        INSERT INTO Selections (name, event_id, price, active, outcome)
        VALUES (?, ?, ?, ?, ?)
    ''', selections_data)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database_and_tables()
    populate_database_with_sample_data()

