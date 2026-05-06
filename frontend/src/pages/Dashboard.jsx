import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import IncidentList from '../components/IncidentList';
import MonitoringPanel from '../components/MonitoringPanel';
import { api } from '../services/api';

const Dashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [systemStatus, setSystemStatus] = useState({
    kubernetes: 'online',
    prometheus: 'online',
    aiEngine: 'online',
    remediation: 'online',
  });

  // Fetch incidents
  const fetchIncidents = async () => {
    try {
      const data = await api.getIncidents();
      setIncidents(data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch incidents:', err);
      setError('Failed to connect to Guardian backend');
    } finally {
      setLoading(false);
    }
  };

  // Check system health
  const checkHealth = async () => {
    try {
      await api.getHealth();
      setSystemStatus(prev => ({
        ...prev,
        kubernetes: 'online',
        prometheus: 'online',
        aiEngine: 'online',
        remediation: 'online',
      }));
    } catch (err) {
      console.error('Health check failed:', err);
    }
  };

  // Initial load
  useEffect(() => {
    fetchIncidents();
    checkHealth();
  }, []);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchIncidents();
      checkHealth();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  // Calculate stats
  const stats = {
    activeIncidents: incidents.filter(i => i.status === 'detected').length,
    resolvedIncidents: incidents.filter(i => i.status === 'resolved').length,
    autoRemediated: incidents.filter(i => i.action_taken && i.action_status === 'success').length,
    uptime: '99.9%',
  };

  return (
    <div className="min-h-screen bg-dark-bg">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-0 w-full h-full">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyber-blue/10 rounded-full filter blur-3xl animate-pulse-slow" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyber-purple/10 rounded-full filter blur-3xl animate-pulse-slow" style={{ animationDelay: '2s' }} />
          <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-cyber-pink/10 rounded-full filter blur-3xl animate-pulse-slow" style={{ animationDelay: '4s' }} />
        </div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        <Navbar systemStatus={systemStatus} />

        <div className="pt-24">
          <Hero stats={stats} />

          {/* Error Banner */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="max-w-7xl mx-auto px-6 mb-6"
            >
              <div className="glass rounded-xl p-4 border border-red-500/30 bg-red-500/10">
                <div className="flex items-center space-x-3">
                  <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-red-400">{error}</p>
                </div>
              </div>
            </motion.div>
          )}

          {/* Main Content */}
          <div className="max-w-7xl mx-auto px-6 pb-12">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Incidents Section */}
              <div className="lg:col-span-2 space-y-6">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <div className="flex items-center justify-between mb-6">
                    <div>
                      <h2 className="text-2xl font-bold text-white mb-1">Active Incidents</h2>
                      <p className="text-gray-400">Real-time Kubernetes issue detection</p>
                    </div>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={fetchIncidents}
                      className="px-4 py-2 rounded-lg bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/30 hover:bg-cyber-blue/20 transition-all duration-300"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    </motion.button>
                  </div>

                  <IncidentList incidents={incidents} loading={loading} />
                </motion.div>
              </div>

              {/* Monitoring Panel */}
              <div className="lg:col-span-1">
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="sticky top-24"
                >
                  <MonitoringPanel systemStatus={systemStatus} />
                </motion.div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
