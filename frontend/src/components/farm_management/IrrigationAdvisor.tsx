import { Droplets, CloudRain, ThermometerSun, TrendingDown, TrendingUp, Minus } from 'lucide-react';

interface ScheduleItem {
  date: string;
  day: string;
  recommendation: string;
  water_mm: number;
  rain_prob_pct: number;
}

interface IrrigationAdvice {
  action: string;
  decision_text: string;
  rain_probability_pct: number;
  temperature_c: number;
  humidity_pct: number;
  etc_mm_day: number;
  weekly_schedule: ScheduleItem[];
}

const actionStyle: Record<string, { bg: string; text: string; icon: React.ElementType; label: string }> = {
  reduce:  { bg: 'from-blue-900/40 to-blue-800/20 border-blue-700/30', text: 'text-blue-400', icon: TrendingDown, label: 'Reduce Irrigation' },
  increase:{ bg: 'from-orange-900/40 to-orange-800/20 border-orange-700/30', text: 'text-orange-400', icon: TrendingUp, label: 'Increase Irrigation' },
  normal:  { bg: 'from-slate-800/60 to-slate-700/20 border-slate-700/30', text: 'text-emerald-400', icon: Minus, label: 'Normal Schedule' },
};

const recColor: Record<string, string> = {
  'Skip':        'text-blue-400 bg-blue-500/10',
  'Reduce (25%)':'text-cyan-400 bg-cyan-500/10',
  'Increase (30%)': 'text-orange-400 bg-orange-500/10',
  'Normal':      'text-emerald-400 bg-emerald-500/10',
};

export const IrrigationAdvisor = ({ advice }: { advice: IrrigationAdvice }) => {
  const style = actionStyle[advice.action] || actionStyle.normal;
  const ActionIcon = style.icon;

  return (
    <div className="rounded-2xl border border-slate-800 bg-surface p-6 shadow-sm space-y-5">
      {/* Header */}
      <div className="flex items-center gap-2">
        <Droplets className="h-5 w-5 text-cyan-400" />
        <h3 className="text-lg font-semibold text-text-primary">Irrigation Advisor</h3>
      </div>

      {/* Main Decision Card */}
      <div className={`p-4 rounded-xl border bg-gradient-to-br ${style.bg}`}>
        <div className="flex items-center gap-2 mb-2">
          <ActionIcon className={`h-5 w-5 ${style.text}`} />
          <span className={`text-sm font-bold ${style.text}`}>{style.label}</span>
        </div>
        <p className="text-sm text-slate-300 leading-relaxed">{advice.decision_text}</p>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-3">
          <div className="flex items-center gap-1 text-slate-400 text-[10px] uppercase tracking-wide mb-1">
            <CloudRain className="h-3 w-3" /> Rain Prob.
          </div>
          <div className="text-xl font-bold text-text-primary">{advice.rain_probability_pct}%</div>
          <div className="mt-1.5 h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div className="h-full bg-blue-500 rounded-full" style={{ width: `${advice.rain_probability_pct}%` }} />
          </div>
        </div>
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-3">
          <div className="flex items-center gap-1 text-slate-400 text-[10px] uppercase tracking-wide mb-1">
            <ThermometerSun className="h-3 w-3" /> Temperature
          </div>
          <div className="text-xl font-bold text-text-primary">{advice.temperature_c}°C</div>
        </div>
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-3">
          <div className="flex items-center gap-1 text-slate-400 text-[10px] uppercase tracking-wide mb-1">
            <Droplets className="h-3 w-3" /> ETo/day
          </div>
          <div className="text-xl font-bold text-text-primary">{advice.etc_mm_day}mm</div>
        </div>
      </div>

      {/* 7-day Schedule */}
      <div>
        <p className="text-xs text-slate-500 uppercase tracking-wider mb-3">7-Day Schedule</p>
        <div className="grid grid-cols-7 gap-1.5">
          {advice.weekly_schedule.map((day, i) => (
            <div key={i} className="flex flex-col items-center gap-1">
              <span className="text-[10px] text-slate-500">{day.day.slice(0, 3)}</span>
              <div className={`w-full rounded-lg p-1.5 text-center ${recColor[day.recommendation] || 'text-slate-400 bg-slate-800/50'}`}>
                <div className="text-[10px] font-semibold leading-tight">
                  {day.recommendation === 'Normal' ? '💧' :
                   day.recommendation === 'Skip' ? '⛔' :
                   day.recommendation.startsWith('Reduce') ? '↓' : '↑'}
                </div>
                <div className="text-[10px] text-slate-400 mt-0.5">{day.water_mm}mm</div>
              </div>
              <div className="flex items-center gap-0.5">
                <CloudRain className="h-2.5 w-2.5 text-blue-400" />
                <span className="text-[9px] text-slate-500">{day.rain_prob_pct}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
