# Sport model
from datetime import datetime
import pytz


def create_sport(conn, name, slug, active):
    c = conn.cursor()
    c.execute("INSERT INTO Sports (name, slug, active) VALUES (?, ?, ?)", (name, slug, active))
    conn.commit()


def read_sport(conn, id):
    c = conn.cursor()
    c.execute("SELECT * FROM Sports WHERE id = ?", (id,))
    return c.fetchone()


def update_sport(conn, id, name, slug, active):
    c = conn.cursor()
    c.execute("UPDATE Sports SET name = ?, slug = ?, active = ? WHERE id = ?", (name, slug, active, id))
    conn.commit()


# When all the events of a sport are inactive, the sport becomes inactive
def check_and_update_sport_status(conn, sport_id):
    c = conn.cursor()
    c.execute("SELECT active FROM Events WHERE sport_id = ?", (sport_id,))
    events_active_status = c.fetchall()

    if not any(status[0] for status in events_active_status):
        c.execute("UPDATE Sports SET active = ? WHERE id = ?", (False, sport_id))
        conn.commit()


def delete_sport(conn, id):
    c = conn.cursor()
    c.execute("DELETE FROM Sports WHERE id = ?", (id,))
    conn.commit()


def search_sports(conn, filters):
    if filters:
        query = "SELECT * FROM Sports WHERE "
        query += " AND ".join([f"{key} = ?" for key in filters])
    else:
        query = "SELECT * FROM Sports"
    c = conn.cursor()
    c.execute(query, tuple(filters.values()))
    return c.fetchall()


# All (sports/events) with a minimum number of active (events/selections) higher than a threshold
def search_sports_with_active_events_greater_than(conn, threshold):
    c = conn.cursor()
    query = """
        SELECT s.id, s.name, COUNT(e.id) as active_event_count 
        FROM Sports s
        JOIN Events e ON s.id = e.sport_id
        WHERE e.active = True
        GROUP BY s.id, s.name
        HAVING COUNT(e.id) > ?
    """
    c.execute(query, (threshold,))
    sports = c.fetchall()
    return sports


def create_event(conn, name, slug, active, type, sport_id, status, scheduled_start, actual_start):
    c = conn.cursor()
    c.execute(
        "INSERT INTO Events (name, slug, active, type, sport_id, status, scheduled_start, actual_start) VALUES (?, ?, "
        "?, ?, ?, ?, ?, ?)",
        (name, slug, active, type, sport_id, status, scheduled_start, actual_start)
    )
    conn.commit()


def read_event(conn, id):
    c = conn.cursor()
    c.execute("SELECT * FROM Events WHERE id = ?", (id,))
    return c.fetchone()


def update_event(conn, event_id, data):
    c = conn.cursor()
    params = (data.get('name'), data.get('active'), data.get('type'), data.get('status'),
              data.get('scheduled_start'), data.get('actual_start'), event_id)
    c.execute(
        "UPDATE Events SET name = ?, active = ?, type = ?, status = ?, scheduled_start = ?, actual_start = ? WHERE id "
        "= ?",
        params)
    check_and_update_sport_status(conn, data.get('sport_id'))
    conn.commit()


# When all the selections of a particular event are inactive, the event becomes inactive
def check_and_update_event_status(conn, event_id):
    c = conn.cursor()
    c.execute("SELECT active FROM Selections WHERE event_id = ?", (event_id,))
    selections_active_status = c.fetchall()

    if not any(status[0] for status in selections_active_status):
        c.execute("UPDATE Events SET active = ? WHERE id = ?", (False, event_id))
        conn.commit()


def delete_event(conn, id):
    c = conn.cursor()
    c.execute("DELETE FROM Events WHERE id = ?", (id,))
    conn.commit()


def search_events(conn, filters):
    if filters:
        query = "SELECT * FROM Events WHERE "
        query += " AND ".join([f"{key} = ?" for key in filters])
    else:
        query = "SELECT * FROM Events"
    c = conn.cursor()
    c.execute(query, tuple(filters.values()))
    return c.fetchall()


def convert_to_utc(time_str, format_str="%Y-%m-%d %H:%M:%S", tz_str='Europe/London'):
    """
    Convert a timezone-aware datetime string to a timezone-naive datetime in UTC.

    Parameters:
    - time_str (str): The datetime string to convert.
    - format_str (str): The format of the datetime string.
        This should match the format codes in Python's datetime module.
        For example, for a date like '2023-07-04 19:00', the format string would be '%Y-%m-%d %H:%M'.
    - tz_str (str): The timezone of the input datetime string.
        This should be a string that pytz can recognize, like 'America/Los_Angeles'.

    Returns:
    - datetime: A timezone-naive datetime object in UTC.
    """
    local_tz = pytz.timezone(tz_str)
    local_dt = datetime.strptime(time_str, format_str)
    local_dt = local_tz.localize(local_dt)
    utc_dt = local_dt.astimezone(pytz.UTC)
    return utc_dt.replace(tzinfo=None)  # Return a timezone-naive datetime


# Events scheduled to start in a specific timeframe for a specific timezone
def search_events_in_timeframe(conn, start_time, end_time):
    st = convert_to_utc(start_time)
    et = convert_to_utc(end_time)
    c = conn.cursor()
    query = "SELECT * FROM Events WHERE scheduled_start BETWEEN ? AND ?"
    c.execute(query, (st, et))
    events = c.fetchall()
    return events


# Selection Model
def create_selection(conn, name, event_id, price, active, outcome):
    c = conn.cursor()
    c.execute(
        "INSERT INTO Selections (name, event_id, price, active, outcome) VALUES (?, ?, ?, ?, ?)",
        (name, event_id, price, active, outcome)
    )
    conn.commit()


def read_selection(conn, id):
    c = conn.cursor()
    c.execute("SELECT * FROM Selections WHERE id = ?", (id,))
    return c.fetchone()


def update_selection(conn, selection_id, data):
    c = conn.cursor()
    params = (data.get('name'), data.get('price'), data.get('active'), data.get('outcome'), selection_id)
    c.execute("UPDATE Selections SET name = ?, price = ?, active = ?, outcome = ? WHERE id = ?", params)

    check_and_update_event_status(conn, data.get('event_id'))

    conn.commit()


def delete_selection(conn, id):
    c = conn.cursor()
    c.execute("DELETE FROM Selections WHERE id = ?", (id,))
    conn.commit()


def search_selections(conn, filters):
    if filters:
        query = "SELECT * FROM Selections WHERE "
        query += " AND ".join([f"{key} = ?" for key in filters])
    else:
        query = "SELECT * FROM Selections"
    c = conn.cursor()
    c.execute(query, tuple(filters.values()))
    return c.fetchall()
