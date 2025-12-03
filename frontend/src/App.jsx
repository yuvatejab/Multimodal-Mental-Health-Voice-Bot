import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import CopingStrategiesPage from './pages/CopingStrategiesPage';
import TherapistFinderPage from './pages/TherapistFinderPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/coping-strategies" element={<CopingStrategiesPage />} />
        <Route path="/find-therapist" element={<TherapistFinderPage />} />
      </Routes>
    </Router>
  );
}

export default App;
