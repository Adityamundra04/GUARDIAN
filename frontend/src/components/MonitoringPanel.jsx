import { motion } from 'framer-motion';

const MonitoringPanel = ({ systemStatus, backendConnected = true }) => {
  return (
    <div className="glass rounded-xl p-6 border border-dark-border">
      <div className="flex items-center space-x-3 mb-6">
        <motion.div
          animate={backendConnected ? { rotate: 360 } : {}}
          transition={{ duration: 3, repeat: backendConnected ? Infinity : 0, ease: "linear" }}
          className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyber-blue/20 to-cyber-purple/20 flex items-center justify-center border border-cyber-blue/30"
        >
          <svg className="w-6 h-6 text-cyber-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </motion.div>
        <div>
          <h2 className="text-xl font-bold text-white">Live Monitoring</h2>
          <p className="text-sm text-gray-400">System Components Status</p>
        </div>
      </div>

      <div className="space-y-4">
        <ServiceStatus
          name="Kubernetes Cluster"
          status={systemStatus.kubernetes}
          description="Monitoring pods and deployments"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
            </svg>
          }
        />

        <ServiceStatus
          name="Prometheus"
          status={systemStatus.prometheus}
          description="Collecting metrics and alerts"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          }
        />

        <ServiceStatus
          name="AI Engine"
          status={systemStatus.aiEngine}
          description="Analyzing and diagnosing issues"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          }
        />

        <ServiceStatus
          name="Auto-Remediation"
          status={systemStatus.remediation}
          description="OpenClaw action executor"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          }
        />
      </div>

      {/* System Health Bar */}
      <div className="mt-6 pt-6 border-t border-dark-border">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">Backend Connection</span>
          <span className={`text-sm font-semibold ${backendConnected ? 'text-green-400' : 'text-red-400'}`}>
            {backendConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        <div className="h-2 bg-gray-700/50 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: backendConnected ? '100%' : '0%' }}
            transition={{ duration: 1 }}
            className={`h-full rounded-full ${
              backendConnected 
                ? 'bg-gradient-to-r from-green-500 to-cyber-blue' 
                : 'bg-gradient-to-r from-red-500 to-red-700'
            }`}
          />
        </div>
      </div>
    </div>
  );
};

const ServiceStatus = ({ name, status, description, icon }) => {
  const normalizedStatus = String(status || '').trim().toLowerCase();
  const isOnline = ['online', 'ok', 'healthy'].includes(normalizedStatus);

  return (
    <motion.div
      whileHover={{ scale: 1.02, x: 5 }}
      className="flex items-center space-x-4 p-4 rounded-lg bg-dark-card/50 border border-dark-border hover:border-cyber-blue/30 transition-all duration-300"
    >
      <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
        isOnline 
          ? 'bg-green-500/10 text-green-400 border border-green-500/30' 
          : 'bg-red-500/10 text-red-400 border border-red-500/30'
      }`}>
        {icon}
      </div>

      <div className="flex-1">
        <div className="flex items-center space-x-2 mb-1">
          <h3 className="text-sm font-semibold text-white">{name}</h3>
          <motion.div
            animate={isOnline ? { scale: [1, 1.2, 1] } : {}}
            transition={{ duration: 2, repeat: Infinity }}
            className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`}
          />
        </div>
        <p className="text-xs text-gray-400">{description}</p>
      </div>

      <div className={`px-3 py-1 rounded-full text-xs font-medium ${
        isOnline 
          ? 'bg-green-500/10 text-green-400 border border-green-500/30' 
          : 'bg-red-500/10 text-red-400 border border-red-500/30'
      }`}>
        {isOnline ? 'ONLINE' : 'OFFLINE'}
      </div>
    </motion.div>
  );
};

export default MonitoringPanel;
