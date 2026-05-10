import React from 'react';
import { clsx } from 'clsx';
import type { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  description?: string;
  className?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon: Icon,
  trend,
  description,
  className,
}) => {
  return (
    <div className={clsx('rounded-xl border border-slate-800 bg-surface p-6 shadow-sm', className)}>
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-slate-400">{title}</h3>
        <Icon className="h-5 w-5 text-slate-500" />
      </div>
      <div className="mt-4 flex items-baseline gap-2">
        <p className="text-3xl font-bold text-text-primary">{value}</p>
        {trend && (
          <span
            className={clsx(
              'text-sm font-medium',
              trend.isPositive ? 'text-primary-500' : 'text-red-500'
            )}
          >
            {trend.isPositive ? '+' : '-'}{Math.abs(trend.value)}%
          </span>
        )}
      </div>
      {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
    </div>
  );
};
