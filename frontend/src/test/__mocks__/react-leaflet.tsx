// Mock leaflet and react-leaflet for tests (they don't work in jsdom)
const MockMapContainer = ({ children }: any) => <div data-testid="map-container">{children}</div>;
const MockTileLayer = () => null;
const MockMarker = ({ children }: any) => <div>{children}</div>;
const MockPopup = ({ children }: any) => <div>{children}</div>;
const MockCircle = () => null;
const MockPolygon = () => null;
const useMapEvents = (_handlers: any) => null;

export {
  MockMapContainer as MapContainer,
  MockTileLayer as TileLayer,
  MockMarker as Marker,
  MockPopup as Popup,
  MockCircle as Circle,
  MockPolygon as Polygon,
  useMapEvents,
};
