import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Logo from '../components/Logo';
import './AboutPage.css';

const AboutPage = () => {
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'technology', label: 'Technology Stack' },
    { id: 'features', label: 'Key Features' },
    { id: 'denominations', label: 'Denominations' },
    { id: 'team', label: 'Development Team' }
  ];

  return (
    <div className="about-page">
      <div className="container">
        <div className="about-header">
          <Logo size="large" />
          <h1>About PesoScan</h1>
          <p className="about-subtitle">
            A Computer Vision-Based Counterfeit Detection, Denomination Classification, and Damage Assessment System for Philippine Banknotes and Coins Using Transfer Learning with a Hybrid of ResNet-50 and MobileNetV3, Integrated with YOLOv8
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="about-tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="about-content">
          
          {/* Overview & FAQ Tab */}
          {activeTab === 'overview' && (
            <div className="tab-content">
              <section className="about-section">
                <h2>What is PesoScan?</h2>
                <p>
                  This study develops an intelligent computer vision system that detects counterfeit Philippine 
                  banknotes and coins, identifies denominations, and assesses their damage/condition using YOLOv8 
                  and Custom Convolutional Neural Networks (CNN). It enables accurate authentication with reporting 
                  to the Bangko Sentral ng Pilipinas (BSP), enhancing financial security through a fast and reliable 
                  deep learning–based solution.
                </p>
              </section>

              <section className="about-section">
                <h2>How It Works</h2>
                <div className="workflow-steps">
                  <div className="workflow-step">
                    <div className="step-number">1</div>
                    <div className="step-content">
                      <h4>Image Capture/Upload</h4>
                      <p>Users capture a photo using their device camera or upload an existing image of a peso banknote.</p>
                    </div>
                  </div>
                  
                  <div className="workflow-step">
                    <div className="step-number">2</div>
                    <div className="step-content">
                      <h4>Object Detection</h4>
                      <p>YOLOv8 model detects and localizes the peso banknote within the image frame for precise analysis.</p>
                    </div>
                  </div>
                  
                  <div className="workflow-step">
                    <div className="step-number">3</div>
                    <div className="step-content">
                      <h4>Feature Analysis & Classification</h4>
                      <p>Hybrid ResNet-50 and MobileNetV3 models analyze security features including watermarks, security threads, and microprinting for denomination classification and authenticity verification.</p>
                    </div>
                  </div>
                  
                  <div className="workflow-step">
                    <div className="step-number">4</div>
                    <div className="step-content">
                      <h4>Result Generation</h4>
                      <p>System provides authenticity classification with confidence score and detailed analysis using transfer learning techniques.</p>
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
                      Our hybrid model utilizing ResNet-50 and MobileNetV3 with transfer learning achieves over 99% 
                      accuracy in laboratory testing. The YOLOv8 object detection combined with deep learning 
                      classification provides robust performance. However, accuracy may vary based on image quality, 
                      lighting conditions, and banknote condition. Always verify suspicious banknotes through official 
                      channels for important transactions.
                    </p>
                  </div>
                  
                  <div className="faq-item">
                    <h5>What technology powers PesoScan?</h5>
                    <p>
                      PesoScan uses a state-of-the-art computer vision pipeline combining YOLOv8 for real-time 
                      object detection and a hybrid architecture of ResNet-50 and MobileNetV3 for classification. 
                      These models are fine-tuned using transfer learning on Philippine banknote datasets, enabling 
                      accurate denomination identification and counterfeit detection.
                    </p>
                  </div>
                  
                  <div className="faq-item">
                    <h5>What peso denominations are supported?</h5>
                    <p>
                      PesoScan currently supports all current Philippine peso denominations: ₱20, ₱50, ₱100, 
                      ₱200, ₱500, and ₱1000 banknotes. The system is trained on the latest polymer and enhanced 
                      security features, with models capable of detecting 41 distinct security features.
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
                    <h5>What should I do if I find a counterfeit banknote?</h5>
                    <p>
                      If PesoScan detects a potentially counterfeit banknote, do not pass it on. Contact your local 
                      bank, the Bangko Sentral ng Pilipinas (BSP), or law enforcement. Remember that this 
                      system is a detection aid, not a definitive authentication method.
                    </p>
                  </div>
                </div>
              </section>
            </div>
          )}

          {/* Technology Stack Tab */}
          {activeTab === 'technology' && (
            <div className="tab-content">
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
                      <li>React Router for navigation</li>
                    </ul>
                  </div>
                  
                  <div className="tech-category">
                    <h4>Backend</h4>
                    <ul>
                      <li>Python FastAPI</li>
                      <li>OpenCV for image processing</li>
                      <li>RESTful API architecture</li>
                      <li>Swagger documentation</li>
                      <li>Uvicorn ASGI server</li>
                    </ul>
                  </div>
                  
                  <div className="tech-category">
                    <h4>Machine Learning</h4>
                    <ul>
                      <li>YOLOv8 (Ultralytics)</li>
                      <li>ResNet-50 & MobileNetV3</li>
                      <li>Transfer Learning</li>
                      <li>PyTorch Framework</li>
                      <li>Computer vision algorithms</li>
                    </ul>
                  </div>
                </div>

                <div className="tech-details">
                  <h3>Architecture Overview</h3>
                  <div className="architecture-grid">
                    <div className="architecture-item">
                      <h5>🔍 Object Detection Layer</h5>
                      <p>YOLOv8 performs real-time detection and localization of Philippine banknotes in images with high precision.</p>
                    </div>
                    <div className="architecture-item">
                      <h5>🧠 Classification Layer</h5>
                      <p>Hybrid ResNet-50 and MobileNetV3 architecture for denomination classification and feature extraction.</p>
                    </div>
                    <div className="architecture-item">
                      <h5>🔐 Security Analysis</h5>
                      <p>Deep learning models trained on 41 security features including watermarks, threads, and microprinting.</p>
                    </div>
                    <div className="architecture-item">
                      <h5>📊 Confidence Scoring</h5>
                      <p>Multi-model ensemble approach provides reliability scores for counterfeit detection decisions.</p>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          )}

          {/* Key Features Tab */}
          {activeTab === 'features' && (
            <div className="tab-content">
              <section className="about-section">
                <h2>Key Features</h2>
                <p className="features-subtitle">Professional-grade counterfeit detection powered by advanced computer vision</p>
                
                <div className="features-modern-grid">
                  <div className="modern-feature-card">
                    <div className="modern-feature-icon">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <path d="M21 21l-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </div>
                    <h3>Multi-Feature Detection</h3>
                    <p>Simultaneously analyzes multiple security features with precision-trained YOLOv8 model for comprehensive authenticity verification.</p>
                  </div>

                  <div className="modern-feature-card">
                    <div className="modern-feature-icon">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="3" y="11" width="18" height="10" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2" fill="none"/>
                      </svg>
                    </div>
                    <h3>Authenticity Verification</h3>
                    <p>Advanced algorithms provide comprehensive authenticity scoring with detailed risk assessment and actionable recommendations.</p>
                  </div>

                  <div className="modern-feature-card">
                    <div className="modern-feature-icon">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <polyline points="12,6 12,12 16,14" stroke="currentColor" strokeWidth="2" fill="none"/>
                      </svg>
                    </div>
                    <h3>Instant Results</h3>
                    <p>Optimized neural networks deliver comprehensive analysis in under 2 seconds with real-time visual feedback.</p>
                  </div>

                  <div className="modern-feature-card">
                    <div className="modern-feature-icon">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
                      </svg>
                    </div>
                    <h3>Flexible Input</h3>
                    <p>Live camera scanning or upload existing images. Multiple formats supported with drag-and-drop convenience.</p>
                  </div>
                </div>
              </section>
            </div>
          )}

          {/* Denominations Tab */}
          {activeTab === 'denominations' && (
            <div className="tab-content">
              <section className="about-section">
                <h2>Supported Philippine Banknote Denominations</h2>
                <p className="denominations-intro">
                  PesoScan is trained to detect and authenticate all current Philippine peso banknotes, 
                  including both paper and polymer versions with the latest security features.
                </p>

                <div className="denominations-grid">
                  <div className="denomination-card-detail">
                    <div className="denomination-image">
                      <img src="/banknotes/20_Paper.jpg" alt="20 Peso Banknote" />
                    </div>
                    <div className="denomination-info">
                      <h3>₱20 Peso</h3>
                      <p className="denomination-color" style={{color: '#ff6b35'}}>Orange</p>
                      <ul>
                        <li><strong>Front:</strong> Manuel L. Quezon</li>
                        <li><strong>Back:</strong> Malacañan Palace</li>
                        <li><strong>Features:</strong> Watermark, security thread, see-through mark</li>
                      </ul>
                    </div>
                  </div>

                  <div className="denomination-card-detail">
                    <div className="denomination-image">
                      <img src="/banknotes/50_Polymer.png" alt="50 Peso Banknote" />
                    </div>
                    <div className="denomination-info">
                      <h3>₱50 Peso</h3>
                      <p className="denomination-color" style={{color: '#e63946'}}>Red</p>
                      <ul>
                        <li><strong>Front:</strong> Sergio Osmeña</li>
                        <li><strong>Back:</strong> Taal Lake</li>
                        <li><strong>Features:</strong> Enhanced security features, polymer substrate</li>
                      </ul>
                    </div>
                  </div>

                  <div className="denomination-card-detail">
                    <div className="denomination-image">
                      <img src="/banknotes/100_Paper.jpg" alt="100 Peso Banknote" />
                    </div>
                    <div className="denomination-info">
                      <h3>₱100 Peso</h3>
                      <p className="denomination-color" style={{color: '#9d4edd'}}>Violet</p>
                      <ul>
                        <li><strong>Front:</strong> Manuel Roxas</li>
                        <li><strong>Back:</strong> Mayon Volcano</li>
                        <li><strong>Features:</strong> Optically variable device, enhanced security thread</li>
                      </ul>
                    </div>
                  </div>

                  <div className="denomination-card-detail">
                    <div className="denomination-image">
                      <img src="/banknotes/200_Paper.jpg" alt="200 Peso Banknote" />
                    </div>
                    <div className="denomination-info">
                      <h3>₱200 Peso</h3>
                      <p className="denomination-color" style={{color: '#06a77d'}}>Green</p>
                      <ul>
                        <li><strong>Front:</strong> Diosdado Macapagal</li>
                        <li><strong>Back:</strong> Bohol Chocolate Hills</li>
                        <li><strong>Features:</strong> Color-shifting ink, microprinting</li>
                      </ul>
                    </div>
                  </div>

                  <div className="denomination-card-detail">
                    <div className="denomination-image">
                      <img src="/banknotes/500_Paper.jpg" alt="500 Peso Banknote" />
                    </div>
                    <div className="denomination-info">
                      <h3>₱500 Peso</h3>
                      <p className="denomination-color" style={{color: '#ffd23f'}}>Yellow</p>
                      <ul>
                        <li><strong>Front:</strong> Benigno Aquino Jr. & Corazon Aquino</li>
                        <li><strong>Back:</strong> Philippine Eagle</li>
                        <li><strong>Features:</strong> Advanced security features, embossed printing</li>
                      </ul>
                    </div>
                  </div>

                  <div className="denomination-card-detail">
                    <div className="denomination-image">
                      <img src="/banknotes/1000_Paper.png" alt="1000 Peso Banknote" />
                    </div>
                    <div className="denomination-info">
                      <h3>₱1000 Peso</h3>
                      <p className="denomination-color" style={{color: '#0077b6'}}>Blue</p>
                      <ul>
                        <li><strong>Front:</strong> José Abad Santos, Vicente Lim, Josefa Llanes Escoda</li>
                        <li><strong>Back:</strong> Tubbataha Reefs</li>
                        <li><strong>Features:</strong> Most advanced security features, multiple verification methods</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div className="security-features-note">
                  <h3>🔐 Security Features We Detect</h3>
                  <div className="security-grid">
                    <div className="security-item">✓ Watermarks</div>
                    <div className="security-item">✓ Security Threads</div>
                    <div className="security-item">✓ Microprinting</div>
                    <div className="security-item">✓ Color-Shifting Ink</div>
                    <div className="security-item">✓ See-Through Marks</div>
                    <div className="security-item">✓ Optically Variable Devices</div>
                    <div className="security-item">✓ Serial Numbers</div>
                    <div className="security-item">✓ Embossed Features</div>
                  </div>
                </div>
              </section>
            </div>
          )}

          {/* Development Team Tab */}
          {activeTab === 'team' && (
            <div className="tab-content">
              <section className="about-section">
                <h2>Development Team</h2>
                <p className="team-intro">
                  PesoScan is developed by Computer Science students from the Technological Institute of the Philippines,
                  combining expertise in artificial intelligence, software development, and computer vision.
                </p>
                <div className="team-grid">
                  <div className="team-member">
                    <div className="member-icon">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <path d="M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </div>
                    <h4>Kurt Andre P. Adodoli</h4>
                    <p className="member-role">Lead Programmer</p>
                    <p className="member-institution">Technological Institute of the Philippines</p>
                  </div>
                  
                  <div className="team-member">
                    <div className="member-icon">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <path d="M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </div>
                    <h4>Cedric Kent C. Centeno</h4>
                    <p className="member-role">Assistant Lead Programmer</p>
                    <p className="member-institution">Technological Institute of the Philippines</p>
                  </div>
                  
                  <div className="team-member">
                    <div className="member-icon">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <path d="M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </div>
                    <h4>Josh Russel P. Magpantay</h4>
                    <p className="member-role">Backend Developer</p>
                    <p className="member-institution">Technological Institute of the Philippines</p>
                  </div>
                  
                  <div className="team-member">
                    <div className="member-icon">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <path d="M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </div>
                    <h4>John Kenneth S. Marzan</h4>
                    <p className="member-role">Frontend Developer</p>
                    <p className="member-institution">Technological Institute of the Philippines</p>
                  </div>
                </div>

                <div className="academic-info">
                  <h3>Academic Information</h3>
                  <div className="academic-details">
                    <div className="academic-card">
                      <span className="academic-label">Institution</span>
                      <span className="academic-value">Technological Institute of the Philippines - Quezon City</span>
                    </div>
                    <div className="academic-card">
                      <span className="academic-label">Program</span>
                      <span className="academic-value">Bachelor of Science in Computer Science</span>
                    </div>
                    <div className="academic-card">
                      <span className="academic-label">Project Type</span>
                      <span className="academic-value">Thesis Project</span>
                    </div>
                    <div className="academic-card">
                      <span className="academic-label">Academic Year</span>
                      <span className="academic-value">2025-2026</span>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          )}

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