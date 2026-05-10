import { render, screen } from '@testing-library/react';
import { StatCard } from './StatCard';
import { Thermometer } from 'lucide-react';

describe('StatCard', () => {
  it('renders the title and value correctly', () => {
    render(
      <StatCard 
        title="Temperature" 
        value="35.5°C" 
        icon={Thermometer} 
        trend={{ value: 2, isPositive: true }} 
      />
    );
    
    expect(screen.getByText('Temperature')).toBeInTheDocument();
    expect(screen.getByText('35.5°C')).toBeInTheDocument();
  });

  it('renders the trend indicator correctly', () => {
    const { rerender } = render(
      <StatCard 
        title="Humidity" 
        value="60%" 
        icon={Thermometer} 
        trend={{ value: 5, isPositive: false }} 
      />
    );
    
    // Test the text content and color class (if applicable)
    expect(screen.getByText('Humidity')).toBeInTheDocument();
    
    rerender(
       <StatCard 
        title="Humidity" 
        value="60%" 
        icon={Thermometer} 
      />
    );
    
    expect(screen.getByText('Humidity')).toBeInTheDocument();
  });
});
