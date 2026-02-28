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

function Greeting() {
  return (<div>
            <h1>Campus Transit Portal</h1>
            <h2>Purchase Parking Passes, Check For Citations, and Access Parking Garages.</h2>
          </div>
    );
}

function Home() {
  return (
    <div>
      <Greeting />
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
        <Route path="checkTickets" element={<h1>Check Citations Page (Under Construction)</h1>}/>
        <Route path="citation" element={<h1>Write Citation Page (Under Construction)</h1>}/>
        <Route path="revokePass" element={<h1>Revoke Parking Pass Page (Under Construction)</h1>}/>
        <Route path="removeTicket" element={<h1>Remove Citation Page (Under Construction)</h1>}/>
        <Route path="*" element={<h1>Error 404 Page Not Found</h1>}/>
      </Routes>
    </div>
  );
}

export default App
