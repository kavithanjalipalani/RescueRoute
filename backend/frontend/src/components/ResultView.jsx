import React, {useState} from 'react'
import MapRoute from './MapRoute'
import axios from 'axios'

export default function ResultView({data}){
  const [route, setRoute] = useState(null)
  const inference = data.inference
  const ngos = data.suggested_ngos || []

  const handleRoute = async () => {
    try {
      const ids = ngos.map(n => n.id).join(',')
      const res = await axios.post('http://127.0.0.1:8000/route', new URLSearchParams({
        start_lat: 11.0168, start_lng: 76.9558, pickup_ids: ids
      }))
      setRoute(res.data.route_order)
    } catch (err) {
      alert("Route error")
      console.error(err)
    }
  }

  return (
    <div className="result-card">
      <h2>Result — {inference.label.toUpperCase()}</h2>
      <p><strong>Food type:</strong> {inference.food_type}</p>
      <p><strong>Edibility score:</strong> {inference.edibility_score}</p>
      <p><strong>Quantity:</strong> {inference.quantity}</p>

      <h3>Suggested NGOs</h3>
      <ul>
        {ngos.map(n => <li key={n.id}>{n.name} — {n.contact}</li>)}
      </ul>

      <button onClick={handleRoute}>Show Optimized Route</button>

      {route && <MapRoute route={route} />}
    </div>
  )
}
