import { motion } from 'framer-motion';
import { useState } from 'react';

const IncidentCard = ({ incident, index }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getStatusColor = (status) => {
    const colors = {
      detected: 'text-yellow-400 bg-yellow-400/10 border-yellow-400/30',
      resolved: 'text-green-400 bg-green-400/10 border-green-400/30',
      investigating: 'text-blue-400 bg-blue-400/10 border-blue-400/30',
    };
    return colors[status] || colors.detected;
  };

  const getActionStatusColor = (status) => {
    const colors = {
      success: 'text-green-400',
      error: 'text-red-400',
      pending: 'text-yellow-400',
    };
    return colors[status] || 'text-gray-400';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      whileHover={{ scale: 1.02, y: -5 }}
      className="glass rounded-xl p-6 border border-dark-border hover:border-cyber-blue/50 transition-all duration-300 cursor-pointer"
      onClick={() => setIsExpanded(!isExpanded)}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <motion.div
              animate={{ rotate: isExpanded ? 180 : 0 }}
              transition={{ duration: 0.3 }}
              className="text-cyber-blue"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </motion.div>
            <h3 className="text-lg font-semibold text-white">{incident.issue}</h3>
          </div>
          <div className="flex items-center space-x-3 ml-8">
            <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(incident.status)}`}>
              {incident.status.toUpperCase()}
            </span>
            {incident.action_taken && (
              <span className="text-xs text-gray-400">
                Action: <span className={getActionStatusColor(incident.action_status)}>{incident.action_taken}</span>
              </span>
            )}
          </div>
        </div>

        {/* Status Icon */}
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="w-12 h-12 rounded-lg bg-gradient-to-br from-cyber-blue/20 to-cyber-purple/20 flex items-center justify-center border border-cyber-blue/30"
        >
          <svg className="w-6 h-6 text-cyber-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </motion.div>
      </div>

      {/* Expanded Content */}
      <motion.div
        initial={false}
        animate={{ height: isExpanded ? 'auto' : 0, opacity: isExpanded ? 1 : 0 }}
        transition={{ duration: 0.3 }}
        className="overflow-hidden"
      >
        <div className="space-y-4 pt-4 border-t border-dark-border">
          {/* AI Diagnosis */}
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <svg className="w-5 h-5 text-cyber-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <h4 className="text-sm font-semibold text-cyber-purple">AI Diagnosis</h4>
            </div>
            <p className="text-sm text-gray-300 ml-7 bg-cyber-purple/5 p-3 rounded-lg border border-cyber-purple/20">
              {incident.cause || 'Analyzing...'}
            </p>
          </div>

          {/* Solution */}
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h4 className="text-sm font-semibold text-green-400">Recommended Solution</h4>
            </div>
            <p className="text-sm text-gray-300 ml-7 bg-green-400/5 p-3 rounded-lg border border-green-400/20">
              {incident.solution || 'Generating solution...'}
            </p>
          </div>

          {/* Remediation Action */}
          {incident.action_taken && (
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <svg className="w-5 h-5 text-cyber-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <h4 className="text-sm font-semibold text-cyber-blue">Auto-Remediation</h4>
              </div>
              <div className="ml-7 bg-cyber-blue/5 p-3 rounded-lg border border-cyber-blue/20">
                <p className="text-sm text-gray-300">
                  Action: <span className="font-medium text-white">{incident.action_taken}</span>
                </p>
                <p className="text-sm text-gray-300 mt-1">
                  Status: <span className={`font-medium ${getActionStatusColor(incident.action_status)}`}>
                    {incident.action_status}
                  </span>
                </p>
              </div>
            </div>
          )}

          {/* Timestamp */}
          {incident.created_at && (
            <div className="text-xs text-gray-500 ml-7">
              Detected: {new Date(incident.created_at).toLocaleString()}
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

export default IncidentCard;
