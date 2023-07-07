from flask import Flask, abort, jsonify, request
from datetime import datetime

import sqlite3
from flask import Flask, request, jsonify
import datetime
import model

DATABASE = 'sportsbook.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


app = Flask(__name__)


# Creating
@app.route('/sports', methods=['POST'])
def create_sport():
    data = request.json

    # Validate inputs
    if 'name' not in data or 'slug' not in data or 'active' not in data:
        abort(400, 'Missing required parameter in the JSON body')

    if not isinstance(data['name'], str) or not isinstance(data['slug'], str) or not isinstance(data['active'], bool):
        abort(400, 'Invalid value type for parameter in the JSON body')

    try:
        conn = get_db()
        model.create_sport(conn, data['name'], data['slug'], data['active'])
        conn.close()
    except Exception as e:
        print(e)
        abort(500, str(e))

    return {'status': 'success'}, 201


@app.route('/events', methods=['POST'])
def create_event():
    data = request.json

    # Define required parameters and their types
    required_params = {
        'name': str,
        'slug': str,
        'active': bool,
        'type': str,
        'sport_id': int,
        'status': str,
        'scheduled_start': str,
        'actual_start': str
    }

    # Validate inputs
    for param, ptype in required_params.items():
        if param not in data:
            abort(400, f"Missing required parameter {param} in the JSON body")

        if not isinstance(data[param], ptype):
            abort(400, f"Invalid value type for parameter {param} in the JSON body")

    try:
        conn = get_db()
        model.create_event(conn, data['name'], data['slug'], data['active'], data['type'], data['sport_id'],
                           data['status'], data['scheduled_start'], data['actual_start'])
        conn.close()
    except Exception as e:
        abort(500, str(e))

    return {'status': 'success'}, 201


@app.route('/selections', methods=['POST'])
def create_selection():
    data = request.json

    # Validate inputs
    if 'name' not in data or 'event_id' not in data or 'price' not in data or 'active' not in data or 'outcome' not in data:
        abort(400, 'Missing required parameter in the JSON body')

    if not isinstance(data['name'], str) or not isinstance(data['event_id'], int) or not isinstance(data['price'],
                                                                                                    float) \
            or not isinstance(data['active'], bool) or not isinstance(data['outcome'], str):
        abort(400, 'Invalid value type for parameter in the JSON body')

    # Handle exceptions
    try:
        conn = get_db()
        model.create_selection(conn, data['name'], data['event_id'], data['price'], data['active'], data['outcome'])
        conn.close()
    except Exception as e:
        abort(500, str(e))

    return {'status': 'success'}, 201


# Updating
@app.route('/sports/<int:sport_id>', methods=['PUT'])
def update_sport(sport_id):
    data = request.json

    # Validate input
    if not data or 'name' not in data or 'slug' not in data or 'active' not in data:
        abort(400, description="Invalid data. 'name', 'slug', and 'active' are required.")
    if not isinstance(data['name'], str) or not isinstance(data['slug'], str) or not isinstance(data['active'], bool):
        abort(400, description="Invalid data types. 'name' and 'slug' should be strings. 'active' should be a boolean.")

    try:
        conn = get_db()
        model.update_sport(conn, sport_id, data['name'], data['slug'], data['active'])
        conn.close()
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}, 500

    return {'status': 'success'}, 200


@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()

    # Validate input
    required_fields = {'name', 'slug', 'active', 'type', 'sport_id', 'status', 'scheduled_start', 'actual_start'}
    if not data or not required_fields.issubset(data.keys()):
        abort(400, description="Invalid data. Required fields: {}".format(", ".join(required_fields)))

    if not all(isinstance(data[field], str) for field in ['name', 'slug', 'type', 'status']):
        abort(400, description="Invalid data types. 'name', 'slug', 'type', and 'status' should be strings.")
    if not isinstance(data['active'], bool):
        abort(400, description="Invalid data type. 'active' should be a boolean.")
    if not isinstance(data['sport_id'], int):
        abort(400, description="Invalid data type. 'sport_id' should be an integer.")
    if not (isinstance(data['scheduled_start'], str) and isinstance(data['actual_start'], str)):
        abort(400,
              description="Invalid data types. 'scheduled_start' and 'actual_start' should be strings (ISO 8601 "
                          "format).")

    try:
        conn = get_db()
        model.update_event(conn, event_id, data)
        conn.close()
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}, 500

    return {'message': 'Event updated successfully'}, 200


@app.route('/selections/<int:selection_id>', methods=['PUT'])
def update_selection(selection_id):
    data = request.get_json()

    # Validate input
    required_fields = {'name', 'event_id', 'price', 'active', 'outcome'}
    if not data or not required_fields.issubset(data.keys()):
        abort(400, description="Invalid data. Required fields: {}".format(", ".join(required_fields)))

    # Validate the data types
    if not isinstance(data['name'], str):
        abort(400, description="Invalid data type. 'name' should be a string.")
    if not isinstance(data['event_id'], int):
        abort(400, description="Invalid data type. 'event_id' should be an integer.")
    if not isinstance(data['price'], (int, float)):
        abort(400, description="Invalid data type. 'price' should be a numeric value.")
    if not isinstance(data['active'], bool):
        abort(400, description="Invalid data type. 'active' should be a boolean.")
    if not isinstance(data['outcome'], str):
        abort(400, description="Invalid data type. 'outcome' should be a string.")

    try:
        conn = get_db()
        model.update_selection(conn, selection_id, data)
        conn.close()
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}, 500

    return {'message': 'Selection updated successfully'}, 200


# Searching
@app.route('/sports', methods=['GET'])
def get_sports():
    # Validate input
    valid_filters = {'name', 'active'}  # define valid filters
    filters = request.args.to_dict()

    if 'active' in filters:
        if filters['active'].lower() == "true":
            filters['active'] = 1
        elif filters['active'].lower() == "false":
            filters['active'] = 0
        else:
            return jsonify({'error': 'Invalid active value, must be true or false.'}), 400

    # Check if the input filters are valid
    if not set(filters.keys()).issubset(valid_filters):
        invalid_filters = set(filters.keys()) - valid_filters
        abort(400, description="Invalid filters: {}".format(", ".join(invalid_filters)))

    try:
        conn = get_db()
        sports = model.search_sports(conn, filters)
        conn.close()
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}, 500

    return {'sports': sports}, 200


@app.route('/sports/<int:sport_id>/events', methods=['GET'])
def get_sport_events(sport_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM Events WHERE sport_id = ?', (sport_id,))
        events = c.fetchall()
        conn.close()
        if events:
            return jsonify({'events': events}), 200
        else:
            return jsonify({'error': 'No events found for this sport'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/events', methods=['GET'])
def get_events():
    valid_event_filters = ['name', 'type', 'status', 'scheduled_start', 'actual_start', 'active', 'sport_id']

    try:
        filters = request.args.to_dict()
        if 'active' in filters:
            if filters['active'].lower() == "true":
                filters['active'] = 1
            elif filters['active'].lower() == "false":
                filters['active'] = 0
            else:
                return jsonify({'error': 'Invalid active value, must be true or false.'}), 400
        for key in filters.keys():
            if key not in valid_event_filters:
                return {'error': f'Invalid filter: {key}'}, 400

        conn = get_db()
        events = model.search_events(conn, filters)
        conn.close()
        if events:
            return jsonify({'events': events}), 200
        else:
            return jsonify({'error': 'No events found for the provided filters.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/events/<int:event_id>/selections', methods=['GET'])
def get_event_selections(event_id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM Selections WHERE event_id = ?', (event_id,))
        selections = c.fetchall()
        conn.close()
        if selections:
            return jsonify({'selections': selections}), 200
        else:
            return jsonify({'error': 'No selections found for the provided event id.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/selections', methods=['GET'])
def get_selections():
    try:
        filters = request.args.to_dict()
        if 'active' in filters:
            if filters['active'].lower() == "true":
                filters['active'] = 1
            elif filters['active'].lower() == "false":
                filters['active'] = 0
            else:
                return jsonify({'error': 'Invalid active value, must be true or false.'}), 400

        # Validate filters before using them
        valid_filters = ["name", "event_id", "price", "active", "outcome"]
        for filter_name in filters.keys():
            if filter_name not in valid_filters:
                return jsonify({'error': f'Invalid filter: {filter_name}. Valid filters are {valid_filters}'}), 400

        conn = get_db()
        selections = model.search_selections(conn, filters)
        conn.close()

        if selections:
            return jsonify({'selections': selections}), 200
        else:
            return jsonify({'error': 'No selections found for the provided filters.'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
