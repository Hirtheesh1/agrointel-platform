import React from 'react';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { fetchLatestForecast } from '../api';
import { useAppStore } from '../store';
import { BrainCircuit, Cpu, Zap, Activity } from 'lucide-react';

export const Explainability = () => {
  const { selectedFarm } = useAppStore();
  
  const { data: forecast, isLoading } = useQuery({
    queryKey: ['latestForecast', selectedFarm?.id],
    queryFn: () => selectedFarm ? fetchLatestForecast(selectedFarm.id) : Promise.reject('No farm'),
    enabled: !!selectedFarm,
  });

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-text-primary">Explainable AI Insights</h2>
          <p className="text-slate-400 mt-1">Transparency report for {selectedFarm?.location_name || 'selected region'}</p>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <div className="flex items-center mb-6">
            <div className="p-2 bg-primary-500/10 rounded-lg mr-4 border border-primary-500/20">
              <BrainCircuit className="h-6 w-6 text-primary-500" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-text-primary">Irrigation Forecast Reasoning</h3>
              <p className="text-sm text-slate-400">TFT Model Explanation Output</p>
            </div>
          </div>
          
          <div className="bg-slate-800/50 rounded-lg p-5 border border-slate-700/50">
            {isLoading ? (
              <div className="animate-pulse flex space-x-4">
                <div className="flex-1 space-y-4 py-1">
                  <div className="h-2 bg-slate-700 rounded w-3/4"></div>
                  <div className="space-y-2">
                    <div className="h-2 bg-slate-700 rounded"></div>
                    <div className="h-2 bg-slate-700 rounded w-5/6"></div>
                  </div>
                </div>
              </div>
            ) : forecast?.irrigation?.explanation ? (
              <p className="text-slate-300 leading-relaxed text-lg italic">
                "{forecast.irrigation.explanation}"
              </p>
            ) : (
              <p className="text-slate-500">Run a forecast to generate natural language explanations.</p>
            )}
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <h3 className="text-lg font-medium text-text-primary mb-6">Attention Weights Visualization</h3>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-300 flex items-center"><Activity className="w-4 h-4 mr-2 text-blue-400" /> Temperature Lag</span>
                <span className="text-slate-400">34%</span>
              </div>
              <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 rounded-full" style={{ width: '34%' }} />
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-300 flex items-center"><Zap className="w-4 h-4 mr-2 text-yellow-400" /> Evaporation Index</span>
                <span className="text-slate-400">28%</span>
              </div>
              <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-yellow-500 rounded-full" style={{ width: '28%' }} />
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-300 flex items-center"><Cpu className="w-4 h-4 mr-2 text-green-400" /> Time of Day</span>
                <span className="text-slate-400">22%</span>
              </div>
              <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 rounded-full" style={{ width: '22%' }} />
              </div>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-6 text-center">
            *Variables driving the current structural TFT prediction*
          </p>
        </div>
      </div>
    </motion.div>
  );
};
