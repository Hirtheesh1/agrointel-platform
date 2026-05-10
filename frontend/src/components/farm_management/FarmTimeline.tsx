import { Calendar, Flag, AlertTriangle, CheckCircle2, Leaf } from 'lucide-react';

interface TimelineMonth {
  month_index: number;
  month_label: string;
  season: string;
  rainfall_level: string;
  risk_key: string;
  risk_label: string;
  risk_color: string;
  activities: string[];
}

interface Milestone {
  day: number;
  label: string;
  type: string;
  date: string;
}

interface Props {
  cropName: string;
  startDate: string;
  endDate: string;
  months: TimelineMonth[];
  milestones: Milestone[];
}

const riskBg: Record<string, string> = {
  green:  'bg-emerald-500/20 border-emerald-500/40 text-emerald-400',
  amber:  'bg-amber-500/20 border-amber-500/40 text-amber-400',
  orange: 'bg-orange-500/20 border-orange-500/40 text-orange-400',
  red:    'bg-red-500/20 border-red-500/40 text-red-400',
  blue:   'bg-blue-500/20 border-blue-500/40 text-blue-400',
  yellow: 'bg-yellow-500/20 border-yellow-500/40 text-yellow-400',
};

const milestoneStyle: Record<string, { color: string; icon: React.ElementType }> = {
  start:   { color: 'bg-emerald-500 text-white', icon: Leaf },
  harvest: { color: 'bg-amber-500 text-slate-900', icon: Flag },
  warning: { color: 'bg-orange-500/20 text-orange-400 border border-orange-500/30', icon: AlertTriangle },
  action:  { color: 'bg-blue-500/20 text-blue-400 border border-blue-500/30', icon: CheckCircle2 },
  info:    { color: 'bg-slate-700 text-slate-300', icon: Calendar },
};

export const FarmTimeline = ({ cropName, startDate, endDate, months, milestones }: Props) => {
  return (
    <div className="rounded-2xl border border-slate-800 bg-surface p-6 shadow-sm space-y-6">
      <div className="flex items-center gap-2">
        <Calendar className="h-5 w-5 text-primary-400" />
        <h3 className="text-lg font-semibold text-text-primary">Agricultural Timeline — {cropName}</h3>
        <span className="ml-auto text-xs text-slate-500">{startDate} → {endDate}</span>
      </div>

      {/* Month Timeline Grid */}
      <div className="overflow-x-auto">
        <div className="flex gap-2 min-w-max pb-2">
          {months.map((month) => (
            <div
              key={month.month_index}
              className={`flex flex-col rounded-xl border p-3 w-28 flex-shrink-0 ${riskBg[month.risk_color] || riskBg.green}`}
            >
              <span className="text-[10px] font-bold uppercase tracking-wide opacity-70">{month.month_label.split(' ')[0]}</span>
              <span className="text-[9px] opacity-60">{month.month_label.split(' ')[1]}</span>
              <div className="mt-2 text-[9px] font-semibold">{month.risk_label}</div>
              <div className="mt-1.5 space-y-0.5">
                {month.activities.slice(0, 2).map((act, i) => (
                  <div key={i} className="text-[9px] opacity-80 truncate">· {act}</div>
                ))}
              </div>
              <div className="mt-auto pt-1.5 text-[8px] opacity-60 uppercase">{month.season}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-3 text-[10px] text-slate-400">
        {[
          { color: 'bg-emerald-500/40', label: 'Good conditions' },
          { color: 'bg-amber-500/40', label: 'Heat/Dry stress' },
          { color: 'bg-blue-500/40', label: 'Flood risk' },
          { color: 'bg-red-500/40', label: 'Drought risk' },
        ].map(({ color, label }) => (
          <div key={label} className="flex items-center gap-1.5">
            <div className={`w-3 h-3 rounded-sm ${color}`} />
            <span>{label}</span>
          </div>
        ))}
      </div>

      {/* Milestones */}
      <div>
        <p className="text-xs text-slate-500 uppercase tracking-wider mb-3">Key Milestones</p>
        <div className="space-y-2">
          {milestones.map((m, i) => {
            const style = milestoneStyle[m.type] || milestoneStyle.info;
            const Icon = style.icon;
            return (
              <div key={i} className="flex items-center gap-3">
                <span className="text-xs text-slate-500 w-24 text-right flex-shrink-0">{m.date}</span>
                <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 ${style.color}`}>
                  <Icon className="h-3.5 w-3.5" />
                </div>
                <span className="text-sm text-slate-300">{m.label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
