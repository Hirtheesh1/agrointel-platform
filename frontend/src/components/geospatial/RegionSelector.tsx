import { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { MapPin, Target } from 'lucide-react';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface ClickCaptureProp {
  onMapClick: (lat: number, lng: number) => void;
}

const ClickCapture = ({ onMapClick }: ClickCaptureProp) => {
  useMapEvents({
    click: (e) => {
      onMapClick(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
};

interface RegionSelectorProps {
  onRegionSelected: (lat: number, lon: number, radiusKm: number) => void;
}

export const RegionSelector = ({ onRegionSelected }: RegionSelectorProps) => {
  const [selectedPoint, setSelectedPoint] = useState<[number, number] | null>(null);
  const [radiusKm, setRadiusKm] = useState(5);
  const tamilNaduCenter: [number, number] = [11.1271, 78.6569];

  const handleMapClick = (lat: number, lng: number) => {
    setSelectedPoint([lat, lng]);
  };

  const handleAnalyze = () => {
    if (selectedPoint) {
      onRegionSelected(selectedPoint[0], selectedPoint[1], radiusKm);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between bg-surface border border-slate-800 p-4 rounded-xl">
        <div className="flex items-center gap-2">
          <Target className="h-5 w-5 text-primary-400" />
          <div>
            <h3 className="text-sm font-medium text-text-primary">Select Analysis Region</h3>
            <p className="text-xs text-slate-400">Click anywhere on the map to select a farm location</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <label className="text-xs text-slate-400">Radius:</label>
            <select
              className="bg-slate-800 border border-slate-700 text-xs rounded px-2 py-1 text-slate-200"
              value={radiusKm}
              onChange={(e) => setRadiusKm(Number(e.target.value))}
            >
              {[2, 5, 10, 20, 50].map(r => <option key={r} value={r}>{r} km</option>)}
            </select>
          </div>
          <button
            onClick={handleAnalyze}
            disabled={!selectedPoint}
            className="bg-primary-500 text-white text-xs font-medium px-3 py-1.5 rounded-lg hover:bg-primary-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Analyze Zone
          </button>
        </div>
      </div>

      {selectedPoint && (
        <div className="text-xs text-slate-400 bg-slate-900/50 px-3 py-2 rounded-lg border border-slate-800 flex items-center gap-2">
          <MapPin className="h-3 w-3 text-primary-400" />
          Selected: {selectedPoint[0].toFixed(4)}°N, {selectedPoint[1].toFixed(4)}°E — Radius: {radiusKm} km
        </div>
      )}

      <div className="h-[380px] w-full rounded-xl overflow-hidden border border-slate-800">
        <MapContainer center={tamilNaduCenter} zoom={7} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <ClickCapture onMapClick={handleMapClick} />
          {selectedPoint && (
            <>
              <Marker position={selectedPoint}>
                <Popup>
                  <p className="text-xs font-medium">Selected Zone</p>
                  <p className="text-xs">{selectedPoint[0].toFixed(4)}, {selectedPoint[1].toFixed(4)}</p>
                </Popup>
              </Marker>
              <Circle
                center={selectedPoint}
                radius={radiusKm * 1000}
                pathOptions={{ color: '#22c55e', fillColor: 'rgba(34,197,94,0.15)', weight: 2 }}
              />
            </>
          )}
        </MapContainer>
      </div>
    </div>
  );
};
