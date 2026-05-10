import { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useAppStore } from '../../store';

// Fix for default marker icon in leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface FarmMapProps {
  onLocationSelect?: (lat: number, lon: number) => void;
  radiusKm?: number;
}

export const FarmMap = ({ onLocationSelect, radiusKm = 5.0 }: FarmMapProps) => {
  const { selectedFarm } = useAppStore();
  
  // Default to central Tamil Nadu if no farm selected
  const defaultCenter = [11.1271, 78.6569];
  const center = selectedFarm && selectedFarm.latitude && selectedFarm.longitude 
    ? [selectedFarm.latitude, selectedFarm.longitude] 
    : defaultCenter;

  return (
    <div className="h-[400px] w-full rounded-xl overflow-hidden border border-slate-800 z-0 relative">
      <MapContainer 
        center={center as [number, number]} 
        zoom={selectedFarm ? 12 : 7} 
        style={{ height: '100%', width: '100%', zIndex: 0 }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {selectedFarm && selectedFarm.latitude && selectedFarm.longitude && (
          <>
            <Marker position={[selectedFarm.latitude, selectedFarm.longitude]}>
              <Popup>
                <div className="text-slate-800">
                  <p className="font-bold">{selectedFarm.farm_name}</p>
                  <p className="text-sm">{selectedFarm.location_name}</p>
                </div>
              </Popup>
            </Marker>
            <Circle 
              center={[selectedFarm.latitude, selectedFarm.longitude]} 
              radius={radiusKm * 1000} // Leaflet uses meters
              pathOptions={{ color: 'rgba(59, 130, 246, 0.5)', fillColor: 'rgba(59, 130, 246, 0.2)' }}
            />
          </>
        )}
      </MapContainer>
    </div>
  );
};
