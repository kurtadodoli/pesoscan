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
          
          <div className="navbar-right">
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
                    <svg className="tool-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="2"/>
                      <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                    <span className="tool-label">UV Light</span>
                  </Link>
                  <Link 
                    to="/tools/ar-security" 
                    className="dropdown-item"
                    onClick={closeTools}
                  >
                    <svg className="tool-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
                      <line x1="21" y1="21" x2="16.65" y2="16.65" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <path d="M11 8v3l2 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                    <span className="tool-label">AR Security Overlay</span>
                  </Link>
                  <Link 
                    to="/tools/magnifier" 
                    className="dropdown-item"
                    onClick={closeTools}
                  >
                    <svg className="tool-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
                      <line x1="21" y1="21" x2="16.65" y2="16.65" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="11" y1="8" x2="11" y2="14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <line x1="8" y1="11" x2="14" y2="11" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                    <span className="tool-label">Digital Magnifier</span>
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
          </ul>
          <DarkModeToggle />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;