from flask import Blueprint, jsonify, request
from ..models import db, SensorData, Vehicle, Hazard
from geoalchemy2.elements import WKTElement
from datetime import datetime
import numpy as np

sensor_bp = Blueprint('sensors', __name__)

@sensor_bp.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    """Receive and process sensor data from mobile devices."""
    data = request.json
    
    # Validate required fields
    required_fields = ['vehicle_id', 'gyroscope', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate vehicle exists
    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    
    # Create location point from coordinates
    location = None
    if 'lat' in data['location'] and 'lng' in data['location']:
        location = WKTElement(f"POINT({data['location']['lng']} {data['location']['lat']})", srid=4326)
    else:
        return jsonify({'error': 'Invalid location format'}), 400
    
    # Create new sensor data record
    new_sensor_data = SensorData(
        vehicle_id=data['vehicle_id'],
        gyroscope_x=data['gyroscope'].get('x', 0),
        gyroscope_y=data['gyroscope'].get('y', 0),
        gyroscope_z=data['gyroscope'].get('z', 0),
        location=location,
        timestamp=datetime.fromisoformat(data.get('timestamp', datetime.utcnow().isoformat())),
        processed=False
    )
    
    db.session.add(new_sensor_data)
    
    # Update vehicle location
    vehicle.location = location
    vehicle.last_updated = datetime.utcnow()
    
    # Process gyroscope data to detect potential hazards
    if detect_pothole(data['gyroscope']):
        # Create a new hazard report if significant movement detected
        new_hazard = Hazard(
            type='pothole',
            severity='medium',  # Default severity, can be adjusted based on gyroscope intensity
            location=location,
            reported_by=f'vehicle_{data["vehicle_id"]}',
            timestamp=datetime.utcnow(),
            status='detected',
            description='Automatically detected by vehicle sensors'
        )
        db.session.add(new_hazard)
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Sensor data received and processed',
        'sensor_data_id': new_sensor_data.id
    })

@sensor_bp.route('/sensor-data/<int:vehicle_id>', methods=['GET'])
def get_vehicle_sensor_data(vehicle_id):
    """Get sensor data for a specific vehicle."""
    # Validate vehicle exists
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    # Get sensor data for the vehicle
    sensor_data = SensorData.query.filter_by(vehicle_id=vehicle_id).order_by(SensorData.timestamp.desc()).limit(100).all()
    
    return jsonify([data.to_dict() for data in sensor_data])

def detect_pothole(gyroscope_data):
    """
    Detect potential potholes based on gyroscope data.
    This is a simplified algorithm that detects sudden vertical movements.
    In a real application, this would be more sophisticated.
    """
    # Extract gyroscope values
    x = gyroscope_data.get('x', 0)
    y = gyroscope_data.get('y', 0)
    z = gyroscope_data.get('z', 0)
    
    # Calculate magnitude of movement
    magnitude = np.sqrt(x**2 + y**2 + z**2)
    
    # Check if vertical movement (z-axis) is significant
    # and if the overall magnitude exceeds a threshold
    threshold = 1.5  # This threshold would be calibrated based on real-world testing
    
    return abs(z) > threshold and magnitude > threshold