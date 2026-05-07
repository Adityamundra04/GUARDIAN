const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const normalizeIncidentsResponse = (data) => {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.incidents)) return data.incidents;
  return [];
};

export const api = {
  // Get all incidents
  async getIncidents() {
    const response = await fetch(`${API_BASE_URL}/incidents`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: Failed to fetch incidents`);
    }

    const data = await response.json();
    const incidents = normalizeIncidentsResponse(data);
    console.log('Fetched incidents:', incidents.length);
    return incidents;
  },

  // Get health status
  async getHealth() {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: Failed to fetch health status`);
    }

    const data = await response.json();
    console.log('Health check:', data);
    return data;
  },

  // Get root endpoint (for connection test)
  async getRoot() {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: Failed to connect to backend`);
    }

    return response.json();
  },

  // Create incident (for testing)
  async createIncident(incidentData) {
    const response = await fetch(`${API_BASE_URL}/incidents`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(incidentData),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: Failed to create incident`);
    }

    return response.json();
  },
};
