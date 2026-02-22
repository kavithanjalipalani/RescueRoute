import React from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

export default function MapRoute({route}){
  const center = [11.0168,76.9558]
  const positions = route.map(r => [r.lat, r.lng])
  return (
    <div style={{height: '350px', marginTop: '12px'}}>
      <MapContainer center={center} zoom={13} style={{height:'100%', width:'100%'}}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {route.map(r => <Marker key={r.id} position={[r.lat, r.lng]}><Popup>{r.name}</Popup></Marker>)}
        <Polyline positions={positions} />
      </MapContainer>
    </div>
  )
}
