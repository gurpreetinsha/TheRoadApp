from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from datetime import datetime

db = SQLAlchemy()

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    route = db.Column(db.String(100))
    status = db.Column(db.String(20), default='inactive')
    location = db.Column(Geometry('POINT', srid=4326))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'route': self.route,
            'status': self.status,
            'location': {
                'lng': self.location.x if self.location else None,
                'lat': self.location.y if self.location else None
            },
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class Hazard(db.Model):
    __tablename__ = 'hazards'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    location = db.Column(Geometry('POINT', srid=4326), nullable=False)
    reported_by = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='reported')
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'severity': self.severity,
            'location': {
                'lng': self.location.x if self.location else None,
                'lat': self.location.y if self.location else None
            },
            'reported_by': self.reported_by,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'status': self.status,
            'description': self.description,
            'image_url': self.image_url
        }

class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    gyroscope_x = db.Column(db.Float)
    gyroscope_y = db.Column(db.Float)
    gyroscope_z = db.Column(db.Float)
    location = db.Column(Geometry('POINT', srid=4326))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)
    
    vehicle = db.relationship('Vehicle', backref=db.backref('sensor_data', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'gyroscope_x': self.gyroscope_x,
            'gyroscope_y': self.gyroscope_y,
            'gyroscope_z': self.gyroscope_z,
            'location': {
                'lng': self.location.x if self.location else None,
                'lat': self.location.y if self.location else None
            },
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'processed': self.processed
        }