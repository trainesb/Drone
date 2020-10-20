import React, { useState } from 'react'
import Button from 'react-bootstrap/Button'

const Prime = () => {
  const [primed, setPrimed] = useState(true)

  function handleClick(event) {
    event.preventDefault()

    fetch('https://192.168.1.114/api/prime')
      .then(response => response.json())
      .then(data => console.log(data))
      .then(() => setPrimed(false))
  }

  return(
    <Button variant={primed ? 'success' : 'secondary'} disabled={primed} onClick={handleClick} style={{display: 'block', margin: '0.5rem auto'}}>Prime Motors</Button>
  )
}
export default Prime
