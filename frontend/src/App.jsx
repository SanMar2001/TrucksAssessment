import { useEffect, useState } from "react";
import { testBackend } from "./api/backend";
import MapView from "./components/MapView";
import RouteForm from './components/RouteForm';

function App() {
  const [message, setMessage] = useState("Loading...");
  const [routeGeojson, setRouteGeojson] = useState(null);

  useEffect(() => {
    async function checkBackend() {
      try {
        const data = await testBackend();
        setMessage(data.message);
      } catch (error) {
        setMessage("Error connecting to backend");
        console.error(error);
      }
    }
    checkBackend();
  }, []);

  return (
    <div>
      <h1>Route Planner</h1>
      <p>{message}</p>

      {}
      <MapView routeGeojson={routeGeojson} />

      {}
      <RouteForm setRouteGeojson={setRouteGeojson} />
    </div>
  );
}

export default App;