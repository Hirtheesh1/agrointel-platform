import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/layout/Layout';
import { Dashboard } from './pages/Dashboard';
import { Forecasting } from './pages/Forecasting';
import { EnvironmentalAnalytics } from './pages/EnvironmentalAnalytics';
import { TamilNaduRegions } from './pages/TamilNaduRegions';
import { Explainability } from './pages/Explainability';
import { Alerts } from './pages/Alerts';
import { Settings } from './pages/Settings';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="forecasting" element={<Forecasting />} />
            <Route path="analytics" element={<EnvironmentalAnalytics />} />
            <Route path="regions" element={<TamilNaduRegions />} />
            <Route path="explainability" element={<Explainability />} />
            <Route path="alerts" element={<Alerts />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
