import React, { useState, useEffect } from 'react'
import { Altimeter } from 'react-flight-indicators'

const Altitude = () => {
  const [tempC, setTempC] = useState(0.0)
  const [tempF, setTempF] = useState(0.0)
  const [pressure, setPressure] = useState(0.0)
  const [altitude, setAltitude] = useState(0.0)

  useEffect(() => {
    bmp()
  }, [])

  function bmp() {
    fetch('https://192.168.1.114/api/BMP280')
      .then(response => response.json())
      .then(data => setAltitude(data.altitude * 3.281))
    setTimeout(bmp, 1000)
  }

  return(
    <>
      <Altimeter altitude={altitude} showBox={false} />
      <p className="text-center">Altitude: {altitude}</p>
    </>
  )
}
export default Altitude
