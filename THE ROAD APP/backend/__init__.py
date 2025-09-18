from flask import Flask
from flask_cors import CORS
from .config import config
from .models import db

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from .routes.vehicle_routes import vehicle_bp
    from .routes.hazard_routes import hazard_bp
    from .routes.sensor_routes import sensor_bp
    
    app.register_blueprint(vehicle_bp, url_prefix='/api')
    app.register_blueprint(hazard_bp, url_prefix='/api')
    app.register_blueprint(sensor_bp, url_prefix='/api')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app