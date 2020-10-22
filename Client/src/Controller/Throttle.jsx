import React, { useState, useEffect } from 'react'

const Throttle = () => {
  const [freq, setFreq] = useState(1000)

  useEffect(() => {
    fetch('https://192.168.1.114/api/throttle')
      .then(response => response.json())
      .then(data => setFreq(data.throttle))
  }, [])

  function handleChange(event) {
    event.preventDefault()
    const val = event.target.value
    setFreq(val)
    fetch('https://192.168.1.114/api/throttle/' + val)
      .then(response => response.json())
      .then(data => console.log(data))
  }

  return(
    <div style={{width: '20rem', border: 'solid thin grey', borderRadius: '0.5rem'}} className='p-2 text-center'>
      <h3 style={{margin: '0.5rem auto'}}>Throttle Freq: {freq}</h3>
      <input type="number" min="1000" step="1" max="2500" value={freq} onChange={handleChange} style={{margin: '0.5rem auto'}}/>
    </div>
  )
}
export default Throttle
