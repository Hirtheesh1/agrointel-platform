import { AlertTriangle, MapPin, Droplets, ThermometerSun } from 'lucide-react';

interface MicroclimateInsightsProps {
  insights: string;
  anomalies: string[];
  tempDelta: number;
  humidityDelta: number;
}

export const MicroclimateInsights = ({ insights, anomalies, tempDelta, humidityDelta }: MicroclimateInsightsProps) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-surface p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <MapPin className="text-primary-400 h-5 w-5" />
        <h3 className="text-lg font-medium text-text-primary">Microclimate Intelligence</h3>
      </div>
      
      <div className="space-y-4">
        <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
          <p className="text-sm text-slate-300">
            {insights || "Analyzing local environmental conditions..."}
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col p-3 rounded-lg border border-slate-800 bg-slate-900/50">
            <span className="text-xs text-slate-400 mb-1 flex items-center gap-1">
              <ThermometerSun className="h-3 w-3" /> Temp Delta vs Region
            </span>
            <span className={`text-lg font-bold ${tempDelta > 0 ? 'text-red-400' : tempDelta < 0 ? 'text-blue-400' : 'text-slate-300'}`}>
              {tempDelta > 0 ? '+' : ''}{tempDelta}°C
            </span>
          </div>
          
          <div className="flex flex-col p-3 rounded-lg border border-slate-800 bg-slate-900/50">
            <span className="text-xs text-slate-400 mb-1 flex items-center gap-1">
              <Droplets className="h-3 w-3" /> Humidity Delta
            </span>
            <span className={`text-lg font-bold ${humidityDelta > 0 ? 'text-blue-400' : humidityDelta < 0 ? 'text-yellow-400' : 'text-slate-300'}`}>
              {humidityDelta > 0 ? '+' : ''}{humidityDelta}%
            </span>
          </div>
        </div>

        {anomalies.length > 0 && (
          <div className="mt-4 flex items-start gap-2 p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
            <AlertTriangle className="h-4 w-4 text-yellow-500 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-xs font-medium text-yellow-500 mb-1">Spatial Anomalies Detected</p>
              <div className="flex flex-wrap gap-2">
                {anomalies.map((a, i) => (
                  <span key={i} className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded">
                    {a.replace('_', ' ')}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
