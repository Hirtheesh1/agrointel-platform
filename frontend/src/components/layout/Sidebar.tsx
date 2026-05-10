import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, LineChart, ThermometerSun, Map, BrainCircuit, Bell, Settings, Tractor } from 'lucide-react';
import { clsx } from 'clsx';
import { useAppStore } from '../../store';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Farm Management', href: '/farm', icon: Tractor },
  { name: 'Forecasting', href: '/forecasting', icon: LineChart },
  { name: 'Environmental Analytics', href: '/analytics', icon: ThermometerSun },
  { name: 'Tamil Nadu Regions', href: '/regions', icon: Map },
  { name: 'Explainable AI', href: '/explainability', icon: BrainCircuit },
  { name: 'Alerts', href: '/alerts', icon: Bell },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export const Sidebar = () => {
  const { isSidebarOpen } = useAppStore();

  return (
    <div
      className={clsx(
        'flex h-full flex-col bg-surface border-r border-slate-800 transition-all duration-300',
        isSidebarOpen ? 'w-64' : 'w-20'
      )}
    >
      <div className="flex h-16 items-center justify-center border-b border-slate-800 px-4">
        <h1 className={clsx('text-xl font-bold text-primary-500 transition-all', !isSidebarOpen && 'scale-0')}>
          AgroIntel AI
        </h1>
        {!isSidebarOpen && <span className="text-xl font-bold text-primary-500 absolute">AI</span>}
      </div>
      <nav className="flex-1 space-y-1 px-2 py-4">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              clsx(
                isActive ? 'bg-primary-900 text-primary-500' : 'text-slate-300 hover:bg-surface-hover',
                'group flex items-center rounded-md px-2 py-2 text-sm font-medium transition-colors'
              )
            }
          >
            <item.icon
              className={clsx(
                'mr-3 h-5 w-5 flex-shrink-0',
                isSidebarOpen ? 'mr-3' : 'mx-auto'
              )}
              aria-hidden="true"
            />
            {isSidebarOpen && <span>{item.name}</span>}
          </NavLink>
        ))}
      </nav>
    </div>
  );
};
