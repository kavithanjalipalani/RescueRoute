import React from 'react'
import UploadForm from './components/UploadForm'
import './styles.css'

function App(){
  return (
    <div className="app">
      <header><h1>RescueRoute — Food Rescue Demo</h1></header>
      <main>
        <UploadForm />
      </main>
      <footer>Team RescueRoute — PSG AI4Dev</footer>
    </div>
  )
}
export default App
