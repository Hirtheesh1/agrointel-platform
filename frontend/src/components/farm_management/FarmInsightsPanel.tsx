import { Activity, TrendingUp, Droplets, AlertTriangle, CheckCircle2, Clock } from 'lucide-react';

interface FarmInsightsPanelProps {
  farmName: string;
  locationName?: string;
  healthScore: { score: number; status: string; color: string };
  activeCrop?: string;
  topRecommendation?: string;
  irrigationAction?: string;
}

const healthColorMap: Record<string, string> = {
  green: 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10',
  amber: 'text-amber-400 border-amber-500/30 bg-amber-500/10',
  orange: 'text-orange-400 border-orange-500/30 bg-orange-500/10',
  red: 'text-red-400 border-red-500/30 bg-red-500/10',
};

const scoreRingColor: Record<string, string> = {
  green: '#10b981', amber: '#f59e0b', orange: '#f97316', red: '#ef4444',
};

export const FarmInsightsPanel = ({
  farmName,
  locationName,
  healthScore,
  activeCrop,
  topRecommendation,
  irrigationAction,
}: FarmInsightsPanelProps) => {
  const colorClass = healthColorMap[healthScore.color] || healthColorMap.amber;
  const ringColor = scoreRingColor[healthScore.color] || '#f59e0b';
  const circumference = 2 * Math.PI * 36;
  const dashOffset = circumference - (healthScore.score / 100) * circumference;

  return (
    <div className="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-800/50 p-6 shadow-xl">
      <div className="flex flex-col md:flex-row gap-6 items-start md:items-center">
        
        {/* Score Ring */}
        <div className="relative flex-shrink-0 flex flex-col items-center">
          <svg width="96" height="96" viewBox="0 0 96 96">
            <circle cx="48" cy="48" r="36" fill="none" stroke="#1e293b" strokeWidth="8" />
            <circle
              cx="48" cy="48" r="36" fill="none"
              stroke={ringColor} strokeWidth="8"
              strokeDasharray={circumference}
              strokeDashoffset={dashOffset}
              strokeLinecap="round"
              transform="rotate(-90 48 48)"
              style={{ transition: 'stroke-dashoffset 1s ease' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-bold text-text-primary">{healthScore.score}</span>
            <span className="text-[10px] text-slate-400">/ 100</span>
          </div>
          <span className={`mt-2 text-xs font-semibold px-2 py-0.5 rounded-full border ${colorClass}`}>
            {healthScore.status}
          </span>
        </div>

        {/* Farm Info */}
        <div className="flex-1 space-y-1">
          <h3 className="text-xl font-bold text-text-primary">{farmName}</h3>
          {locationName && <p className="text-sm text-slate-400">{locationName}</p>}
          {activeCrop && (
            <div className="flex items-center gap-1.5 mt-2">
              <Activity className="h-4 w-4 text-emerald-400" />
              <span className="text-sm text-slate-300">Active Crop: <strong className="text-text-primary">{activeCrop}</strong></span>
            </div>
          )}
        </div>

        {/* Quick Decision Cards */}
        <div className="flex flex-col gap-2 w-full md:w-auto min-w-[220px]">
          {topRecommendation && (
            <div className="flex items-start gap-2 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
              <TrendingUp className="h-4 w-4 text-emerald-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-[10px] text-emerald-400 uppercase tracking-wide font-medium">Top Crop Recommendation</p>
                <p className="text-xs text-slate-200 mt-0.5">{topRecommendation}</p>
              </div>
            </div>
          )}
          {irrigationAction && (
            <div className={`flex items-start gap-2 p-3 rounded-xl border ${
              irrigationAction === 'reduce' ? 'bg-blue-500/10 border-blue-500/20' :
              irrigationAction === 'increase' ? 'bg-orange-500/10 border-orange-500/20' :
              'bg-slate-800/50 border-slate-700'
            }`}>
              <Droplets className={`h-4 w-4 mt-0.5 flex-shrink-0 ${
                irrigationAction === 'reduce' ? 'text-blue-400' :
                irrigationAction === 'increase' ? 'text-orange-400' : 'text-slate-400'
              }`} />
              <div>
                <p className="text-[10px] uppercase tracking-wide font-medium text-slate-400">Irrigation Today</p>
                <p className="text-xs text-slate-200 mt-0.5 capitalize font-semibold">{irrigationAction} irrigation</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
