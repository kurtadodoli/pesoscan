import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Logo from './Logo';
import DarkModeToggle from './DarkModeToggle';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();
  const [isToolsOpen, setIsToolsOpen] = useState(false);

  const toggleTools = () => {
    setIsToolsOpen(!isToolsOpen);
  };

  const closeTools = () => {
    setIsToolsOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            <Logo size="small" animated={true} />
            <span className="brand-text">PesoScan</span>
          </Link>
          
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link 
                to="/" 
                className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
              >
                Home
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/scan" 
                className={`nav-link ${location.pathname === '/scan' ? 'active' : ''}`}
              >
                Scan
              </Link>
            </li>
            <li className="nav-item dropdown" onMouseLeave={closeTools}>
              <button 
                className={`nav-link dropdown-toggle ${
                  ['/tools/uv-light', '/tools/ar-security', '/tools/magnifier'].includes(location.pathname) ? 'active' : ''
                }`}
                onClick={toggleTools}
                onMouseEnter={() => setIsToolsOpen(true)}
              >
                Tools
                <span className="dropdown-arrow">▼</span>
              </button>
              {isToolsOpen && (
                <div className="dropdown-menu">
                  <Link 
                    to="/tools/uv-light" 
                    className="dropdown-item"
                    onClick={closeTools}
                  >
                    <span className="tool-icon">💡</span>
                    UV Light
                    <span className="tool-description">Detect UV-reactive features</span>
                  </Link>
                  <Link 
                    to="/tools/ar-security" 
                    className="dropdown-item"
                    onClick={closeTools}
                  >
                    <span className="tool-icon">🔍</span>
                    AR Security Overlay
                    <span className="tool-description">Identify security features</span>
                  </Link>
                  <Link 
                    to="/tools/magnifier" 
                    className="dropdown-item"
                    onClick={closeTools}
                  >
                    <span className="tool-icon">🔎</span>
                    Digital Magnifier
                    <span className="tool-description">Zoom in for detailed inspection</span>
                  </Link>
                </div>
              )}
            </li>
            <li className="nav-item">
              <Link 
                to="/history" 
                className={`nav-link ${location.pathname === '/history' ? 'active' : ''}`}
              >
                History
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/about" 
                className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}
              >
                About
              </Link>
            </li>
            <li className="nav-item">
              <DarkModeToggle />
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;