import React from 'react';
import { VegaLite } from 'react-vega';
import { useAuth0 } from '@auth0/auth0-react';

const sampleSpec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "Sample timeline placeholder",
  "data": {
    "values": [
      {"date": "1900-01-01", "event": "Start of 20th century"},
      {"date": "1914-07-28", "event": "World War I begins"},
      {"date": "1939-09-01", "event": "World War II begins"},
      {"date": "1969-07-20", "event": "Moon landing"}
    ]
  },
  "mark": "point",
  "encoding": {
    "x": {"field": "date", "type": "temporal", "title": "Date"},
    "y": {"field": "event", "type": "nominal", "title": "Event"},
    "tooltip": [{"field": "event", "type": "nominal"}]
  }
};

export default function App() {
  const { loginWithRedirect, logout, isAuthenticated, user, isLoading } = useAuth0();

  return (
    <div style={{ padding: '2rem' }}>
      <h1>EchoPlex Explorer</h1>
      {isLoading && <p>Loading auth…</p>}
      {isAuthenticated ? (
        <>
          <p>Welcome, {user?.name || user?.email}</p>
          <button onClick={() => logout({ returnTo: window.location.origin })}>Logout</button>
        </>
      ) : (
        <button onClick={() => loginWithRedirect()}>Login</button>
      )}
      <h2>Timeline Demo</h2>
      <VegaLite spec={sampleSpec} />
    </div>
  );
}
