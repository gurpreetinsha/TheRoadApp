import React, { useState } from 'react';

const HazardForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    type: 'pothole',
    description: '',
    severity: 'medium',
    latitude: '',
    longitude: ''
  });
  const [useCurrentLocation, setUseCurrentLocation] = useState(true);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let coords = {};
      
      if (useCurrentLocation) {
        // Get current location
        const position = await getCurrentPosition();
        coords = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        };
      } else {
        // Use manually entered coordinates
        coords = {
          latitude: parseFloat(formData.latitude),
          longitude: parseFloat(formData.longitude)
        };
      }

      // Validate coordinates
      if (isNaN(coords.latitude) || isNaN(coords.longitude)) {
        throw new Error('Invalid coordinates. Please check your input or allow location access.');
      }

      // Submit the hazard report
      await onSubmit({
        ...formData,
        latitude: coords.latitude,
        longitude: coords.longitude
      });

      // Reset form
      setFormData({
        type: 'pothole',
        description: '',
        severity: 'medium',
        latitude: '',
        longitude: ''
      });
    } catch (error) {
      console.error('Error submitting hazard:', error);
      alert(error.message || 'Failed to submit hazard report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Promise wrapper for geolocation API
  const getCurrentPosition = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported by your browser'));
        return;
      }
      
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      });
    });
  };

  return (
    <div className="hazard-form">
      <h3>Report Road Hazard</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="type">Hazard Type</label>
          <select
            id="type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            required
          >
            <option value="pothole">Pothole</option>
            <option value="construction">Construction</option>
            <option value="accident">Accident</option>
            <option value="flooding">Flooding</option>
            <option value="debris">Debris on Road</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe the hazard..."
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="severity">Severity</label>
          <select
            id="severity"
            name="severity"
            value={formData.severity}
            onChange={handleChange}
            required
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={useCurrentLocation}
              onChange={() => setUseCurrentLocation(!useCurrentLocation)}
            />
            Use my current location
          </label>
        </div>

        {!useCurrentLocation && (
          <>
            <div className="form-group">
              <label htmlFor="latitude">Latitude</label>
              <input
                type="number"
                id="latitude"
                name="latitude"
                value={formData.latitude}
                onChange={handleChange}
                step="any"
                required={!useCurrentLocation}
              />
            </div>

            <div className="form-group">
              <label htmlFor="longitude">Longitude</label>
              <input
                type="number"
                id="longitude"
                name="longitude"
                value={formData.longitude}
                onChange={handleChange}
                step="any"
                required={!useCurrentLocation}
              />
            </div>
          </>
        )}

        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Report Hazard'}
        </button>
      </form>
    </div>
  );
};

export default HazardForm;