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

    fetch('https://192.168.1.114/api/throttle/' + event.target.value)
      .then(response => response.json())
      .then(data => console.log(data))
      .then(() => setFreq(event.target.value))
  }

  return(
    <div style={{width: '20rem', border: 'solid thin grey', borderRadius: '0.5rem'}} className='p-2 text-center'>
      <h3 style={{margin: '0.5rem auto'}}>Throttle Freq: {freq}</h3>
      <input type="range" min="1000" max="2500" value={freq} onChange={handleChange} style={{margin: '0.5rem auto'}}/>
    </div>
  )
}
export default Throttle
