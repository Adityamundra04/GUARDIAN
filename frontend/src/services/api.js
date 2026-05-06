const API_BASE_URL = 'http://127.0.0.1:8000';

export const api = {
  // Get all incidents
  async getIncidents() {
    try {
      const response = await fetch(`${API_BASE_URL}/incidents`);
      if (!response.ok) {
        throw new Error('Failed to fetch incidents');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching incidents:', error);
      throw error;
    }
  },

  // Get health status
  async getHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error('Failed to fetch health status');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching health:', error);
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
        },
        body: JSON.stringify(incidentData),
      });
      if (!response.ok) {
        throw new Error('Failed to create incident');
      }
      return await response.json();
    } catch (error) {
      console.error('Error creating incident:', error);
      throw error;
    }
  },
};
