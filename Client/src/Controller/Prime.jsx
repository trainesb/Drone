import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'

const Prime = () => {
  const [primed, setPrimed] = useState(false)

  function handleClick(event) {
    event.preventDefault()

    fetch('https://192.168.1.114/api/prime')
      .then(response => response.json())
      .then(data => console.log(data))
      .then(() => setPrimed(true))
  }

  return(
    <Button variant={primed ? 'secondary' : 'success'} disabled={primed} onClick={handleClick} style={{display: 'block', margin: '0.5rem auto'}}>Prime Motors</Button>
  )
}
export default Prime
