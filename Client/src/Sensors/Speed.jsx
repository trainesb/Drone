import React, { useState, useEffect } from 'react'
import { Airspeed } from 'react-flight-indicators'

const Speed = () => {
  const [speed, setSpeed] = useState(0.0)

  useEffect(() => {
    getSpeed()
  }, [])

  function getSpeed() {
    fetch('https://192.168.1.114/api/speed')
      .then(response => response.json())
      .then(data => setSpeed(data.velocity_x))
    setTimeout(getSpeed, 1000)
  }

  return (
    <>
      <Airspeed speed={speed} showBox={false} />
      <p className="text-center">Speed: {speed}</p>
    </>
  )
}
export default Speed
