import React, { useState, useEffect } from 'react'

const Temp = () => {
  const [tempF, setTempF] = useState(0.0)
  const [tempC, setTempC] = useState(0.0)
  const [preassure, setPressure] = useState(0.0)

  useEffect(() => {
    getTemp()
  }, [])

  function getTemp() {
    fetch('https://192.168.1.114/api/BMP280')
      .then(response => response.json())
      .then(data => {
        setTempC(data.temp)
        setTempF((data.temp * 9/5) + 32)
        setPressure(data.pressure)
      })
    setTimeout(getTemp, 1000)
  }

  return (
    <div style={{width: '9rem', border: 'solid thin grey', borderRadius: '0.5rem'}} className='p-2'>
      <p style={{margin: '0.5rem auto'}}>Temp F: {tempF.toFixed(2)}</p>
      <p style={{margin: '0.5rem auto'}}>Temp C: {tempC.toFixed(2)}</p>
      <p style={{margin: '0.5rem auto'}}>Preassure: {preassure.toFixed(2)}</p>
    </div>
  )
}
export default Temp
