import { create } from 'zustand';
import type { Farm } from '../types';

interface AppState {
  selectedFarm: Farm | null;
  setSelectedFarm: (farm: Farm) => void;
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  selectedFarm: null,
  setSelectedFarm: (farm) => set({ selectedFarm: farm }),
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
}));
