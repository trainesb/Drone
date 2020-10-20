import React, { useState, useEffect } from 'react'

const PID = () => {
  const [kp, setKP] = useState(0.0)
  const [ki, setKI] = useState(0.0)
  const [kd, setKD] = useState(0.0)

  useEffect(() => {
    fetch('https://192.168.1.114/api/PID')
      .then(response => response.json())
      .then(data => {
        setKP(data.kp)
        setKI(data.ki)
        setKD(data.kd)
      })
  }, [])

  function handleChange(event) {
    event.preventDefault()

    fetch('https://192.168.1.114/api/PID/' + event.target.name + '/' + event.target.value)
      .then(response => response.json())
      .then(data => console.log(data))
      .then(() => {
        if(event.target.name === 'kp') { setKP(event.target.value) }
        if(event.target.name === 'ki') { setKI(event.target.value) }
        if(event.target.name === 'kd') { setKD(event.target.value) }
      })
  }

  return(
    <div style={{width: '9rem', border: 'solid thin grey', borderRadius: '0.5rem'}} className='p-2'>
      <label for='kp' style={{width: '2rem'}}>kp:</label>
      <input name='kp' type="number" min="0" step="0.001" value={kp} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />

      <label for='ki' style={{width: '2rem'}}>ki:</label>
      <input name='ki' type="number" min="0" step="0.001" value={ki} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />

      <label for='kd' style={{width: '2rem'}}>kd:</label>
      <input name='kd' type="number" min="0" step="0.001" value={kd} onChange={handleChange} style={{width: '5rem', paddingLeft: '0.5rem'}} />
    </div>
  )
}
export default PID
