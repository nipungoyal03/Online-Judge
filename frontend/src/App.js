import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProblemList from './components/ProblemList';
import ProblemDetail from './components/ProblemDetail';
import NotFound from './components/NotFound';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<LoginForm />} />
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/problems" element={<ProblemList />} />
        <Route path="/problem/:code" element={<ProblemDetail />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
