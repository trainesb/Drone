import React, { useState, useEffect } from 'react'
import { TurnCoordinator } from 'react-flight-indicators'

const Turn = () => {
  const [turn, setTurn] = useState(0.0)

  useEffect(() => {
    getTurn()
  }, [])

  function getTurn() {
    fetch('https://192.168.1.114/api/MPU/rotation')
      .then(response => response.json())
      .then(data => setTurn(data.roll))
    setTimeout(getTurn, 1000)
  }

  return (
    <TurnCoordinator turn={turn} showBox={false} />
  )
}
export default Turn
