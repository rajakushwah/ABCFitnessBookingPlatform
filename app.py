from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
classes = {}
bookings = {}

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def find_class_by_date_and_name(class_name, booking_date):
    return classes.get((class_name, booking_date))

@app.route('/classes', methods=['POST'])
def create_class():
    try:
        data = request.json
        class_name = data.get('class_name')
        start_date = validate_date(data.get('start_date'))
        end_date = validate_date(data.get('end_date'))
        capacity = data.get('capacity')
        if not class_name or not start_date or not end_date or not capacity:
            return jsonify({'error': 'All fields (class_name, start_date, end_date, capacity) are required.'}), 400
        if start_date > end_date:
            return jsonify({'error': 'Start date cannot be after end date.'}), 400
        if not isinstance(capacity, int) or capacity <= 0:
            return jsonify({'error': 'Capacity must be a positive integer.'}), 400

        current_date = start_date
        while current_date <= end_date:
            class_key = (class_name, current_date)
            if class_key in classes:
                return jsonify({'error': f'Class "{class_name}" on {current_date} already exists.'}), 400
            classes[class_key] = {'capacity': capacity, 'booked': 0}
            current_date += timedelta(days=1)
        print(classes)
        return jsonify({'message': 'Classes created successfully!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bookings', methods=['POST'])
def book_class():
    try:
        data = request.json
        member_name = data.get('name')
        booking_date = validate_date(data.get('date'))
        class_name = data.get('class_name')

        if not member_name or not booking_date or not class_name:
            return jsonify({'error': 'All fields (name, date, class_name) are required.'}), 400

        studio_class = find_class_by_date_and_name(class_name, booking_date)
        if not studio_class:
            return jsonify({'error': f'Class "{class_name}" on {booking_date} not found.'}), 404

        bookings[(member_name, class_name, booking_date)] = {
            'member_name': member_name,
            'class_name': class_name,
            'date': booking_date
        }
        studio_class['booked'] += 1

        return jsonify({'message': 'Booking successful!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/classes', methods=['GET'])
def get_classes():
    try:
        result = []
        for (class_name, date), details in classes.items():
            result.append({
                'class_name': class_name,
                'date': date.strftime('%Y-%m-%d'),
                'capacity': details['capacity'],
                'booked': details['booked'],
                'remaining_capacity': details['capacity'] - details['booked']
            })
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bookings', methods=['GET'])
def get_bookings():
    try:
        result = []
        for (member_name, class_name, date), booking_details in bookings.items():
            result.append({
                'member_name': member_name,
                'class_name': class_name,
                'date': date.strftime('%Y-%m-%d'),
            })
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
