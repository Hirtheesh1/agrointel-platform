import React from 'react';
import { motion } from 'framer-motion';
import { Badge } from '../components/ui/Badge';
import { AlertTriangle, Droplets, ThermometerSun, AlertCircle } from 'lucide-react';

const mockAlerts = [
  {
    id: 1,
    type: 'drought',
    title: 'High Drought Probability',
    message: 'Coimbatore region is showing a 68% probability of drought conditions developing over the next 14 days due to sustained heat and low soil moisture.',
    severity: 'warning',
    time: '2 hours ago',
    icon: ThermometerSun,
  },
  {
    id: 2,
    type: 'irrigation',
    title: 'Critical Irrigation Demand',
    message: 'Erode region requires immediate irrigation. Forecasted demand has exceeded 20mm/day threshold.',
    severity: 'danger',
    time: '5 hours ago',
    icon: Droplets,
  },
  {
    id: 3,
    type: 'system',
    title: 'Model Retraining Required',
    message: 'Data drift detected in Trichy humidity sensors. Automatic retraining pipeline scheduled for midnight.',
    severity: 'info',
    time: '1 day ago',
    icon: AlertCircle,
  }
];

export const Alerts = () => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-text-primary">Intelligence Alerts</h2>
          <p className="text-slate-400 mt-1">AI-generated warnings and system notifications</p>
        </div>
      </div>

      <div className="space-y-4">
        {mockAlerts.map((alert) => (
          <div key={alert.id} className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm flex items-start">
            <div className={`p-3 rounded-xl mr-4 ${
              alert.severity === 'danger' ? 'bg-red-500/10 text-red-500 border border-red-500/20' :
              alert.severity === 'warning' ? 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20' :
              'bg-blue-500/10 text-blue-500 border border-blue-500/20'
            }`}>
              <alert.icon className="h-6 w-6" />
            </div>
            <div className="flex-1">
              <div className="flex items-center justify-between mb-1">
                <h3 className="text-lg font-medium text-text-primary">{alert.title}</h3>
                <span className="text-sm text-slate-500">{alert.time}</span>
              </div>
              <p className="text-slate-400 text-sm mb-3">{alert.message}</p>
              <div className="flex gap-2">
                <Badge variant={alert.severity as any}>
                  {alert.severity.toUpperCase()}
                </Badge>
                <Badge variant="default">
                  {alert.type.toUpperCase()}
                </Badge>
              </div>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
};
