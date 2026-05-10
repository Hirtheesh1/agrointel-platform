import React from 'react';
import {
  AreaChart as RechartsAreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

interface DataPoint {
  time: string;
  timestamp?: number; // epoch ms for smart formatting
  value: number;
  [key: string]: any;
}

interface AreaChartProps {
  data: DataPoint[];
  dataKey: string;
  xAxisKey?: string;
  color?: string;
  height?: number;
  predictionStartIndex?: number;
  yAxisFormatter?: (val: number) => string;
  unit?: string;
}

// Custom tooltip that shows date + time properly
const CustomTooltip = ({ active, payload, unit }: any) => {
  if (active && payload && payload.length) {
    // Prefer the 'tooltip' field (full date string) over the axis 'time' label
    const fullLabel = payload[0]?.payload?.tooltip || payload[0]?.payload?.time || '';
    return (
      <div
        style={{
          backgroundColor: '#0f172a',
          border: '1px solid #334155',
          borderRadius: 10,
          padding: '10px 14px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
        }}
      >
        <p style={{ color: '#94a3b8', fontSize: 11, marginBottom: 4, fontWeight: 500 }}>{fullLabel}</p>
        {payload.map((entry: any, i: number) => (
          <p key={i} style={{ color: entry.color, fontSize: 14, fontWeight: 700, margin: 0 }}>
            {entry.name}: {typeof entry.value === 'number' ? Number(entry.value).toFixed(1) : entry.value}
            {unit ? ` ${unit}` : ''}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export const AreaChart: React.FC<AreaChartProps> = ({
  data,
  dataKey,
  xAxisKey = 'time',
  color = '#22c55e',
  height = 300,
  predictionStartIndex,
  yAxisFormatter = (val) => `${val}`,
  unit = '',
}) => {
  // Show only every Nth tick to avoid crowding
  // For 169-point (7-day hourly) data: show one tick every 12 hours
  const tickInterval = data.length > 100 ? 11 : data.length > 48 ? 5 : 1;

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer>
        <RechartsAreaChart
          data={data}
          margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id={`color${dataKey}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.35} />
              <stop offset="95%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />

          <XAxis
            dataKey={xAxisKey}
            stroke="#475569"
            tick={{ fill: '#64748b', fontSize: 11 }}
            tickLine={false}
            axisLine={{ stroke: '#1e293b' }}
            interval={tickInterval}
            // Angle the labels slightly to avoid overlap when there are many
            angle={data.length > 72 ? -35 : 0}
            textAnchor={data.length > 72 ? 'end' : 'middle'}
            height={data.length > 72 ? 45 : 30}
          />

          <YAxis
            stroke="#475569"
            tick={{ fill: '#64748b', fontSize: 11 }}
            tickLine={false}
            axisLine={false}
            tickFormatter={yAxisFormatter}
            width={40}
          />

          <Tooltip
            content={<CustomTooltip unit={unit} />}
            cursor={{ stroke: color, strokeWidth: 1, strokeDasharray: '4 4' }}
          />

          {predictionStartIndex !== undefined && data[predictionStartIndex] && (
            <ReferenceLine
              x={data[predictionStartIndex][xAxisKey]}
              stroke="#fbbf24"
              strokeDasharray="4 4"
              label={{ position: 'top', value: 'Forecast →', fill: '#fbbf24', fontSize: 11 }}
            />
          )}

          <Area
            type="monotone"
            dataKey={dataKey}
            stroke={color}
            strokeWidth={2}
            fillOpacity={1}
            fill={`url(#color${dataKey})`}
            dot={false}
            activeDot={{ r: 4, stroke: color, strokeWidth: 2, fill: '#0f172a' }}
          />
        </RechartsAreaChart>
      </ResponsiveContainer>
    </div>
  );
};
