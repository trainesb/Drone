import React, { useState, useEffect } from 'react'

const PitchP = () => {
  const [p, setP] = useState(0.0)

  useEffect(() => {
    fetch('https://192.168.1.114/api/PID/pitch/p')
      .then(response => response.json())
      .then(data => setP(data.kp))
  }, [])

  function handleChange(event) {
    event.preventDefault()
    const value = event.target.value
    setP(value)
    fetch('https://192.168.1.114/api/PID/pitch/p/' + value)
      .then(response => response.json())
      .then(data => console.log(data))
  }

  return (
    <>
      <label for='pitch_p' style={{width: '2rem'}}>Pitch p:</label>
      <input name='pitch_p' type="number" min="0.0" step="0.001" value={p} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />
    </>
  )
}

const PitchI = () => {
  const [i, setI] = useState(0.0)

  useEffect(() => {
    fetch('https://192.168.1.114/api/PID/pitch/i')
      .then(response => response.json())
      .then(data => setI(data.ki))
  }, [])

  function handleChange(event) {
    event.preventDefault()
    const value = event.target.value
    setI(value)
    fetch('https://192.168.1.114/api/PID/pitch/i/' + value)
      .then(response => response.json())
      .then(data => console.log(data))
  }

  return (
    <>
      <label for='pitch_i' style={{width: '2rem'}}>Pitch i:</label>
      <input name='pitch_i' type="number" min="0.0" step="0.001" value={i} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />
    </>
  )
}

const PitchD = () => {
  const [d, setD] = useState(0.0)

  useEffect(() => {
    fetch('https://192.168.1.114/api/PID/pitch/d')
      .then(response => response.json())
      .then(data => setD(data.kd))
  }, [])

  function handleChange(event) {
    event.preventDefault()
    const value = event.target.value
    setD(value)
    fetch('https://192.168.1.114/api/PID/pitch/d/' + value)
      .then(response => response.json())
      .then(data => console.log(data))
  }

  return (
    <>
      <label for='pitch_d' style={{width: '2rem'}}>Pitch d:</label>
      <input name='pitch_d' type="number" min="0.0" step="0.001" value={d} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />
    </>
  )
}

const RollP = () => {
  const [p, setP] = useState(0.0)

  useEffect(() => {
    fetch('https://192.168.1.114/api/PID/roll/p')
      .then(response => response.json())
      .then(data => setP(data.kp))
  }, [])

  function handleChange(event) {
    event.preventDefault()
    const value = event.target.value
    setP(value)
    fetch('https://192.168.1.114/api/PID/roll/p/' + value)
      .then(response => response.json())
      .then(data => console.log(data))
  }

  return (
    <>
      <label for='roll_p' style={{width: '2rem'}}>Roll p:</label>
      <input name='roll_p' type="number" min="0.0" step="0.001" value={p} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />
    </>
  )
}

const RollI = () => {
  const [i, setI] = useState(0.0)

  useEffect(() => {
    fetch('https://192.168.1.114/api/PID/roll/i')
      .then(response => response.json())
      .then(data => setI(data.ki))
  }, [])

  function handleChange(event) {
    event.preventDefault()
    const value = event.target.value
    setI(value)
    fetch('https://192.168.1.114/api/PID/roll/i/' + value)
      .then(response => response.json())
      .then(data => console.log(data))
  }

  return (
    <>
      <label for='roll_i' style={{width: '2rem'}}>Roll i:</label>
      <input name='roll_i' type="number" min="0.0" step="0.001" value={i} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />
    </>
  )
}

const RollD = () => {
  const [d, setD] = useState(0.0)

  useEffect(() => {
    fetch('https://192.168.1.114/api/PID/roll/d')
      .then(response => response.json())
      .then(data => setD(data.kd))
  }, [])

  function handleChange(event) {
    event.preventDefault()
    const value = event.target.value
    setD(value)
    fetch('https://192.168.1.114/api/PID/roll/d/' + value)
      .then(response => response.json())
      .then(data => console.log(data))
  }

  return (
    <>
      <label for='roll_d' style={{width: '2rem'}}>Roll d:</label>
      <input name='roll_d' type="number" min="0.0" step="0.001" value={d} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />
    </>
  )
}

const PID = () => {
  return(
    <>
      <div style={{width: '9rem', border: 'solid thin grey', borderRadius: '0.5rem'}} className='p-2'>
        <PitchP />
        <PitchI />
        <PitchD />
      </div>
      <div style={{width: '9rem', border: 'solid thin grey', borderRadius: '0.5rem'}} className='p-2'>
        <RollP />
        <RollI />
        <RollD />
      </div>
    </>
  )
}
export default PID
