import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'

const Toggle = () => {
  const [toggle, setToggle] = useState(true)

  function handleClick(event) {
    event.preventDefault()

    if(toggle) {
      fetch('https://192.168.1.114/api/start')
        .then(response => response.json())
        .then(data => console.log(data))
        .then(() => setToggle(!toggle))
    } else {
      fetch('https://192.168.1.114/api/stop')
        .then(response => response.json())
        .then(data => console.log(data))
        .then(() => setToggle(!toggle))
    }

  }

  return (
    <>
      {toggle
        ? <Button variant='success' style={{display: 'block', margin: '0.5rem auto'}} onClick={handleClick}>Start Motors</Button>
        : <Button variant='danger' style={{display: 'block', margin: '0.5rem auto'}} onClick={handleClick}>Stop Motors</Button>
      }
    </>
  )
}
export default Toggle
