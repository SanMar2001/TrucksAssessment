import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function MapView({ routeGeojson }) {
  // Centrar el mapa en la primera coordenada de la ruta o default en Bogotá
  const center = routeGeojson
    ? routeGeojson[0]
    : [4.711, -74.0721];

  return (
    <MapContainer center={center} zoom={6} style={{ height: "500px", width: "100%" }}>
      <TileLayer
        attribution="OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Dibuja la ruta si existe */}
      {routeGeojson && <Polyline positions={routeGeojson} color="blue" />}

      {/* Opcional: marcadores en inicio y fin */}
      {routeGeojson && (
        <>
          <Marker position={routeGeojson[0]}>
            <Popup>Current Location</Popup>
          </Marker>
          <Marker position={routeGeojson[routeGeojson.length - 1]}>
            <Popup>Dropoff Location</Popup>
          </Marker>
        </>
      )}
    </MapContainer>
  );
}

export default MapView;