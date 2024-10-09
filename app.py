from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Set up MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['calendar_db']
events_collection = db['events']

@app.route('/')
def calendar():
    return render_template('calendar.html')

@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        event_data = request.get_json()
        events_collection.update_one(
            {'day': event_data['day']}, 
            {'$set': event_data}, 
            upsert=True
        )
        return jsonify(status="success")

    all_events = events_collection.find()
    events = {event['day']: event for event in all_events}
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
