import React, { useState, useEffect } from 'react'

const PWM = () => {
  const [fl, setFL] = useState(0.0)
  const [fr, setFR] = useState(0.0)
  const [bl, setBL] = useState(0.0)
  const [br, setBR] = useState(0.0)

  useEffect(() => {
    getPWM()
  }, [])

  function getPWM() {
    fetch('https://192.168.1.114/api/pwm')
      .then(response => response.json())
      .then(data => {
        setFL(data.fl)
        setFR(data.fr)
        setBL(data.bl)
        setBR(data.br)
      })
    setTimeout(getPWM, 1000)
  }

  return(
    <>
      <p className='p-4 text-center'>Front Right: {fr}</p>
      <p className='p-4 text-center'>Front Left: {fl}</p>
      <h1 className='p-3 text-center'>Drone</h1>
      <p className='p-4 text-center'>Back Right: {br}</p>
      <p className='p-4 text-center'>Back Left: {bl}</p>
    </>
  )
}
export default PWM
