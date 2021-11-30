import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Home from "./routes/main/home";
import Login from "./routes/main/login";
import Logout from "./routes/main/logout";
import StudentDashboard from './routes/student/dashboard';

import 'bootstrap/dist/css/bootstrap.min.css';
import "./App.min.css";
import "./components/components.min.css";
import "./routes/main/main.min.css";

const portals = ['/student', '/teacher', '/parent', '/management', '/admin'];

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Routes>
                    <Route exact path='/' element={<Home />} />

                    <Route exact path="/login" element={<Login />} />
                    <Route exact path="/logout" element={<Logout />} />

                    {/* Redirect to dashboard in case of navigation to "portals" */}
                    {portals.map((r, index) => {
                        return <Route exact path={r} key={index} element={<Navigate to='dashboard/' />} />
                    })}

                    {/* Student */}
                    <Route path="/student/dashboard" element={<StudentDashboard />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
};

export default App;