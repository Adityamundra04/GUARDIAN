// Get API URL from environment variable or use default
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

console.log('Guardian API URL:', API_BASE_URL);

export const api = {
  // Get all incidents
  async getIncidents() {
    try {
      const response = await fetch(`${API_BASE_URL}/incidents`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to fetch incidents`);
      }
      
      const data = await response.json();
      console.log('Fetched incidents:', data.length);
      return data;
    } catch (error) {
      console.error('Error fetching incidents:', error);
      throw error;
    }
  },

  // Get health status
  async getHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to fetch health status`);
      }
      
      const data = await response.json();
      console.log('Health check:', data);
      return data;
    } catch (error) {
      console.error('Error fetching health:', error);
      throw error;
    }
  },

  // Get root endpoint (for connection test)
  async getRoot() {
    try {
      const response = await fetch(`${API_BASE_URL}/`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to connect to backend`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error connecting to backend:', error);
      throw error;
    }
  },

  // Create incident (for testing)
  async createIncident(incidentData) {
    try {
      const response = await fetch(`${API_BASE_URL}/incidents`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(incidentData),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Failed to create incident`);
      }
      
      const data = await response.json();
      console.log('Created incident:', data);
      return data;
    } catch (error) {
      console.error('Error creating incident:', error);
      throw error;
    }
  },
};
