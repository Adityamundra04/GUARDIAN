import { motion } from 'framer-motion';

const Navbar = ({ systemStatus, backendConnected = true }) => {
  return (
    <motion.nav
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 glass border-b border-dark-border"
    >
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-4">
            <motion.div
              animate={{ rotate: backendConnected ? 360 : 0 }}
              transition={{ duration: 20, repeat: backendConnected ? Infinity : 0, ease: "linear" }}
              className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyber-blue to-cyber-purple flex items-center justify-center"
            >
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </motion.div>
            <div>
              <h1 className="text-2xl font-bold gradient-text">Guardian</h1>
              <p className="text-xs text-gray-400">AI Ops Platform</p>
            </div>
          </div>

          {/* System Status */}
          <div className="flex items-center space-x-6">
            <StatusIndicator label="Kubernetes" status={systemStatus.kubernetes} />
            <StatusIndicator label="Prometheus" status={systemStatus.prometheus} />
            <StatusIndicator label="AI Engine" status={systemStatus.aiEngine} />
          </div>

          {/* Live Indicator */}
          <div className="flex items-center space-x-2">
            <motion.div
              animate={backendConnected ? { 
                scale: [1, 1.2, 1], 
                opacity: [1, 0.5, 1] 
              } : {}}
              transition={{ duration: 2, repeat: backendConnected ? Infinity : 0 }}
              className={`w-3 h-3 rounded-full ${backendConnected ? 'bg-green-500' : 'bg-red-500'}`}
            />
            <span className={`text-sm font-medium ${backendConnected ? 'text-green-400' : 'text-red-400'}`}>
              {backendConnected ? 'LIVE' : 'OFFLINE'}
            </span>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

const StatusIndicator = ({ label, status }) => {
  const normalizedStatus = String(status || '').trim().toLowerCase();
  const isOnline = ['online', 'ok', 'healthy'].includes(normalizedStatus);
  
  return (
    <div className="flex items-center space-x-2">
      <motion.div
        animate={isOnline ? { scale: [1, 1.2, 1] } : {}}
        transition={{ duration: 2, repeat: Infinity }}
        className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`}
      />
      <span className="text-sm text-gray-300">{label}</span>
    </div>
  );
};

export default Navbar;
