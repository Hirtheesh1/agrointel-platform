import { useState } from 'react';
import { Sprout, ChevronDown, ChevronUp, Droplets, Clock, Award } from 'lucide-react';

interface CropRec {
  crop_key: string;
  crop_name: string;
  season: string;
  score: number;
  confidence: string;
  status: string;
  total_days: number;
  water_need_mm_day: number;
  yield_range_tons: { low: number; high: number };
  reasoning: string;
}

interface Props {
  recommendations: CropRec[];
}

const statusStyle: Record<string, string> = {
  'Recommended':     'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  'Monitor':         'bg-amber-500/20 text-amber-400 border-amber-500/30',
  'Not Recommended': 'bg-red-500/20 text-red-400 border-red-500/30',
};

const confidenceBar: Record<string, string> = {
  High: 'bg-emerald-500', Medium: 'bg-amber-500', Low: 'bg-red-500',
};

const seasonBadge: Record<string, string> = {
  kharif:   'bg-green-500/20 text-green-400',
  rabi:     'bg-blue-500/20 text-blue-400',
  zaid:     'bg-yellow-500/20 text-yellow-400',
  perennial:'bg-purple-500/20 text-purple-400',
};

export const CropRecommendationDashboard = ({ recommendations }: Props) => {
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div className="rounded-2xl border border-slate-800 bg-surface p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-5">
        <Sprout className="h-5 w-5 text-emerald-400" />
        <h3 className="text-lg font-semibold text-text-primary">AI Crop Recommendations</h3>
        <span className="ml-auto text-xs text-slate-400">{recommendations.length} crops analyzed</span>
      </div>

      <div className="space-y-3">
        {recommendations.map((crop, idx) => (
          <div
            key={crop.crop_key}
            className={`rounded-xl border transition-all duration-200 ${
              expanded === crop.crop_key
                ? 'border-slate-600 bg-slate-800/60'
                : 'border-slate-800 bg-slate-900/40 hover:border-slate-700'
            }`}
          >
            <button
              className="w-full text-left p-4"
              onClick={() => setExpanded(expanded === crop.crop_key ? null : crop.crop_key)}
            >
              <div className="flex items-center gap-3">
                {/* Rank */}
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${
                  idx === 0 ? 'bg-amber-500 text-slate-900' :
                  idx === 1 ? 'bg-slate-400 text-slate-900' :
                  idx === 2 ? 'bg-orange-700 text-white' : 'bg-slate-800 text-slate-400'
                }`}>{idx + 1}</span>

                {/* Name & badges */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm font-semibold text-text-primary">{crop.crop_name}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full capitalize ${seasonBadge[crop.season] || 'bg-slate-700 text-slate-400'}`}>
                      {crop.season}
                    </span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full border ${statusStyle[crop.status]}`}>
                      {crop.status}
                    </span>
                  </div>
                </div>

                {/* Score bar */}
                <div className="flex items-center gap-2 flex-shrink-0">
                  <div className="w-20 h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${confidenceBar[crop.confidence]} transition-all duration-500`}
                      style={{ width: `${crop.score * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-bold text-text-primary w-10 text-right">
                    {Math.round(crop.score * 100)}%
                  </span>
                  {expanded === crop.crop_key
                    ? <ChevronUp className="h-4 w-4 text-slate-400" />
                    : <ChevronDown className="h-4 w-4 text-slate-400" />}
                </div>
              </div>
            </button>

            {/* Expanded details */}
            {expanded === crop.crop_key && (
              <div className="px-4 pb-4 border-t border-slate-700/50 pt-3 space-y-3">
                <p className="text-sm text-slate-300 leading-relaxed">{crop.reasoning}</p>
                <div className="grid grid-cols-3 gap-3">
                  <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 uppercase tracking-wide flex items-center gap-1">
                      <Clock className="h-3 w-3" /> Duration
                    </p>
                    <p className="text-base font-bold text-text-primary mt-1">{crop.total_days} days</p>
                  </div>
                  <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 uppercase tracking-wide flex items-center gap-1">
                      <Droplets className="h-3 w-3" /> Water Need
                    </p>
                    <p className="text-base font-bold text-text-primary mt-1">{crop.water_need_mm_day} mm/d</p>
                  </div>
                  <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 uppercase tracking-wide flex items-center gap-1">
                      <Award className="h-3 w-3" /> Yield Range
                    </p>
                    <p className="text-base font-bold text-text-primary mt-1">
                      {crop.yield_range_tons.low}–{crop.yield_range_tons.high}t
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
