import React, { useState, useEffect } from 'react'
import { Variometer } from 'react-flight-indicators'

const Vario = () => {
  const [vario, setVario] = useState(0.0)

  useEffect(() => {
    getVario()
  }, [])

  function getVario() {
    fetch('https://192.168.1.114/api/MPU/accel')
      .then(response => response.json())
      .then(data => setVario(data.z))
    setTimeout(getVario, 1000)
  }

  return(
    <Variometer vario={vario} showBox={false} />
  )
}
export default Vario
