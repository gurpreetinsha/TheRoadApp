from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Mock data for demonstration
transport_vehicles = [
    {
        "id": 1,
        "name": "Bus 101",
        "type": "bus",
        "location": {"lat": 40.7128, "lng": -74.0060},
        "route": "Downtown Express",
        "status": "active"
    },
    {
        "id": 2,
        "name": "Bus 202",
        "type": "bus",
        "location": {"lat": 40.7138, "lng": -74.0050},
        "route": "Uptown Local",
        "status": "active"
    }
]

road_hazards = [
    {
        "id": 1,
        "type": "pothole",
        "severity": "high",
        "location": {"lat": 40.7118, "lng": -74.0065},
        "reported_by": "mobile_app",
        "timestamp": "2023-09-18T10:30:00Z",
        "status": "reported"
    }
]

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify(transport_vehicles)

@app.route('/api/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = next((v for v in transport_vehicles if v["id"] == vehicle_id), None)
    if vehicle:
        return jsonify(vehicle)
    return jsonify({"error": "Vehicle not found"}), 404

@app.route('/api/hazards', methods=['GET'])
def get_hazards():
    return jsonify(road_hazards)

@app.route('/api/hazards', methods=['POST'])
def report_hazard():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validate required fields
    required_fields = ["type", "location", "severity"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Create new hazard report
    new_hazard = {
        "id": len(road_hazards) + 1,
        "type": data["type"],
        "severity": data["severity"],
        "location": data["location"],
        "reported_by": data.get("reported_by", "web_app"),
        "timestamp": data.get("timestamp", ""),
        "status": "reported"
    }
    
    road_hazards.append(new_hazard)
    return jsonify(new_hazard), 201

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Process gyroscope and GPS data
    # In a real application, this would analyze the data and potentially create hazard reports
    
    return jsonify({"status": "received", "message": "Sensor data processed successfully"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)