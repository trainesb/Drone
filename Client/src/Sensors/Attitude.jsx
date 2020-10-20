import React, { useState, useEffect } from 'react'
import { AttitudeIndicator } from 'react-flight-indicators'

const Attitude = () => {
  const [pitch, setPitch] = useState(0.0)
  const [roll, setRoll] = useState(0.0)

  useEffect(() => {
    mpu()
  }, [])

  function mpu() {
    fetch('https://192.168.1.114/api/mpu')
      .then(response => response.json())
      .then(data => {
        console.log(data)
        setPitch(data.accel_angle_y)
        setRoll(data.accel_angle_x)
      })
    setTimeout(mpu, 1000)
  }

  return(
    <AttitudeIndicator roll={roll} pitch={pitch} showBox={false} />
  )
}
export default Attitude
