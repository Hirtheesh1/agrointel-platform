import { useState } from 'react';
import { motion } from 'framer-motion';
import { AreaChart } from '../components/charts/AreaChart';
import { useAppStore } from '../store';

// Mock environmental data for visualization
const generateEnvData = () => {
  const data = [];
  const now = new Date();
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  for (let i = -168; i <= 0; i++) {
    const time = new Date(now.getTime() + i * 3600000);
    const hour = time.getHours();

    // Diurnal temperature curve (peaks at ~14:00, trough at ~4:00)
    const temp = 25 - Math.cos((hour - 4) * Math.PI / 12) * 8 + (Math.random() * 2 - 1);
    // Inverse humidity relationship
    const humidity = 80 - (temp - 15) * 2 + (Math.random() * 5 - 2.5);

    // Show "Mon 08:00" for every-6h ticks, giving date+time context
    const hourStr = `${hour.toString().padStart(2, '0')}:00`;
    const dateLabel = `${dayNames[time.getDay()]} ${monthNames[time.getMonth()]} ${time.getDate()}, ${hourStr}`;
    // Compact label for the axis (shown every 12h): "Mon 00:00"
    const axisLabel = `${dayNames[time.getDay()]} ${hourStr}`;

    data.push({
      time: axisLabel,        // short label shown on X-axis ticks
      tooltip: dateLabel,     // full label shown in tooltip
      timestamp: time.getTime(),
      value: 0,
      temperature: parseFloat(temp.toFixed(1)),
      humidity: parseFloat(Math.max(30, Math.min(100, humidity)).toFixed(1)),
    });
  }
  return data;
};

export const EnvironmentalAnalytics = () => {
  const { selectedFarm } = useAppStore();
  const [mockData] = useState(generateEnvData());

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-text-primary">Environmental Analytics</h2>
          <p className="text-slate-400 mt-1">168-Hour historical sequences for {selectedFarm?.location_name || 'selected region'}</p>
        </div>
      </div>

      <div className="grid gap-6">
        <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-medium text-text-primary">Temperature History (°C)</h3>
          </div>
          <AreaChart 
            data={mockData} 
            dataKey="temperature" 
            color="#f97316" 
            height={280}
            unit="°C"
          />
        </div>

        <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-medium text-text-primary">Humidity History (%)</h3>
          </div>
          <AreaChart 
            data={mockData} 
            dataKey="humidity" 
            color="#0ea5e9" 
            height={280}
            unit="%"
          />
        </div>
      </div>
    </motion.div>
  );
};
