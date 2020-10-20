import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'

const Start = () => {
  return (
    <Button variant='success' style={{display: 'block', margin: '0.5rem auto'}}>Start Motors</Button>
  )
}

const Stop = () => {
  return (
    <Button variant='danger' style={{display: 'block', margin: '0.5rem auto'}}>Stop Motors</Button>
  )
}

const Toggle = () => {
  const [toggle, setToggle] = useState(true)

  function handleClick(event) {
    event.preventDefault()

    let url = '/api/start'
    if(!toggle) { url = '/api/stop' }
    fetch('https://192.168.1.114' + url)
      .then(response => response.json())
      .then(data => console.log(data))
      .then(() => setToggle(!toggle))
  }

  return (
    <>
      {toggle
        ? <Start onClick={handleClick} />
        : <Stop onClick={handleClick} />
      }
    </>
  )
}
export default Toggle
