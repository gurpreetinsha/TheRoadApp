from flask import Blueprint, jsonify, request
from ..models import db, Hazard
from geoalchemy2.elements import WKTElement
from datetime import datetime

hazard_bp = Blueprint('hazards', __name__)

@hazard_bp.route('/hazards', methods=['GET'])
def get_hazards():
    """Get all hazards."""
    hazards = Hazard.query.all()
    return jsonify([hazard.to_dict() for hazard in hazards])

@hazard_bp.route('/hazards/<int:hazard_id>', methods=['GET'])
def get_hazard(hazard_id):
    """Get a specific hazard by ID."""
    hazard = Hazard.query.get_or_404(hazard_id)
    return jsonify(hazard.to_dict())

@hazard_bp.route('/hazards', methods=['POST'])
def create_hazard():
    """Create a new hazard report."""
    data = request.json
    
    # Validate required fields
    required_fields = ['type', 'severity', 'location', 'reported_by']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create location point from coordinates
    location = None
    if 'location' in data and 'lat' in data['location'] and 'lng' in data['location']:
        location = WKTElement(f"POINT({data['location']['lng']} {data['location']['lat']})", srid=4326)
    else:
        return jsonify({'error': 'Invalid location format'}), 400
    
    # Create new hazard
    new_hazard = Hazard(
        type=data['type'],
        severity=data['severity'],
        location=location,
        reported_by=data['reported_by'],
        timestamp=datetime.fromisoformat(data.get('timestamp', datetime.utcnow().isoformat())),
        status=data.get('status', 'reported'),
        description=data.get('description'),
        image_url=data.get('image_url')
    )
    
    db.session.add(new_hazard)
    db.session.commit()
    
    return jsonify(new_hazard.to_dict()), 201

@hazard_bp.route('/hazards/<int:hazard_id>', methods=['PUT'])
def update_hazard(hazard_id):
    """Update a hazard."""
    hazard = Hazard.query.get_or_404(hazard_id)
    data = request.json
    
    # Update fields
    if 'type' in data:
        hazard.type = data['type']
    if 'severity' in data:
        hazard.severity = data['severity']
    if 'status' in data:
        hazard.status = data['status']
    if 'description' in data:
        hazard.description = data['description']
    if 'image_url' in data:
        hazard.image_url = data['image_url']
    
    # Update location if provided
    if 'location' in data and 'lat' in data['location'] and 'lng' in data['location']:
        hazard.location = WKTElement(f"POINT({data['location']['lng']} {data['location']['lat']})", srid=4326)
    
    db.session.commit()
    return jsonify(hazard.to_dict())

@hazard_bp.route('/hazards/<int:hazard_id>', methods=['DELETE'])
def delete_hazard(hazard_id):
    """Delete a hazard."""
    hazard = Hazard.query.get_or_404(hazard_id)
    db.session.delete(hazard)
    db.session.commit()
    return jsonify({'message': 'Hazard deleted successfully'})

@hazard_bp.route('/hazards/nearby', methods=['GET'])
def get_nearby_hazards():
    """Get hazards near a specific location."""
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = float(request.args.get('radius', 1.0))  # km
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid location parameters'}), 400
    
    # Convert radius from km to degrees (approximate)
    radius_degrees = radius / 111.0
    
    # Query for hazards within radius
    point = WKTElement(f'POINT({lng} {lat})', srid=4326)
    nearby_hazards = Hazard.query.filter(
        Hazard.location.ST_DWithin(point, radius_degrees)
    ).all()
    
    return jsonify([hazard.to_dict() for hazard in nearby_hazards])