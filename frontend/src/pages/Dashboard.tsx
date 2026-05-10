import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchFarms } from '../api';
import { StatCard } from '../components/cards/StatCard';
import { Droplets, ThermometerSun, AlertTriangle, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { useAppStore } from '../store';
import { GeoAnalyticsPanel } from '../components/geospatial/GeoAnalyticsPanel';

export const Dashboard = () => {
  const { data: farms, isLoading } = useQuery({
    queryKey: ['farms'],
    queryFn: fetchFarms,
  });

  const { setSelectedFarm } = useAppStore();

  // Set default farm if none selected
  useEffect(() => {
    if (farms && farms.length > 0) {
      setSelectedFarm(farms[0]);
    }
  }, [farms, setSelectedFarm]);

  if (isLoading) {
    return <div className="flex h-full items-center justify-center text-slate-400">Loading AI Intelligence...</div>;
  }

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-text-primary">Regional Intelligence Overview</h2>
          <p className="text-slate-400 mt-1">Live monitoring across {farms?.length || 0} Tamil Nadu agricultural zones.</p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Avg Irrigation Demand"
          value="14.2 mm"
          icon={Droplets}
          trend={{ value: 2.4, isPositive: true }}
          description="Next 24 hours forecast"
        />
        <StatCard
          title="Environmental Risk"
          value="Low"
          icon={ThermometerSun}
          trend={{ value: 12, isPositive: false }}
          description="Heat stress probability"
        />
        <StatCard
          title="Active Alerts"
          value="2"
          icon={AlertTriangle}
          className="border-yellow-500/30"
          description="Requires attention"
        />
        <StatCard
          title="System Status"
          value="Healthy"
          icon={CheckCircle}
          className="border-green-500/30 text-green-500"
          description="TFT Model Synced"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <h3 className="text-lg font-medium text-text-primary mb-4">Latest Explainable AI Insights</h3>
          <div className="space-y-4">
            <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-primary-400">Coimbatore Region</span>
                <span className="text-xs bg-slate-700 px-2 py-1 rounded text-slate-300">2 hours ago</span>
              </div>
              <p className="text-sm text-slate-300">
                "The forecast is primarily driven by recent changes in temperature and heavily influenced by historical evaporation_index patterns over the past 168-hour observation window."
              </p>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <h3 className="text-lg font-medium text-text-primary mb-4">Monitored Regions</h3>
          <div className="overflow-hidden">
            <table className="min-w-full divide-y divide-slate-800">
              <thead>
                <tr>
                  <th className="py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Region</th>
                  <th className="py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Crop Type</th>
                  <th className="py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {farms?.map((farm) => (
                  <tr key={farm.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 text-sm font-medium text-slate-200">{farm.location_name}</td>
                    <td className="py-3 text-sm text-slate-400">{farm.farm_name}</td>
                    <td className="py-3 text-right text-sm">
                      <span className="inline-flex items-center rounded-full bg-green-500/10 px-2 py-1 text-xs font-medium text-green-400 border border-green-500/20">
                        Monitoring
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div className="mt-6">
        <GeoAnalyticsPanel />
      </div>

    </motion.div>
  );
};
