import { motion } from 'framer-motion';

const Hero = ({ stats }) => {
  return (
    <div className="relative overflow-hidden py-20">
      {/* Animated background gradient */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyber-blue rounded-full filter blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-cyber-purple rounded-full filter blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
      </div>

      <div className="relative max-w-7xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <motion.h1
            className="text-6xl md:text-7xl font-bold mb-6"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <span className="gradient-text">Autonomous AI Ops</span>
            <br />
            <span className="text-white">Platform</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto"
          >
            Real-time Kubernetes monitoring with AI-powered diagnosis and automated remediation
          </motion.p>

          {/* Stats Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-5xl mx-auto"
          >
            <StatCard
              icon={
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              }
              label="Active Incidents"
              value={stats.activeIncidents}
              color="cyan"
              delay={0.7}
            />
            <StatCard
              icon={
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              }
              label="Resolved"
              value={stats.resolvedIncidents}
              color="green"
              delay={0.8}
            />
            <StatCard
              icon={
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              }
              label="Auto-Remediated"
              value={stats.autoRemediated}
              color="purple"
              delay={0.9}
            />
            <StatCard
              icon={
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              }
              label="System Uptime"
              value={stats.uptime}
              color="pink"
              delay={1.0}
            />
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value, color, delay }) => {
  const colorClasses = {
    cyan: 'from-cyber-blue/20 to-cyber-blue/5 border-cyber-blue/30 text-cyber-blue',
    green: 'from-green-500/20 to-green-500/5 border-green-500/30 text-green-400',
    purple: 'from-cyber-purple/20 to-cyber-purple/5 border-cyber-purple/30 text-cyber-purple',
    pink: 'from-cyber-pink/20 to-cyber-pink/5 border-cyber-pink/30 text-cyber-pink',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ scale: 1.05, y: -5 }}
      className={`glass rounded-xl p-6 border bg-gradient-to-br ${colorClasses[color]} backdrop-blur-xl`}
    >
      <div className="flex flex-col items-center space-y-3">
        <div className={colorClasses[color].split(' ')[3]}>
          {icon}
        </div>
        <div className="text-center">
          <div className="text-3xl font-bold text-white mb-1">{value}</div>
          <div className="text-sm text-gray-400">{label}</div>
        </div>
      </div>
    </motion.div>
  );
};

export default Hero;
