import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { Map, Target, PenLine, Satellite } from 'lucide-react';
import { FarmMap } from './FarmMap';
import { RegionSelector } from './RegionSelector';
import { FarmBoundaryDrawer } from './FarmBoundaryDrawer';
import { MicroclimateInsights } from './MicroclimateInsights';
import { useAppStore } from '../../store';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

type Tab = 'overview' | 'region' | 'boundary';

export const GeoAnalyticsPanel = () => {
  const { selectedFarm } = useAppStore();
  const [activeTab, setActiveTab] = useState<Tab>('overview');
  const [radiusKm, setRadiusKm] = useState(5);
  const [adHocResult, setAdHocResult] = useState<any>(null);

  // Fetch microclimate for currently selected farm
  const { data: microclimate, isLoading: loadingMicro } = useQuery({
    queryKey: ['microclimate', selectedFarm?.id],
    queryFn: async () => {
      const r = await axios.get(`${API_URL}/geospatial/microclimate/${selectedFarm!.id}`);
      return r.data;
    },
    enabled: !!selectedFarm,
    retry: false,
  });

  // Ad-hoc region analysis mutation
  const analyzeRegion = useMutation({
    mutationFn: async ({ lat, lon, radius }: { lat: number; lon: number; radius: number }) => {
      const r = await axios.post(`${API_URL}/geospatial/analyze-region`, {
        latitude: lat,
        longitude: lon,
        radius_km: radius,
      });
      return r.data;
    },
    onSuccess: (data) => setAdHocResult(data),
  });

  const tabs: { id: Tab; label: string; icon: React.ElementType }[] = [
    { id: 'overview', label: 'Farm Overview', icon: Map },
    { id: 'region', label: 'Region Analysis', icon: Target },
    { id: 'boundary', label: 'Draw Boundary', icon: PenLine },
  ];

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3 rounded-xl bg-gradient-to-r from-emerald-900/40 to-blue-900/40 border border-emerald-800/30 p-4">
        <Satellite className="h-6 w-6 text-emerald-400" />
        <div>
          <h2 className="text-base font-semibold text-text-primary">Geospatial Farm Intelligence</h2>
          <p className="text-xs text-slate-400">Precision microclimate analysis · Tamil Nadu agricultural zones</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-slate-900/60 border border-slate-800 rounded-xl p-1">
        {tabs.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            className={`flex-1 flex items-center justify-center gap-2 text-xs font-medium py-2 px-3 rounded-lg transition-all duration-200 ${
              activeTab === id
                ? 'bg-primary-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Icon className="h-3.5 w-3.5" />
            {label}
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
          {/* OVERVIEW TAB */}
          {activeTab === 'overview' && (
            <div className="grid gap-4 lg:grid-cols-3">
              <div className="lg:col-span-2 space-y-3">
                <div className="flex items-center justify-between bg-surface border border-slate-800 p-3 rounded-xl">
                  <p className="text-sm font-medium text-text-primary">
                    {selectedFarm ? `${selectedFarm.farm_name} — ${selectedFarm.location_name}` : 'No Farm Selected'}
                  </p>
                  <div className="flex items-center gap-2">
                    <label className="text-xs text-slate-400">Radius:</label>
                    <select
                      className="bg-slate-800 border border-slate-700 text-xs rounded px-2 py-1 text-slate-200"
                      value={radiusKm}
                      onChange={(e) => setRadiusKm(Number(e.target.value))}
                    >
                      {[2, 5, 10, 20].map(r => <option key={r} value={r}>{r} km</option>)}
                    </select>
                  </div>
                </div>
                <FarmMap radiusKm={radiusKm} />
              </div>

              <div className="lg:col-span-1">
                {!selectedFarm ? (
                  <div className="h-full flex items-center justify-center border border-slate-800 rounded-xl bg-surface/50 p-6 text-center">
                    <p className="text-slate-400 text-sm">Select a farm from the dashboard to view microclimate analysis.</p>
                  </div>
                ) : loadingMicro ? (
                  <div className="h-full flex items-center justify-center border border-slate-800 rounded-xl bg-surface/50 animate-pulse p-6">
                    <p className="text-slate-400 text-sm">Computing spatial aggregations...</p>
                  </div>
                ) : microclimate ? (
                  <MicroclimateInsights
                    insights={microclimate.insights.text_explanation}
                    anomalies={microclimate.insights.anomalies}
                    tempDelta={microclimate.insights.temp_delta}
                    humidityDelta={microclimate.insights.humidity_delta}
                  />
                ) : (
                  <div className="h-full flex items-center justify-center border border-slate-800 rounded-xl bg-surface/50 p-6">
                    <p className="text-slate-400 text-sm">Could not fetch microclimate data.</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* REGION ANALYSIS TAB */}
          {activeTab === 'region' && (
            <div className="grid gap-4 lg:grid-cols-3">
              <div className="lg:col-span-2">
                <RegionSelector
                  onRegionSelected={(lat, lon, radius) =>
                    analyzeRegion.mutate({ lat, lon, radius })
                  }
                />
              </div>
              <div className="lg:col-span-1">
                {analyzeRegion.isPending ? (
                  <div className="h-full flex items-center justify-center border border-slate-800 rounded-xl bg-surface/50 animate-pulse p-6">
                    <p className="text-slate-400 text-sm">Fetching environmental data...</p>
                  </div>
                ) : adHocResult ? (
                  <div className="rounded-xl border border-slate-800 bg-surface p-5 space-y-4">
                    <h4 className="text-sm font-semibold text-text-primary">Zone Environment</h4>
                    <div className="grid grid-cols-2 gap-3">
                      {Object.entries(adHocResult.environment).map(([key, val]) => (
                        <div key={key} className="bg-slate-900/50 border border-slate-800 p-3 rounded-lg">
                          <p className="text-[10px] uppercase tracking-wide text-slate-500">{key.replace(/_/g, ' ')}</p>
                          <p className="text-lg font-bold text-text-primary mt-1">{typeof val === 'number' ? (val as number).toFixed(1) : val as string}</p>
                        </div>
                      ))}
                    </div>
                    <div className="text-xs text-slate-500">
                      📍 {adHocResult.latitude?.toFixed(4)}°N, {adHocResult.longitude?.toFixed(4)}°E · {adHocResult.radius_km} km radius
                    </div>
                  </div>
                ) : (
                  <div className="h-full flex flex-col items-center justify-center border border-dashed border-slate-700 rounded-xl p-6 text-center gap-2">
                    <Target className="h-8 w-8 text-slate-600" />
                    <p className="text-slate-400 text-sm">Click on the map to select a location, then click <strong>Analyze Zone</strong>.</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* BOUNDARY DRAWER TAB */}
          {activeTab === 'boundary' && (
            <div className="grid gap-4 lg:grid-cols-3">
              <div className="lg:col-span-2">
                <FarmBoundaryDrawer
                  onBoundaryComplete={(geojson) => {
                    console.log('Farm Boundary GeoJSON:', JSON.stringify(geojson, null, 2));
                    // Could save to backend here
                  }}
                />
              </div>
              <div className="lg:col-span-1 rounded-xl border border-slate-800 bg-surface p-5 space-y-3">
                <h4 className="text-sm font-semibold text-text-primary flex items-center gap-2">
                  <PenLine className="h-4 w-4 text-amber-400" /> Boundary Instructions
                </h4>
                <ol className="space-y-2 text-sm text-slate-400 list-decimal list-inside">
                  <li>Click <strong className="text-slate-200">Start Drawing</strong></li>
                  <li>Click on the map to place boundary vertices</li>
                  <li>Place at least <strong className="text-slate-200">3 points</strong></li>
                  <li>Click <strong className="text-slate-200">Finish</strong> to complete</li>
                </ol>
                <div className="mt-4 p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg">
                  <p className="text-xs text-amber-400">
                    The boundary GeoJSON will be stored with the farm record and used for localized microclimate analysis.
                  </p>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
};
