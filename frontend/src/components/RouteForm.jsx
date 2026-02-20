import { useState } from 'react';
import { submitInputs } from '../api/backend';

export default function RouteForm({ setRouteGeojson }) {
  const [currentLocation, setCurrentLocation] = useState('');
  const [pickupLocation, setPickupLocation] = useState('');
  const [dropoffLocation, setDropoffLocation] = useState('');
  const [cycleUsedHours, setCycleUsedHours] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const data = {
      currentLocation,
      pickupLocation,
      dropoffLocation,
      cycleUsedHours: parseInt(cycleUsedHours, 10) || 0, // <-- cambiado a entero
    };

    try {
      const result = await submitInputs(data);
      setResponseData(result);

      // Convierte OSRM geojson de lon,lat a lat,lon para Leaflet
      const routeCoords = result.routes[0].geometry.coordinates.map(
        ([lon, lat]) => [lat, lon]
      );

      setRouteGeojson(routeCoords);

    } catch (err) {
      setError(err.message || "Error submitting data");
      setResponseData(null);
      setRouteGeojson(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Current Location:
          <input
            type="text"
            value={currentLocation}
            onChange={(e) => setCurrentLocation(e.target.value)}
            required
          />
        </label>

        <label>
          Pickup Location:
          <input
            type="text"
            value={pickupLocation}
            onChange={(e) => setPickupLocation(e.target.value)}
            required
          />
        </label>

        <label>
          Dropoff Location:
          <input
            type="text"
            value={dropoffLocation}
            onChange={(e) => setDropoffLocation(e.target.value)}
            required
          />
        </label>

        <label>
          Current Cycle Used (Hrs):
          <input
            type="number"
            value={cycleUsedHours}
            onChange={(e) => setCycleUsedHours(e.target.value)}
            min="0"
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {responseData && (
        <pre style={{ background: '#f0f0f0', padding: '10px' }}>
          {JSON.stringify(responseData, null, 2)}
        </pre>
      )}
    </div>
  );
}