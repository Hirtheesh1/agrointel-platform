import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AreaChart } from '../components/charts/AreaChart';
import { useQuery } from '@tanstack/react-query';
import { useAppStore } from '../store';
import { runForecast, fetchLatestForecast } from '../api';
import { Play, Loader2, Info } from 'lucide-react';

// Mock temporal data for visualization demo
const generateMockData = () => {
  const data = [];
  const now = new Date();
  for (let i = -48; i <= 24; i++) {
    const time = new Date(now.getTime() + i * 3600000);
    // Add some random noise to a sine wave for realism
    const baseValue = Math.sin(i / 12) * 5 + 10;
    const value = i <= 0 ? baseValue + Math.random() * 2 : baseValue + Math.random() * 3;
    data.push({
      time: time.getHours() + ':00',
      value: Math.max(0, value),
      irrigation_demand: Math.max(0, value).toFixed(1),
      isForecast: i > 0
    });
  }
  return data;
};

export const Forecasting = () => {
  const { selectedFarm } = useAppStore();
  const [isGenerating, setIsGenerating] = useState(false);
  const [mockData] = useState(generateMockData());

  const { data: forecast, refetch } = useQuery({
    queryKey: ['latestForecast', selectedFarm?.id],
    queryFn: () => selectedFarm ? fetchLatestForecast(selectedFarm.id) : Promise.reject('No farm'),
    enabled: !!selectedFarm,
  });

  const handleRunForecast = async () => {
    if (!selectedFarm) return;
    setIsGenerating(true);
    try {
      await runForecast(selectedFarm.id);
      await refetch();
    } catch (error) {
      console.error('Failed to run forecast', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-text-primary">Temporal Forecasting</h2>
          <p className="text-slate-400 mt-1">
            {selectedFarm ? `Analyzing sequences for ${selectedFarm.location_name}` : 'Select a region to view forecasts'}
          </p>
        </div>
        <button
          onClick={handleRunForecast}
          disabled={isGenerating || !selectedFarm}
          className="inline-flex items-center justify-center rounded-md bg-primary-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isGenerating ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <Play className="mr-2 h-4 w-4" />
          )}
          Generate Live Forecast
        </button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-medium text-text-primary">Irrigation Demand Timeline (mm)</h3>
            <span className="inline-flex items-center rounded-full bg-blue-500/10 px-2 py-1 text-xs font-medium text-blue-400 border border-blue-500/20">
              TFT Transformer Active
            </span>
          </div>
          <AreaChart 
            data={mockData} 
            dataKey="irrigation_demand" 
            color="#3b82f6" 
            predictionStartIndex={48}
          />
        </div>

        <div className="space-y-6">
          <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
            <h3 className="text-lg font-medium text-text-primary mb-4">Latest Prediction</h3>
            {forecast?.irrigation ? (
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-slate-400">Predicted Demand</p>
                  <p className="text-3xl font-bold text-primary-500">{forecast.irrigation.prediction_value.toFixed(2)} mm</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Confidence Score</p>
                  <div className="flex items-center mt-1">
                    <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-primary-500 rounded-full" 
                        style={{ width: `${forecast.irrigation.confidence_score * 100}%` }}
                      />
                    </div>
                    <span className="ml-3 text-sm font-medium text-slate-300">
                      {(forecast.irrigation.confidence_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                <div className="pt-4 border-t border-slate-800">
                  <p className="text-xs text-slate-500 flex items-center">
                    <Info className="h-3 w-3 mr-1" />
                    Model: {forecast.irrigation.model_version}
                  </p>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-8 text-center">
                <p className="text-slate-400 mb-2">No recent forecast available.</p>
                <p className="text-sm text-slate-500">Click Generate Live Forecast to run the AI pipeline.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
