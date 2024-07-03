// Import necessary modules from react-router-dom
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import LoginForm from './Components/LoginForm.jsx';
import SignUpForm from './Components/SignUpForm.jsx';
import Topbar from './Components/Dashboard.jsx';
import Profile from './Components/Profile.jsx';
import {CookiesProvider,useCookies} from 'react-cookie'

// Wrap your entire application with Router component
function App() {
  const [cookies,setCookie] = useCookies(['user'])

  function handlLog(user)  {
    setCookie('user',user,{path:'/'})
  }
  return (
    <CookiesProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<LoginForm handlLog={handlLog}/>} />
            <Route path="/login" element={<LoginForm />} />
            <Route path="/signup" element={<SignUpForm />} />
            <Route path="/dashboard" element={<Topbar/>} />
            <Route path='/profile' element={<Profile/>} />
          </Routes>
        </div>
      </Router>
    </CookiesProvider>
  );
}

export default App;
