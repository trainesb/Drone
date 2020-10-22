import React from 'react';

import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

// Controller
import PWM from './Controller/PWM.jsx'
import PID from './Controller/PID.jsx'
import Prime from './Controller/Prime.jsx'
import Toggle from './Controller/Toggle.jsx'
import Throttle from './Controller/Throttle.jsx'
import DesiredAngles from './Controller/DesiredAngles.jsx'

// Sensors
import Temp from './Sensors/Temp.jsx'
import Turn from './Sensors/Turn.jsx'
import Speed from './Sensors/Speed.jsx'
import Vario from './Sensors/Vario.jsx'
import Altitude from './Sensors/Altitude.jsx'
import Heading from './Sensors/Heading.jsx'
import Attitude from './Sensors/Attitude.jsx'
import MonitorCamera from './Sensors/MonitorCamera.jsx'

function App() {
  return (
    <div className="App">
      <header style={{backgroundColor: 'lightgrey', display: 'flex', justifyContent: 'space-around'}}>
        <PWM />
      </header>
      <Container fluid>
        <Row>
          <Col sm={12} style={{display: 'flex', justifyContent: 'space-around'}}>
            <PID />
            <DesiredAngles />
            <Throttle />
            <div style={{width: '9rem', border: 'solid thin grey', borderRadius: '0.5rem'}} className='p-2 text-center'>
              <Prime />
              <Toggle />
            </div>
            <Temp />
          </Col>
        </Row>

        <Row>
          <Col sm={2}>
            <Attitude />
            <Heading />
            <Speed />
          </Col>
          <Col sm={8}>
            <MonitorCamera />
          </Col>
          <Col sm={2}>
            <Turn />
            <Vario />
            <Altitude />
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
