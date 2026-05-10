import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { Tractor, RefreshCw, MapPin, Leaf, CheckCircle } from 'lucide-react';
import axios from 'axios';
import { useAppStore } from '../store';
import { FarmInsightsPanel } from '../components/farm_management/FarmInsightsPanel';
import { CropRecommendationDashboard } from '../components/farm_management/CropRecommendationDashboard';
import { IrrigationAdvisor } from '../components/farm_management/IrrigationAdvisor';
import { SeasonalForecastPanel } from '../components/farm_management/SeasonalForecastPanel';
import { FarmTimeline } from '../components/farm_management/FarmTimeline';
import { YieldProjectionPanel } from '../components/farm_management/YieldProjectionPanel';

const API = 'http://localhost:8000/api/v1';

// Tab definitions
type Tab = 'overview' | 'crops' | 'irrigation' | 'forecast' | 'timeline';
const TABS: { id: Tab; label: string }[] = [
  { id: 'overview',   label: 'Overview' },
  { id: 'crops',      label: 'Crop Advisor' },
  { id: 'irrigation', label: 'Irrigation' },
  { id: 'forecast',   label: 'Seasonal Forecast' },
  { id: 'timeline',   label: 'Farm Timeline' },
];

export const FarmManagement = () => {
  const { selectedFarm, setSelectedFarm } = useAppStore();
  const [activeTab, setActiveTab] = useState<Tab>('overview');

  // Fetch list of farms
  const { data: farms } = useQuery({
    queryKey: ['farms'],
    queryFn: async () => {
      const r = await axios.get(`${API}/farm/farms`);
      return r.data;
    },
  });

  // Run full AI farm intelligence analysis when a farm is selected
  const {
    data: intelligence,
    isLoading,
    isError,
    refetch,
    isFetching,
  } = useQuery({
    queryKey: ['farm-intelligence', selectedFarm?.id],
    queryFn: async () => {
      const r = await axios.post(`${API}/farm/analyze?farm_id=${selectedFarm!.id}`);
      return r.data;
    },
    enabled: !!selectedFarm,
    staleTime: 5 * 60 * 1000, // 5 min cache
    retry: false,
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      {/* Page Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
            <Tractor className="h-6 w-6 text-emerald-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-text-primary">Farm Management</h2>
            <p className="text-slate-400 text-sm">AI-powered precision agriculture operating system</p>
          </div>
        </div>
        {selectedFarm && (
          <button
            onClick={() => refetch()}
            disabled={isFetching}
            className="flex items-center gap-2 text-xs font-medium px-3 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-slate-300 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${isFetching ? 'animate-spin' : ''}`} />
            Refresh Analysis
          </button>
        )}
      </div>

      {/* Farm Selector */}
      <div>
        <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Select Farm</p>
        <div className="flex gap-2 flex-wrap">
          {farms?.map((farm: any) => (
            <button
              key={farm.id}
              onClick={() => { setSelectedFarm(farm); setActiveTab('overview'); }}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-sm transition-all ${
                selectedFarm?.id === farm.id
                  ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-400 font-semibold'
                  : 'bg-slate-900/50 border-slate-800 text-slate-300 hover:border-slate-600'
              }`}
            >
              {selectedFarm?.id === farm.id
                ? <CheckCircle className="h-3.5 w-3.5" />
                : <MapPin className="h-3.5 w-3.5" />}
              <span>{farm.farm_name}</span>
              {farm.location_name && <span className="text-slate-500 text-xs">· {farm.location_name}</span>}
            </button>
          ))}
        </div>
      </div>

      {/* No farm selected state */}
      {!selectedFarm && (
        <div className="flex flex-col items-center justify-center py-20 border border-dashed border-slate-700 rounded-2xl">
          <Leaf className="h-12 w-12 text-slate-600 mb-4" />
          <h3 className="text-lg font-semibold text-slate-400">Select a Farm to Begin</h3>
          <p className="text-sm text-slate-500 mt-1">Choose a farm above to run the AI analysis</p>
        </div>
      )}

      {/* Loading state */}
      {isLoading && selectedFarm && (
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-32 rounded-2xl bg-slate-800/50 animate-pulse border border-slate-800" />
          ))}
          <p className="text-center text-sm text-slate-400">Running AI farm analysis...</p>
        </div>
      )}

      {/* Error state */}
      {isError && (
        <div className="flex flex-col items-center justify-center py-12 border border-red-500/20 rounded-2xl bg-red-500/5">
          <p className="text-red-400 font-medium">Failed to run farm analysis</p>
          <p className="text-slate-500 text-sm mt-1">Ensure the backend is running and farm data is seeded</p>
          <button onClick={() => refetch()} className="mt-4 text-xs px-3 py-1.5 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 hover:bg-red-500/20 transition-colors">
            Retry
          </button>
        </div>
      )}

      {/* Main Intelligence Dashboard */}
      {intelligence && !isLoading && (
        <div className="space-y-5">
          {/* Health Score Banner */}
          <FarmInsightsPanel
            farmName={intelligence.farm_name}
            locationName={intelligence.location_name}
            healthScore={intelligence.health_score}
            activeCrop={intelligence.active_crop}
            topRecommendation={intelligence.crop_recommendations?.[0]?.crop_name
              ? `${intelligence.crop_recommendations[0].crop_name} — ${Math.round(intelligence.crop_recommendations[0].score * 100)}% suitability`
              : undefined}
            irrigationAction={intelligence.irrigation_advice?.action}
          />

          {/* Navigation Tabs */}
          <div className="flex gap-1 bg-slate-900/60 border border-slate-800 rounded-xl p-1">
            {TABS.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 text-xs font-medium py-2 px-2 rounded-lg transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.2 }}
            >
              {activeTab === 'overview' && (
                <div className="grid gap-5 lg:grid-cols-2">
                  <CropRecommendationDashboard recommendations={intelligence.crop_recommendations?.slice(0, 5) || []} />
                  <IrrigationAdvisor advice={intelligence.irrigation_advice} />
                </div>
              )}

              {activeTab === 'crops' && (
                <CropRecommendationDashboard recommendations={intelligence.crop_recommendations || []} />
              )}

              {activeTab === 'irrigation' && (
                <IrrigationAdvisor advice={intelligence.irrigation_advice} />
              )}

              {activeTab === 'forecast' && (
                <div className="space-y-5">
                  <SeasonalForecastPanel forecast={intelligence.seasonal_forecast} />
                  <YieldProjectionPanel projections={intelligence.yield_projections || []} />
                </div>
              )}

              {activeTab === 'timeline' && (
                <FarmTimeline
                  cropName={intelligence.agricultural_timeline?.crop_name || 'Paddy'}
                  startDate={intelligence.agricultural_timeline?.start_date || ''}
                  endDate={intelligence.agricultural_timeline?.end_date || ''}
                  months={intelligence.agricultural_timeline?.months || []}
                  milestones={intelligence.agricultural_timeline?.milestones || []}
                />
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      )}
    </motion.div>
  );
};
