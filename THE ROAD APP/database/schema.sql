-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create tables
CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    route VARCHAR(100),
    status VARCHAR(20) DEFAULT 'inactive',
    location GEOMETRY(Point, 4326),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hazards (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL,
    reported_by VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'reported',
    description TEXT,
    image_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id),
    gyroscope_x FLOAT,
    gyroscope_y FLOAT,
    gyroscope_z FLOAT,
    location GEOMETRY(Point, 4326),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- Create indexes for spatial queries
CREATE INDEX idx_vehicles_location ON vehicles USING GIST(location);
CREATE INDEX idx_hazards_location ON hazards USING GIST(location);
CREATE INDEX idx_sensor_data_location ON sensor_data USING GIST(location);

-- Create index for timestamp queries
CREATE INDEX idx_sensor_data_timestamp ON sensor_data(timestamp);
CREATE INDEX idx_hazards_timestamp ON hazards(timestamp);

-- Sample data for testing
INSERT INTO vehicles (name, type, route, status, location)
VALUES 
    ('Bus 101', 'bus', 'Downtown Express', 'active', ST_SetSRID(ST_MakePoint(-74.0060, 40.7128), 4326)),
    ('Bus 202', 'bus', 'Uptown Local', 'active', ST_SetSRID(ST_MakePoint(-74.0050, 40.7138), 4326));

INSERT INTO hazards (type, severity, location, reported_by, status, description)
VALUES 
    ('pothole', 'high', ST_SetSRID(ST_MakePoint(-74.0065, 40.7118), 4326), 'mobile_app', 'reported', 'Large pothole in the middle of the road');