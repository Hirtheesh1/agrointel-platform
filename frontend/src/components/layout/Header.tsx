import React from 'react';
import { Menu, Search, User } from 'lucide-react';
import { useAppStore } from '../../store';

export const Header = () => {
  const { toggleSidebar } = useAppStore();

  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-800 bg-surface px-4 sm:px-6 lg:px-8">
      <div className="flex flex-1 items-center">
        <button
          type="button"
          className="text-slate-400 hover:text-slate-300 focus:outline-none"
          onClick={toggleSidebar}
        >
          <span className="sr-only">Toggle sidebar</span>
          <Menu className="h-6 w-6" aria-hidden="true" />
        </button>
        <div className="ml-4 flex flex-1">
          <div className="relative w-full max-w-md">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <Search className="h-5 w-5 text-slate-400" aria-hidden="true" />
            </div>
            <input
              id="search"
              name="search"
              className="block w-full rounded-md border-0 bg-slate-800 py-1.5 pl-10 pr-3 text-slate-300 placeholder:text-slate-400 focus:bg-slate-700 focus:ring-0 sm:text-sm sm:leading-6"
              placeholder="Search regions or metrics..."
              type="search"
            />
          </div>
        </div>
      </div>
      <div className="ml-4 flex items-center md:ml-6">
        <div className="relative ml-3">
          <button className="flex max-w-xs items-center rounded-full bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 focus:ring-offset-slate-800 p-1">
            <span className="sr-only">Open user menu</span>
            <User className="h-6 w-6 text-slate-300" />
          </button>
        </div>
      </div>
    </header>
  );
};
