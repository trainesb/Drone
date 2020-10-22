import React, { useState, useEffect } from 'react'
import { AttitudeIndicator } from 'react-flight-indicators'

const Attitude = () => {
  const [pitch, setPitch] = useState(0.0)
  const [roll, setRoll] = useState(0.0)
  const [totalX, setTotalX] = useState(0.0)
  const [totalY, setTotalY] = useState(0.0)

  useEffect(() => {
    mpu()
  }, [])

  function mpu() {
    fetch('https://192.168.1.114/api/MPU/rotation')
      .then(response => response.json())
      .then(data => {
        console.log(data)
        setPitch(data.pitch)
        setRoll(data.roll)
      })
    setTimeout(mpu, 1000)
  }

  return(
    <>
      <AttitudeIndicator roll={roll} pitch={pitch} showBox={false} />
      <p className="text-center">Pitch: {pitch}  -  Roll: {roll}</p>
    </>
  )
}
export default Attitude
