import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../components/Logo';
import { useDarkModeClasses } from '../hooks/useDarkModeClasses';
import './AboutPage.css';

const AboutPage = () => {
  const { getPageClasses } = useDarkModeClasses();
  
  return (
    <div className={getPageClasses("about-page")}>
      <div className="container">
        <div className="about-header">
          <Logo size="large" />
          <h1>About PesoScan</h1>
          <p className="about-subtitle">
            Advanced AI-powered counterfeit detection for Philippine peso bills
          </p>
        </div>

        <div className="about-content">
          <section className="about-section">
            <h2>What is PesoScan?</h2>
            <p>
              PesoScan is a cutting-edge web-based platform designed to detect counterfeit Philippine peso bills 
              using state-of-the-art artificial intelligence technology. Our system combines YOLOv8 object detection 
              with Convolutional Neural Networks (CNNs) to provide fast, accurate, and reliable currency authentication.
            </p>
            <p>
              Developed as a thesis project, PesoScan aims to contribute to the fight against currency counterfeiting 
              by making advanced detection technology accessible to businesses, financial institutions, and individuals.
            </p>
          </section>

          <section className="about-section">
            <h2>How It Works</h2>
            <div className="workflow-steps">
              <div className="workflow-step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4>Image Capture/Upload</h4>
                  <p>Users capture a photo using their device camera or upload an existing image of a peso bill.</p>
                </div>
              </div>
              
              <div className="workflow-step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4>Object Detection</h4>
                  <p>YOLOv8 model detects and localizes the peso bill within the image frame for precise analysis.</p>
                </div>
              </div>
              
              <div className="workflow-step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4>Feature Analysis</h4>
                  <p>CNN classifier analyzes security features including watermarks, security threads, and microprinting.</p>
                </div>
              </div>
              
              <div className="workflow-step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h4>Result Generation</h4>
                  <p>System provides authenticity classification with confidence score and detailed analysis.</p>
                </div>
              </div>
            </div>
          </section>

          <section className="about-section">
            <h2>Technology Stack</h2>
            <div className="tech-grid">
              <div className="tech-category">
                <h4>Frontend</h4>
                <ul>
                  <li>ReactJS</li>
                  <li>CSS3 with custom design system</li>
                  <li>WebRTC for camera access</li>
                  <li>Axios for API communication</li>
                </ul>
              </div>
              
              <div className="tech-category">
                <h4>Backend</h4>
                <ul>
                  <li>Python FastAPI</li>
                  <li>OpenCV for image processing</li>
                  <li>RESTful API architecture</li>
                  <li>Swagger documentation</li>
                </ul>
              </div>
              
              <div className="tech-category">
                <h4>AI/ML</h4>
                <ul>
                  <li>YOLOv8 (Ultralytics)</li>
                  <li>Custom CNN model</li>
                  <li>TensorFlow/PyTorch</li>
                  <li>Computer vision algorithms</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="about-section">
            <h2>Key Features</h2>
            <div className="features-list">
              <div className="feature-item">
                <div className="feature-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
                  </svg>
                </div>
                <div>
                  <h5>Real-time Camera Scanning</h5>
                  <p>Live capture and analysis using device camera with instant feedback.</p>
                </div>
              </div>
              
              <div className="feature-item">
                <div className="feature-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <path d="M21 21l-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
                  </svg>
                </div>
                <div>
                  <h5>Advanced AI Detection</h5>
                  <p>State-of-the-art object detection and classification algorithms.</p>
                </div>
              </div>
              
              <div className="feature-item">
                <div className="feature-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <polyline points="22,12 18,12 15,21 9,3 6,12 2,12" stroke="currentColor" strokeWidth="2" fill="none"/>
                  </svg>
                </div>
                <div>
                  <h5>Confidence Scoring</h5>
                  <p>Detailed confidence percentages for transparency and reliability.</p>
                </div>
              </div>
              
              <div className="feature-item">
                <div className="feature-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                  </svg>
                </div>
                <div>
                  <h5>Security Feature Analysis</h5>
                  <p>Detailed examination of watermarks, threads, and other security elements.</p>
                </div>
              </div>
              
              <div className="feature-item">
                <div className="feature-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" strokeWidth="2"/>
                    <line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" strokeWidth="2"/>
                  </svg>
                </div>
                <div>
                  <h5>Responsive Design</h5>
                  <p>Works seamlessly across desktop, tablet, and mobile devices.</p>
                </div>
              </div>
              
              <div className="feature-item">
                <div className="feature-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                  </svg>
                </div>
                <div>
                  <h5>Scan History</h5>
                  <p>Track and manage previous scans with detailed records and statistics.</p>
                </div>
              </div>
            </div>
          </section>

          <section className="about-section">
            <h2>Frequently Asked Questions</h2>
            <div className="faq-list">
              <div className="faq-item">
                <h5>How accurate is PesoScan?</h5>
                <p>
                  Our AI model achieves over 99% accuracy in laboratory testing. However, accuracy may vary 
                  based on image quality, lighting conditions, and bill condition. Always verify suspicious 
                  bills through official channels for important transactions.
                </p>
              </div>
              
              <div className="faq-item">
                <h5>What peso denominations are supported?</h5>
                <p>
                  PesoScan currently supports all current Philippine peso denominations: ₱20, ₱50, ₱100, 
                  ₱200, ₱500, and ₱1000 bills. The system is trained on the latest polymer and enhanced 
                  security features.
                </p>
              </div>
              
              <div className="faq-item">
                <h5>Is my data stored or shared?</h5>
                <p>
                  For the demo version, scan history is stored locally in your browser. In production, 
                  we follow strict privacy policies and do not share personal data. Images are processed 
                  temporarily and not permanently stored on our servers.
                </p>
              </div>
              
              <div className="faq-item">
                <h5>Can I use this for business purposes?</h5>
                <p>
                  This is currently a research prototype for educational purposes. For commercial 
                  applications, please contact us for licensing and integration options with additional 
                  security and compliance features.
                </p>
              </div>
              
              <div className="faq-item">
                <h5>What should I do if I find a counterfeit bill?</h5>
                <p>
                  If PesoScan detects a potentially counterfeit bill, do not pass it on. Contact your local 
                  bank, the Bangko Sentral ng Pilipinas (BSP), or law enforcement. Remember that this 
                  system is a detection aid, not a definitive authentication method.
                </p>
              </div>
            </div>
          </section>

          <section className="about-section disclaimer-section">
            <h2>Important Disclaimer</h2>
            <div className="disclaimer-box">
              <p>
                <strong>Educational and Research Use Only:</strong> PesoScan is developed as a thesis project 
                for educational and research purposes. While our AI model strives for high accuracy, it should 
                not be used as the sole method for currency authentication in critical financial decisions.
              </p>
              <p>
                <strong>Professional Verification Required:</strong> Always verify suspicious bills through 
                official banking channels, trained professionals, or the Bangko Sentral ng Pilipinas (BSP) 
                for important transactions. This system serves as a detection aid and should complement, 
                not replace, traditional authentication methods.
              </p>
              <p>
                <strong>No Liability:</strong> The developers assume no responsibility for financial losses 
                or decisions made based solely on PesoScan results. Users acknowledge that this is an 
                experimental technology and should exercise appropriate caution.
              </p>
            </div>
          </section>

          <div className="about-actions">
            <Link to="/scan" className="btn btn-primary btn-large">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
              </svg>
              Try PesoScan Now
            </Link>
            
            <Link to="/" className="btn btn-outline">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                <polyline points="9,22 9,12 15,12 15,22" stroke="currentColor" strokeWidth="2" fill="none"/>
              </svg>
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;