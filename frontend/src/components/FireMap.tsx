import { CircleMarker, MapContainer, TileLayer, useMap } from 'react-leaflet'
import { useEffect } from 'react'

function Recenter({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap()
  useEffect(() => {
    map.setView([lat, lng], map.getZoom())
  }, [lat, lng, map])
  return null
}

export default function FireMap({ latitude, longitude }: { latitude: number; longitude: number }) {
  return (
    <div className="overflow-hidden rounded-[10px] border border-graphite" style={{ height: 360 }}>
      <MapContainer center={[latitude, longitude]} zoom={7} scrollWheelZoom={false} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a> &copy; OpenStreetMap contributors'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        <CircleMarker
          center={[latitude, longitude]}
          radius={10}
          pathOptions={{ color: '#cc9166', fillColor: '#cc9166', fillOpacity: 0.5, weight: 2 }}
        />
        <Recenter lat={latitude} lng={longitude} />
      </MapContainer>
    </div>
  )
}
