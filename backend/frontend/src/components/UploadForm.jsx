import React, {useState} from 'react'
import axios from 'axios'
import ResultView from './ResultView'

export default function UploadForm(){
  const [file, setFile] = useState(null)
  const [text, setText] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const form = new FormData()
      if(file) form.append('file', file)
      form.append('text', text)
      const res = await axios.post('http://127.0.0.1:8000/predict', form)
      setResult(res.data)
    } catch (err) {
      alert("Error: " + (err.message || "failed"))
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upload-card">
      <form onSubmit={handleSubmit}>
        <label>Upload food photo</label>
        <input type="file" accept="image/*" onChange={e=>setFile(e.target.files[0])} />
        <label>Describe (quantity/time) — e.g. "30 meals cooked 2 hours ago lat:11.02 lng:76.95"</label>
        <textarea value={text} onChange={e=>setText(e.target.value)} />
        <button type="submit" disabled={loading}>{loading ? "Analyzing..." : "Analyze & Find NGO"}</button>
      </form>
      {result && <ResultView data={result} />}
    </div>
  )
}
