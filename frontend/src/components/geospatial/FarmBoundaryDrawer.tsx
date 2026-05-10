import { useState } from 'react';
import { MapContainer, TileLayer, Polygon, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Pencil, Trash2, CheckCircle2 } from 'lucide-react';

interface FarmBoundaryDrawerProps {
  onBoundaryComplete: (geojson: object) => void;
}

const PolygonDrawer = ({ onPointAdded }: { onPointAdded: (lat: number, lng: number) => void }) => {
  useMapEvents({
    click: (e) => onPointAdded(e.latlng.lat, e.latlng.lng),
  });
  return null;
};

export const FarmBoundaryDrawer = ({ onBoundaryComplete }: FarmBoundaryDrawerProps) => {
  const [points, setPoints] = useState<[number, number][]>([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const tamilNaduCenter: [number, number] = [11.1271, 78.6569];

  const handlePointAdded = (lat: number, lng: number) => {
    if (!isDrawing) return;
    setPoints(prev => [...prev, [lat, lng]]);
  };

  const handleFinish = () => {
    if (points.length < 3) return;
    setIsDrawing(false);
    // Build GeoJSON Polygon
    const geojson = {
      type: 'Polygon',
      coordinates: [[...points.map(([lat, lng]) => [lng, lat]), [points[0][1], points[0][0]]]]
    };
    onBoundaryComplete(geojson);
  };

  const handleReset = () => {
    setPoints([]);
    setIsDrawing(false);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between bg-surface border border-slate-800 p-3 rounded-xl">
        <div className="flex items-center gap-2">
          <Pencil className="h-4 w-4 text-emerald-400" />
          <p className="text-sm text-slate-300">
            {isDrawing ? `Drawing... ${points.length} points placed` : 'Boundary Drawer'}
          </p>
        </div>
        <div className="flex gap-2">
          {!isDrawing ? (
            <button
              onClick={() => setIsDrawing(true)}
              className="bg-emerald-600 text-white text-xs font-medium px-3 py-1.5 rounded-lg hover:bg-emerald-700 transition-colors"
            >
              Start Drawing
            </button>
          ) : (
            <>
              <button
                onClick={handleFinish}
                disabled={points.length < 3}
                className="bg-blue-600 text-white text-xs font-medium px-3 py-1.5 rounded-lg hover:bg-blue-700 disabled:opacity-40 flex items-center gap-1 transition-colors"
              >
                <CheckCircle2 className="h-3 w-3" /> Finish
              </button>
              <button
                onClick={handleReset}
                className="bg-red-600/30 text-red-400 text-xs font-medium px-3 py-1.5 rounded-lg hover:bg-red-600/50 flex items-center gap-1 transition-colors"
              >
                <Trash2 className="h-3 w-3" /> Reset
              </button>
            </>
          )}
        </div>
      </div>

      <div className="h-[340px] w-full rounded-xl overflow-hidden border border-slate-800">
        <MapContainer center={tamilNaduCenter} zoom={8} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <PolygonDrawer onPointAdded={handlePointAdded} />
          {points.length > 1 && (
            <Polygon
              positions={points}
              pathOptions={{ color: '#f59e0b', fillColor: 'rgba(245,158,11,0.2)', weight: 2, dashArray: '6' }}
            />
          )}
        </MapContainer>
      </div>

      {points.length > 0 && (
        <p className="text-xs text-slate-400">
          {points.length} vertices · Click <strong>Finish</strong> when boundary is complete (min 3 points)
        </p>
      )}
    </div>
  );
};
