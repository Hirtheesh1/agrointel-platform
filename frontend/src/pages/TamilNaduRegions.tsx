import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { fetchFarms } from '../api';
import { useAppStore } from '../store';
import { MapPin, Navigation, Satellite, CheckCircle } from 'lucide-react';
import { GeoAnalyticsPanel } from '../components/geospatial/GeoAnalyticsPanel';

export const TamilNaduRegions = () => {
  const { data: farms } = useQuery({
    queryKey: ['farms'],
    queryFn: fetchFarms,
  });

  const { selectedFarm, setSelectedFarm } = useAppStore();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-text-primary">Tamil Nadu Geo Intelligence</h2>
          <p className="text-slate-400 mt-1">Precision microclimate · Farm-specific spatial analysis · Village-level insights</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-2 rounded-lg">
          <Satellite className="h-4 w-4" />
          {farms?.length || 0} Agricultural Zones Active
        </div>
      </div>

      {/* Farm Selection Grid */}
      <div>
        <p className="text-sm text-slate-500 mb-3 uppercase tracking-wider">Select a Farm Zone to Analyze</p>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {farms?.map((farm) => (
            <div
              key={farm.id}
              className={`rounded-xl border transition-all cursor-pointer ${
                selectedFarm?.id === farm.id
                  ? 'border-emerald-500/50 bg-emerald-900/20 shadow-md shadow-emerald-500/10'
                  : 'border-slate-800 bg-surface hover:border-slate-700 hover:bg-slate-800/50'
              } p-5`}
              onClick={() => setSelectedFarm(farm)}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${selectedFarm?.id === farm.id ? 'bg-emerald-500/20' : 'bg-slate-800'}`}>
                    <MapPin className={`h-4 w-4 ${selectedFarm?.id === farm.id ? 'text-emerald-400' : 'text-slate-400'}`} />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-text-primary">{farm.location_name}</h3>
                    <p className="text-xs text-slate-400">{farm.farm_name}</p>
                  </div>
                </div>
                {selectedFarm?.id === farm.id && (
                  <CheckCircle className="h-4 w-4 text-emerald-400 flex-shrink-0" />
                )}
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/50 grid grid-cols-2 gap-2">
                <div>
                  <p className="text-[10px] text-slate-500 uppercase tracking-wide">Soil</p>
                  <p className="text-xs text-slate-300 font-medium">{farm.soil_type || '—'}</p>
                </div>
                <div>
                  <p className="text-[10px] text-slate-500 uppercase tracking-wide">Size</p>
                  <p className="text-xs text-slate-300 font-medium">{farm.farm_size ? `${farm.farm_size} acres` : '—'}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-[10px] text-slate-500 uppercase tracking-wide">Coordinates</p>
                  <p className="text-xs text-slate-300 font-mono flex items-center gap-1 mt-0.5">
                    <Navigation className="h-3 w-3" />
                    {farm.latitude?.toFixed(4)}°N, {farm.longitude?.toFixed(4)}°E
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Geospatial Intelligence Panel */}
      <GeoAnalyticsPanel />
    </motion.div>
  );
};

