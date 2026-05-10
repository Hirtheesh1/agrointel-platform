import { BarChart3, TrendingUp } from 'lucide-react';

interface YieldItem {
  crop_name: string;
  crop_key: string;
  score: number;
  yield_low_tons: number;
  yield_expected_tons: number;
  yield_high_tons: number;
  farm_size_ha: number;
  risk_adjusted: boolean;
}

const barColors = [
  { low: '#1e3a5f', expected: '#3b82f6', high: '#93c5fd' },
  { low: '#1a3a2a', expected: '#10b981', high: '#6ee7b7' },
  { low: '#3b2800', expected: '#f59e0b', high: '#fde68a' },
  { low: '#3b1a1a', expected: '#f97316', high: '#fed7aa' },
  { low: '#2e1a3b', expected: '#a855f7', high: '#d8b4fe' },
  { low: '#1a3b3b', expected: '#06b6d4', high: '#a5f3fc' },
];

export const YieldProjectionPanel = ({ projections }: { projections: YieldItem[] }) => {
  const maxYield = Math.max(...projections.map(p => p.yield_high_tons), 1);

  return (
    <div className="rounded-2xl border border-slate-800 bg-surface p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-5">
        <BarChart3 className="h-5 w-5 text-primary-400" />
        <h3 className="text-lg font-semibold text-text-primary">Yield Projections</h3>
        <span className="ml-auto text-xs text-slate-400 flex items-center gap-1">
          <TrendingUp className="h-3 w-3" /> Risk-adjusted forecasts
        </span>
      </div>

      <div className="space-y-4">
        {projections.map((item, idx) => {
          const colors = barColors[idx % barColors.length];
          const lowPct = (item.yield_low_tons / maxYield) * 100;
          const expPct = (item.yield_expected_tons / maxYield) * 100;
          const highPct = (item.yield_high_tons / maxYield) * 100;

          return (
            <div key={item.crop_key}>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-sm font-medium text-text-primary">{item.crop_name}</span>
                <span className="text-xs text-slate-400">
                  {item.yield_expected_tons}t expected · <span className="text-slate-500">up to {item.yield_high_tons}t</span>
                </span>
              </div>
              <div className="relative h-6 bg-slate-900 rounded-lg overflow-hidden">
                {/* Low bar */}
                <div
                  className="absolute inset-y-0 left-0 rounded-lg transition-all duration-700"
                  style={{ width: `${highPct}%`, backgroundColor: colors.low }}
                />
                {/* Expected bar */}
                <div
                  className="absolute inset-y-0 left-0 rounded-lg transition-all duration-700"
                  style={{ width: `${expPct}%`, backgroundColor: colors.expected }}
                />
                {/* Low threshold marker */}
                <div
                  className="absolute inset-y-0 w-0.5 bg-white/20"
                  style={{ left: `${lowPct}%` }}
                />
                {/* Labels inside bar */}
                <div className="absolute inset-0 flex items-center px-2 gap-4">
                  <span className="text-[10px] text-white/60">Low: {item.yield_low_tons}t</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="flex gap-4 mt-4 text-[10px] text-slate-400 border-t border-slate-800 pt-3">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-slate-600" /> Low scenario
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-primary-500" /> Expected yield
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-primary-300/50" /> High scenario
        </div>
        <span className="ml-auto">Per {projections[0]?.farm_size_ha || 1} ha farm</span>
      </div>
    </div>
  );
};
