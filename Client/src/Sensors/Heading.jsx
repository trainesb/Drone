import React, { useState, useEffect } from 'react'
import { HeadingIndicator } from 'react-flight-indicators'

const Heading = () => {
  const [heading, setHeading] = useState(0)

  useEffect(() => {
    hmc()
  }, [])

  function hmc() {
    fetch('https://192.168.1.114/api/heading')
      .then(response => response.json())
      .then(data => setHeading(data.heading))
    setTimeout(hmc, 1000)
  }

  return(
    <HeadingIndicator heading={heading} showBox={false} />
  )
}
export default Heading
