import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Login from './routes/login';
import Logout from './routes/logout';
// import Test from './routes/test';
import Dashboard from './routes/student/dashboard';


const portals = ['/student', '/teacher', '/parent', '/management', '/admin'];

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Routes>
                    <Route exact path='/' element={<h1>This is home page</h1>} />

                    {/* Login Route */}
                    <Route exact path="/login" element={<Login />} />
                    <Route exact path="/logout" element={<Logout />} />
                    {/* <Route exact path="/test" element={<Test />} /> */}
                    {/* Portals Route - redirecting to dashboard */}
                    {portals.map((r, index) => {
                        return <Route exact path={r} key={index} element={<Navigate to='dashboard/' />} />
                    })}

                    {/* Student */}
                    <Route path="/student/dashboard" element={<Dashboard />} />

                    {/* Teacher */}
                    {/* <Route path="/teacher/dashboard" element={<TeacherDashboard />} /> */}

                    {/* Parent */}
                    {/* <Route path="/parent/dashboard" element={<ParentDashboard />} /> */}

                    {/* Management */}
                    {/* <Route path="/management/dashboard" element={<ManagementDashboard />} /> */}

                    {/* Admin */}
                    {/* <Route path="/admin/dashboard" element={<AdminDashboard />} /> */}
                </Routes>
            </BrowserRouter>
        </div>
    );
};

export default App;