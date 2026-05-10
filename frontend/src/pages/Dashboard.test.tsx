import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';
import { Dashboard } from './Dashboard';

// Mock the dependencies
vi.mock('@tanstack/react-query', () => ({
  useQuery: vi.fn().mockReturnValue({
    data: [
      { id: '1', farm_name: 'Test Farm 1', location_name: 'Coimbatore', latitude: 11.0, longitude: 77.0 },
    ],
    isLoading: false,
  }),
  useMutation: vi.fn().mockReturnValue({
    mutate: vi.fn(),
    isPending: false,
    data: null,
  }),
}));

vi.mock('../store', () => ({
  useAppStore: vi.fn().mockReturnValue({
    setSelectedFarm: vi.fn(),
  }),
}));

// Mock framer-motion to avoid animation issues in tests
vi.mock('framer-motion', async () => {
  const actual = await vi.importActual('framer-motion');
  return {
    ...actual as any,
    motion: {
      div: ({ children, className }: any) => <div className={className}>{children}</div>,
    },
  };
});

describe('Dashboard', () => {
  it('renders the Dashboard header and farm list', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('Regional Intelligence Overview')).toBeInTheDocument();
    
    // Check if the mocked farm is rendered in the table
    expect(screen.getByText('Test Farm 1')).toBeInTheDocument();
    expect(screen.getByText('Coimbatore')).toBeInTheDocument();
  });
});
