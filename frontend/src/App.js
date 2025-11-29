import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/globals.css';
import './styles/dark-mode-sync.css';
import './styles/dark-mode.css';
import { DarkModeProvider } from './contexts/DarkModeContext';

// Import pages
import HomePage from './pages/HomePage';
import ScanPage from './pages/ScanPage';
import ResultsPage from './pages/ResultsPage';
import HistoryPage from './pages/HistoryPage';
import AboutPage from './pages/AboutPage';
import TestResults from './pages/TestResults';

// Import tool pages
import UVLight from './pages/tools/UVLight';
import ARSecurity from './pages/tools/ARSecurity';
import DigitalMagnifier from './pages/tools/DigitalMagnifier';

// Import components
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import StandaloneResultsDemo from './components/StandaloneResultsDemo';

function App() {
  return (
    <DarkModeProvider>
      <Router>
        <div className="App">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/scan" element={<ScanPage />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/test-results" element={<TestResults />} />
              <Route path="/demo-results" element={<StandaloneResultsDemo />} />
              
              {/* Tool routes */}
              <Route path="/tools/uv-light" element={<UVLight />} />
              <Route path="/tools/ar-security" element={<ARSecurity />} />
              <Route path="/tools/digital-magnifier" element={<DigitalMagnifier />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </DarkModeProvider>
  );
}

export default App;