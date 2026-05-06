import { motion } from 'framer-motion';
import IncidentCard from './IncidentCard';

const IncidentList = ({ incidents, loading }) => {
  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }

  if (incidents.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass rounded-xl p-12 text-center border border-dark-border"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
          className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-cyber-blue/20 to-cyber-purple/20 flex items-center justify-center border border-cyber-blue/30"
        >
          <svg className="w-10 h-10 text-cyber-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </motion.div>
        <h3 className="text-2xl font-bold text-white mb-2">All Systems Operational</h3>
        <p className="text-gray-400">No incidents detected. Guardian is monitoring your infrastructure.</p>
      </motion.div>
    );
  }

  return (
    <div className="space-y-4">
      {incidents.map((incident, index) => (
        <IncidentCard key={incident.id} incident={incident} index={index} />
      ))}
    </div>
  );
};

const SkeletonCard = () => {
  return (
    <div className="glass rounded-xl p-6 border border-dark-border animate-pulse">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1 space-y-3">
          <div className="h-6 bg-gray-700/50 rounded w-3/4" />
          <div className="h-4 bg-gray-700/50 rounded w-1/4" />
        </div>
        <div className="w-12 h-12 bg-gray-700/50 rounded-lg" />
      </div>
    </div>
  );
};

export default IncidentList;
