import './App.css'
import MenuBar from './MenuBar';
import './MenuBar.css'
import { Route, Routes } from 'react-router-dom';
import Login from './Login';
import { ApiClientGetUserInfo } from './ApiClient.jsx';



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
        <Route path="*" element={<h1>Error 404 Page Not Found</h1>}/>
      </Routes>
    </div>
  );
}

export default App
