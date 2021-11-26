import { BrowserRouter, Routes, Route } from 'react-router-dom';

import LoginForm from './routes/login';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route exact path="/login" element={<LoginForm />}></Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;