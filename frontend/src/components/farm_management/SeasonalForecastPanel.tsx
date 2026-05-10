import { Sun, CloudRain, AlertTriangle, Droplets } from 'lucide-react';

interface SeasonalHorizon {
  label: string;
  suitability_score: number;
  rainfall_index: number;
  drought_risk: string;
  drought_color: string;
  irrigation_status: string;
  irrigation_color: string;
  outlook: string;
}

interface SeasonalForecast {
  '7_day': SeasonalHorizon;
  '30_day': SeasonalHorizon;
  '3_month': SeasonalHorizon;
  '10_month': SeasonalHorizon;
}

const droughtColor: Record<string, string> = {
  Low: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  Medium: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  High: 'text-red-400 bg-red-500/10 border-red-500/20',
};
const irrigationColor: Record<string, string> = {
  blue: 'text-blue-400',
  amber: 'text-amber-400',
  red: 'text-red-400',
};
const scoreGradient = (score: number) => {
  if (score >= 70) return '#10b981';
  if (score >= 50) return '#f59e0b';
  return '#ef4444';
};

const HorizonCard = ({ horizon }: { horizon: SeasonalHorizon }) => {
  const circumference = 2 * Math.PI * 24;
  const dashOffset = circumference - (horizon.suitability_score / 100) * circumference;
  const color = scoreGradient(horizon.suitability_score);

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4 flex flex-col gap-3">
      {/* Label + Score */}
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-text-primary">{horizon.label}</span>
        <div className="relative w-12 h-12">
          <svg width="48" height="48" viewBox="0 0 48 48">
            <circle cx="24" cy="24" r="20" fill="none" stroke="#1e293b" strokeWidth="5" />
            <circle
              cx="24" cy="24" r="20" fill="none"
              stroke={color} strokeWidth="5"
              strokeDasharray={circumference}
              strokeDashoffset={dashOffset}
              strokeLinecap="round"
              transform="rotate(-90 24 24)"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-xs font-bold" style={{ color }}>{horizon.suitability_score}</span>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-400 flex items-center gap-1"><CloudRain className="h-3 w-3" /> Rainfall Index</span>
          <div className="flex items-center gap-1.5">
            <div className="w-16 h-1.5 bg-slate-700 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500 rounded-full" style={{ width: `${horizon.rainfall_index}%` }} />
            </div>
            <span className="text-slate-300 font-medium">{horizon.rainfall_index}</span>
          </div>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-400 flex items-center gap-1"><AlertTriangle className="h-3 w-3" /> Drought Risk</span>
          <span className={`text-[10px] px-2 py-0.5 rounded-full border ${droughtColor[horizon.drought_risk]}`}>
            {horizon.drought_risk}
          </span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-400 flex items-center gap-1"><Droplets className="h-3 w-3" /> Irrigation</span>
          <span className={`text-xs font-medium ${irrigationColor[horizon.irrigation_color]}`}>
            {horizon.irrigation_status}
          </span>
        </div>
      </div>

      {/* Outlook text */}
      <p className="text-[11px] text-slate-400 leading-relaxed border-t border-slate-800 pt-2">
        {horizon.outlook}
      </p>
    </div>
  );
};

export const SeasonalForecastPanel = ({ forecast }: { forecast: SeasonalForecast }) => {
  const horizons = [
    forecast['7_day'], forecast['30_day'], forecast['3_month'], forecast['10_month']
  ];

  return (
    <div className="rounded-2xl border border-slate-800 bg-surface p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-5">
        <Sun className="h-5 w-5 text-amber-400" />
        <h3 className="text-lg font-semibold text-text-primary">Seasonal Climate Forecast</h3>
        <span className="ml-auto text-xs text-slate-500">Tamil Nadu Monsoon Intelligence</span>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {horizons.map((h, i) => <HorizonCard key={i} horizon={h} />)}
      </div>
    </div>
  );
};
