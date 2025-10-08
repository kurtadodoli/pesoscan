import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../components/Logo';
import { useDarkModeClasses } from '../hooks/useDarkModeClasses';
import './HomePage.css';

const HomePage = () => {
  const { getPageClasses } = useDarkModeClasses();
  
  return (
    <div className={getPageClasses("home-page")}>
      <section className="hero-section">
        <div className="container">
          <div className="hero-content">
            <div className="hero-logo-wrapper">
              <Logo size="xl" animated={false} />
            </div>
            <h1 className="hero-title">
              <span className="title-main">PesoScan</span>
              <div className="title-accent"></div>
            </h1>
            <p className="hero-subtitle">Advanced Counterfeit Detection System</p>
            <p className="hero-description">
              Secure your transactions with AI-powered peso bill authentication.
              <br/>
              Precision-trained YOLOv8 model with 94.0% accuracy detecting 41+ security features.
            </p>
            
            <div className="action-buttons">
              <Link to="/scan" className="btn btn-primary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                  <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
                </svg>
                Start Scanning
              </Link>
              
              <Link to="/scan?mode=upload" className="btn btn-outline">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" strokeWidth="2"/>
                  <polyline points="7,10 12,15 17,10" stroke="currentColor" strokeWidth="2"/>
                  <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" strokeWidth="2"/>
                </svg>
                Upload Image
              </Link>
            </div>

            <div className="metrics">
              <div className="metric">
                <span className="metric-value">94.0%</span>
                <span className="metric-label">Accuracy</span>
              </div>
              <div className="metric">
                <span className="metric-value">41+</span>
                <span className="metric-label">Features</span>
              </div>
              <div className="metric">
                <span className="metric-value">&lt;2s</span>
                <span className="metric-label">Processing</span>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Key Features</h2>
            <p className="section-subtitle">
              Professional-grade counterfeit detection powered by advanced AI
            </p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
                  <path d="m21 21-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <h3>Multi-Feature Detection</h3>
              <p>Simultaneously analyzes 41+ security features with precision-trained YOLOv8 model achieving 94.0% accuracy.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" strokeWidth="2" fill="none"/>
                  <path d="m9 12 2 2 4-4" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <h3>Authenticity Verification</h3>
              <p>Advanced algorithms provide comprehensive authenticity scoring with detailed risk assessment and actionable recommendations.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="currentColor" strokeWidth="2" fill="none"/>
                </svg>
              </div>
              <h3>Instant Results</h3>
              <p>Optimized neural networks deliver comprehensive analysis in under 2 seconds with real-time visual feedback.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                  <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
                </svg>
              </div>
              <h3>Flexible Input</h3>
              <p>Live camera scanning or upload existing images. Multiple formats supported with drag-and-drop convenience.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="advanced-features-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Advanced Features</h2>
            <p className="section-subtitle">
              Professional tools for comprehensive bill authentication
            </p>
          </div>
          
          <div className="advanced-features-grid">
            <div className="advanced-feature-card">
              <div className="advanced-feature-icon ar">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 12l2 2 4-4" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 6v6l4 2" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <h3>AR Overlays</h3>
              <p>Interactive augmented reality overlays highlight security features in real-time during camera scanning.</p>
              <div className="feature-status new">NEW</div>
            </div>

            <div className="advanced-feature-card">
              <div className="advanced-feature-icon uv">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="2"/>
                  <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" strokeWidth="2"/>
                  <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" strokeWidth="2"/>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" strokeWidth="2"/>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" strokeWidth="2"/>
                  <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" strokeWidth="2"/>
                  <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <h3>UV Detection Simulation</h3>
              <p>Advanced AI simulates ultraviolet light detection to identify UV-reactive security features on peso bills.</p>
              <div className="feature-status beta">BETA</div>
            </div>

            <div className="advanced-feature-card">
              <div className="advanced-feature-icon bsp">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                  <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
                  <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" strokeWidth="2"/>
                  <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" strokeWidth="2"/>
                  <polyline points="10,9 9,9 8,9" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <h3>BSP Reporting</h3>
              <p>Generate official reports compatible with Bangko Sentral ng Pilipinas standards, including contact information.</p>
              <div className="feature-status official">OFFICIAL</div>
            </div>

            <div className="advanced-feature-card">
              <div className="advanced-feature-icon magnifier">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
                  <path d="m21 21-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
                  <line x1="11" y1="8" x2="11" y2="14" stroke="currentColor" strokeWidth="2"/>
                  <line x1="8" y1="11" x2="14" y2="11" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <h3>Bill Magnifier</h3>
              <p>High-resolution magnification tool with security feature guide to examine peso bills in precise detail.</p>
              <div className="feature-status new">NEW</div>
            </div>
          </div>
        </div>
      </section>
      
      <section className="performance-section">
        <div className="container">
          <div className="performance-grid">
            <div className="performance-item">
              <div className="performance-number">94.0%</div>
              <div className="performance-label">Model Accuracy</div>
            </div>
            <div className="performance-item">
              <div className="performance-number">41+</div>
              <div className="performance-label">Security Features</div>
            </div>
            <div className="performance-item">
              <div className="performance-number">&lt;2s</div>
              <div className="performance-label">Processing Time</div>
            </div>
            <div className="performance-item">
              <div className="performance-number">100%</div>
              <div className="performance-label">Secure & Private</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;