import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h4>PesoScan</h4>
            <p>PesoScan: A Computer Vision-Based Counterfeit Detection, Denomination Classification, and Damage Assessment System for Philippine Banknotes and Coins Using Transfer Learning with a Hybrid of ResNet-50 and MobileNetV3, Integrated with YOLOv8</p>
          </div>
          
          <div className="footer-section">
            <h5>Quick Links</h5>
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/scan">Scan Banknote</a></li>
              <li><a href="/about">About</a></li>
              <li><a href="/history">History</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h5>Technology</h5>
            <ul>
              <li>YOLOv8 Detection</li>
              <li>CNN Classification</li>
              <li>ReactJS Frontend</li>
              <li>Python Backend</li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h5>Disclaimer</h5>
            <p className="disclaimer">
              This system is for educational and research purposes. 
              Always verify currency authenticity through official banking channels.
            </p>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; 2025 PesoScan. Thesis Project - Educational Use Only.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;