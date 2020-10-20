import React, { useState, useEffect } from 'react'

const DesiredAngles = () => {
  const [x, setX] = useState(0.0)
  const [y, setY] = useState(0.0)

  useEffect(() => {
    fetch('https://192.168.1.114/api/desired/angles')
      .then(response => response.json())
      .then(data => {
        setX(data.desired_angel_x)
        setY(data.desired_angel_y)
      })
  }, [])

  function handleChange(event) {
    event.preventDefault()

    fetch('https://192.168.1.114/api/desired/angle/' + event.target.name + '/' + event.target.value)
      .then(response => response.json())
      .then(data => console.log(data))
      .then(() => {
        if (event.target.name === 'y') { setY(event.target.value) }
        else if (event.target.name === 'x') { setX(event.target.value) }
      })
  }

  return (
    <div style={{width: '14rem', border: 'solid thin grey', borderRadius: '0.5rem'}} className='p-2'>
      <label for='y' style={{width: '8rem', margin: '0.5rem auto'}}>Desired Angle Y:</label>
      <input name='y' type="number" min="0" max="360" step="0.1" value={y} onChange={handleChange} style={{width: '4rem', margin: '0.5rem auto', paddingLeft: '0.5rem'}} />

      <label for='x' style={{width: '8rem', margin: '0.5rem auto'}}>Desired Angle X:</label>
      <input name='x' type="number" min="0" max="360" step="0.1" value={x} onChange={handleChange} style={{width: '4rem', margin: '0.5rem auto', paddingLeft: '0.5rem'}} />
    </div>
  )
}
export default DesiredAngles
