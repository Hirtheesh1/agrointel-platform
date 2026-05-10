import React from 'react';
import { motion } from 'framer-motion';
import { Database, Server } from 'lucide-react';

export const Settings = () => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-text-primary">Platform Settings</h2>
          <p className="text-slate-400 mt-1">Configure your AI pipeline and integrations</p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <div className="flex items-center mb-4">
            <Server className="h-5 w-5 text-primary-500 mr-2" />
            <h3 className="text-lg font-medium text-text-primary">Inference API</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Backend URL</label>
              <input 
                type="text" 
                defaultValue="http://localhost:8000/api/v1"
                className="w-full rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-300 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Active Model</label>
              <select className="w-full rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-300 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500">
                <option>TFT v1.0 (Production)</option>
                <option>TFT v0.9 (Legacy)</option>
              </select>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <div className="flex items-center mb-4">
            <Database className="h-5 w-5 text-blue-500 mr-2" />
            <h3 className="text-lg font-medium text-text-primary">Data Pipeline</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Weather Sync Interval</label>
              <select className="w-full rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-300 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500">
                <option>Hourly</option>
                <option>Every 6 Hours</option>
                <option>Daily</option>
              </select>
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-sm text-slate-300">Auto-retrain model</span>
              <button className="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-primary-600 transition-colors duration-200 ease-in-out focus:outline-none">
                <span className="translate-x-5 pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out" />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div className="flex justify-end pt-4">
        <button className="bg-primary-600 hover:bg-primary-500 text-white px-4 py-2 rounded-md font-medium text-sm transition-colors">
          Save Configuration
        </button>
      </div>
    </motion.div>
  );
};
