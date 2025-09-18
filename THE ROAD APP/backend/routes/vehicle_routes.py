from flask import Blueprint, jsonify, request
from ..models import db, Vehicle
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
import json

vehicle_bp = Blueprint('vehicles', __name__)

@vehicle_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    """Get all vehicles."""
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.to_dict() for vehicle in vehicles])

@vehicle_bp.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """Get a specific vehicle by ID."""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify(vehicle.to_dict())

@vehicle_bp.route('/vehicles', methods=['POST'])
def create_vehicle():
    """Create a new vehicle."""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create location point from coordinates if provided
    location = None
    if 'location' in data and 'lat' in data['location'] and 'lng' in data['location']:
        location = WKTElement(f"POINT({data['location']['lng']} {data['location']['lat']})", srid=4326)
    
    # Create new vehicle
    new_vehicle = Vehicle(
        name=data['name'],
        type=data['type'],
        route=data.get('route'),
        status=data.get('status', 'inactive'),
        location=location
    )
    
    db.session.add(new_vehicle)
    db.session.commit()
    
    return jsonify(new_vehicle.to_dict()), 201

@vehicle_bp.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    """Update a vehicle."""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.json
    
    # Update fields
    if 'name' in data:
        vehicle.name = data['name']
    if 'type' in data:
        vehicle.type = data['type']
    if 'route' in data:
        vehicle.route = data['route']
    if 'status' in data:
        vehicle.status = data['status']
    
    # Update location if provided
    if 'location' in data and 'lat' in data['location'] and 'lng' in data['location']:
        vehicle.location = WKTElement(f"POINT({data['location']['lng']} {data['location']['lat']})", srid=4326)
    
    db.session.commit()
    return jsonify(vehicle.to_dict())

@vehicle_bp.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """Delete a vehicle."""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted successfully'})