import { useEffect, useState } from "react";
import { checkHealth } from "./services/api";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [error, setError] = useState("");

  useEffect(() => {
    checkHealth()
      .then((data) => {
        console.log("Backend data:", data);
        setBackendStatus("Backend connected ✅");
      })
      .catch((error) => {
        console.error("Health check failed:", error);
        setBackendStatus("Backend unavailable ❌");
        setError(error.message);
      });
  }, []);

  return (
    <main>
      <h1>AI PDF Assistant</h1>

      <p>{backendStatus}</p>

      {error && (
        <p>
          Error: {error}
        </p>
      )}
    </main>
  );
}

export default App;