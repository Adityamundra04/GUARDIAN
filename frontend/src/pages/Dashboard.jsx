import { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import IncidentList from '../components/IncidentList';
import MonitoringPanel from '../components/MonitoringPanel';
import { api } from '../services/api';

const Dashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [backendConnected, setBackendConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [systemStatus, setSystemStatus] = useState({
    kubernetes: 'offline',
    prometheus: 'offline',
    aiEngine: 'offline',
    remediation: 'offline',
  });

  // Use ref to track if component is mounted
  const isMounted = useRef(true);

  // Fetch incidents with better error handling
  const fetchIncidents = useCallback(async (isInitialLoad = false) => {
    try {
      if (isInitialLoad) {
        setLoading(true);
      }
      
      const data = await api.getIncidents();
      
      if (isMounted.current) {
        setIncidents(data);
        setError(null);
        setBackendConnected(true);
        setLastUpdate(new Date());
      }
    } catch (err) {
      console.error('Failed to fetch incidents:', err);
      if (isMounted.current) {
        setError('Failed to connect to Guardian backend. Please ensure the backend is running on http://127.0.0.1:8000');
        setBackendConnected(false);
      }
    } finally {
      if (isMounted.current && isInitialLoad) {
        setLoading(false);
      }
    }
  }, []);

  // Check system health
  const checkHealth = useCallback(async () => {
    try {
      const healthData = await api.getHealth();
      
      if (isMounted.current) {
        // If health check succeeds, assume all systems are online
        setSystemStatus({
          kubernetes: 'online',
          prometheus: 'online',
          aiEngine: 'online',
          remediation: 'online',
        });
        setBackendConnected(true);
      }
    } catch (err) {
      console.error('Health check failed:', err);
      if (isMounted.current) {
        setSystemStatus({
          kubernetes: 'offline',
          prometheus: 'offline',
          aiEngine: 'offline',
          remediation: 'offline',
        });
        setBackendConnected(false);
      }
    }
  }, []);

  // Test backend connection
  const testConnection = useCallback(async () => {
    try {
      await api.getRoot();
      console.log('Backend connection successful');
      setBackendConnected(true);
    } catch (err) {
      console.error('Backend connection failed:', err);
      setBackendConnected(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    console.log('Dashboard mounted - initializing...');
    testConnection();
    fetchIncidents(true);
    checkHealth();

    return () => {
      isMounted.current = false;
    };
  }, [testConnection, fetchIncidents, checkHealth]);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    console.log('Setting up auto-refresh (5 seconds)');
    
    const interval = setInterval(() => {
      console.log('Auto-refresh triggered');
      fetchIncidents(false);
      checkHealth();
    }, 5000);

    return () => {
      console.log('Cleaning up auto-refresh');
      clearInterval(interval);
    };
  }, [fetchIncidents, checkHealth]);

  // Calculate stats from real data
  const stats = {
    activeIncidents: incidents.filter(i => i.status === 'detected').length,
    resolvedIncidents: incidents.filter(i => i.status === 'resolved').length,
    autoRemediated: incidents.filter(i => i.action_taken && i.action_status === 'success').length,
    uptime: backendConnected ? '99.9%' : '0%',
  };

  // Manual refresh handler
  const handleManualRefresh = () => {
    console.log('Manual refresh triggered');
    fetchIncidents(false);
    checkHealth();
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
        <Navbar systemStatus={systemStatus} backendConnected={backendConnected} />

        <div className="pt-24">
          <Hero stats={stats} />

          {/* Connection Status Banner */}
          <AnimatePresence>
            {!backendConnected && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="max-w-7xl mx-auto px-6 mb-6"
              >
                <div className="glass rounded-xl p-4 border border-red-500/30 bg-red-500/10">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <motion.div
                        animate={{ scale: [1, 1.2, 1] }}
                        transition={{ duration: 1, repeat: Infinity }}
                      >
                        <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </motion.div>
                      <div>
                        <p className="text-red-400 font-semibold">Backend Connection Lost</p>
                        <p className="text-red-300 text-sm">Ensure Guardian backend is running on http://127.0.0.1:8000</p>
                      </div>
                    </div>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={testConnection}
                      className="px-4 py-2 rounded-lg bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 transition-all duration-300"
                    >
                      Retry Connection
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Error Banner */}
          <AnimatePresence>
            {error && backendConnected && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="max-w-7xl mx-auto px-6 mb-6"
              >
                <div className="glass rounded-xl p-4 border border-yellow-500/30 bg-yellow-500/10">
                  <div className="flex items-center space-x-3">
                    <svg className="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <p className="text-yellow-400">{error}</p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

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
                      <div className="flex items-center space-x-2">
                        <p className="text-gray-400">Real-time Kubernetes issue detection</p>
                        {lastUpdate && (
                          <span className="text-xs text-gray-500">
                            • Updated {lastUpdate.toLocaleTimeString()}
                          </span>
                        )}
                      </div>
                    </div>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleManualRefresh}
                      disabled={!backendConnected}
                      className={`px-4 py-2 rounded-lg border transition-all duration-300 ${
                        backendConnected
                          ? 'bg-cyber-blue/10 text-cyber-blue border-cyber-blue/30 hover:bg-cyber-blue/20'
                          : 'bg-gray-700/10 text-gray-500 border-gray-700/30 cursor-not-allowed'
                      }`}
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
                  <MonitoringPanel systemStatus={systemStatus} backendConnected={backendConnected} />
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
