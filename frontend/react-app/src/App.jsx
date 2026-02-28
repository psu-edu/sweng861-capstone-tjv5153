import './App.css'
import MenuBar from './MenuBar';
import './MenuBar.css'
import { Route, Routes } from 'react-router-dom';
import Login from './Login';
import { ApiClientGetUserInfo } from './ApiClient.jsx';
import Dashboard from './Dashboard';
import OfficerDashboard from './OfficerDashboard.jsx';
import GetParkingPass from './GetParkingPass.jsx';
import PassSuccess from './PassSuccess.jsx';
import LicensePlate from './LicensePlate.jsx';
import AccessGranted from './AccessGranted.jsx';
import Citation from './Citation.jsx';
import CheckTickets from './CheckTickets.jsx';
import RevokeParkingPass from './RevokeParkingPass.jsx';
import RemoveCitation from './RemoveCitation.jsx';

function Greeting() {
  return (<div>
            <h1>Penn State Transit Portal</h1>
            <h2>Purchase Parking Passes, Check For Citations, and Access Parking Garages.</h2>
          </div>
    );
}

function Home() {
  return (
    <div>
      <div className="home-container">
        <div className="home-picture">
          <img src="src/assets/BehrendGarage.jpg"/>
        </div>
        <div className="home-header">
          <Greeting />
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <div>
      <MenuBar />
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/dashboard" element={<Dashboard/>}/>
        <Route path="/officerDashboard" element={<OfficerDashboard/>}/>
        <Route path="/parkingPass" element={<GetParkingPass/>}/>
        <Route path="/passSuccess" element={<PassSuccess/>}/>
        <Route path="/licensePlate" element={<LicensePlate/>}/>
        <Route path="/accessGranted" element={<AccessGranted/>}/>
        <Route path="/checkTickets" element={<CheckTickets/>}/>
        <Route path="/citation" element={<Citation/>}/>
        <Route path="/revokePass" element={<RevokeParkingPass/>}/>
        <Route path="/removeTicket" element={<RemoveCitation/>}/>
        <Route path="*" element={<h1>Error 404 Page Not Found</h1>}/>
      </Routes>
    </div>
  );
}

export default App
