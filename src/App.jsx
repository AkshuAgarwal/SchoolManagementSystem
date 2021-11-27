import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Login from './routes/login';
import Dashboard from './routes/student/dashboard';


const portals = ['/student', '/teacher', '/parent', '/management', '/admin'];

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Routes>
                    <Route exact path='/' element={<Navigate to='/login' />} />

                    {/* Login Route */}
                    <Route exact path="/login" element={<Login />}></Route>

                    {/* Portals Route - redirecting to dashboard */}
                    {portals.map((r, index) => {
                        return <Route exact path={r} key={index} element={<Navigate to='dashboard/' />}></Route>
                    })}

                    {/* Student */}
                    <Route path="/student/dashboard" element={<Dashboard />}></Route>

                    {/* Teacher */}
                    {/* <Route path="/teacher/dashboard" element={<TeacherDashboard />}></Route> */}

                    {/* Parent */}
                    {/* <Route path="/parent/dashboard" element={<ParentDashboard />}></Route> */}

                    {/* Management */}
                    {/* <Route path="/management/dashboard" element={<ManagementDashboard />}></Route> */}

                    {/* Admin */}
                    {/* <Route path="/admin/dashboard" element={<AdminDashboard />}></Route> */}
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;