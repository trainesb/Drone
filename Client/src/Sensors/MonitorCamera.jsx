import React from 'react'

import Card from 'react-bootstrap/Card'

const MonitorCamera = () => {

  return (
    <Card className="text-center m-3" style={{height: '40rem'}}>
      <Card.Body>
        <Card.Title>Monitor Camera</Card.Title>
        <img src="https://192.168.1.114/api/video_stream" alt="video stream" style={{ width: '100%' }} />
      </Card.Body>
    </Card>
  )
}
export default MonitorCamera
