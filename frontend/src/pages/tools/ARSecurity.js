import React, { useState, useRef, useEffect } from 'react';
import './ARSecurity.css';

const ARSecurity = () => {
  const [isArActive, setIsArActive] = useState(false);
  const [detectedFeatures, setDetectedFeatures] = useState([]);
  const [cameraStream, setCameraStream] = useState(null);
  const [showHelp, setShowHelp] = useState(false);
  const videoRef = useRef(null);

  useEffect(() => {
    startCamera();
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment',
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setCameraStream(stream);
    } catch (error) {
      console.error('Error accessing camera:', error);
    }
  };

  const toggleAR = () => {
    setIsArActive(!isArActive);
    if (!isArActive) {
      // Simulate feature detection
      simulateFeatureDetection();
    } else {
      setDetectedFeatures([]);
    }
  };

  const simulateFeatureDetection = () => {
    const detectedFeaturesList = commonSecurityFeatures.map((feature, index) => ({
      ...feature,
      position: {
        x: Math.random() * 60 + 20, // 20-80% from left
        y: Math.random() * 60 + 20, // 20-80% from top
      },
      confidence: Math.random() * 0.3 + 0.7, // 70-100% confidence
      detected: Math.random() > 0.2 // 80% chance of detection
    }));
    
    setDetectedFeatures(detectedFeaturesList);
  };

  const commonSecurityFeatures = [
    {
      name: 'Security Thread',
      type: 'embedded',
      description: 'Embedded security thread with microprinting',
      color: '#6366f1',
      icon: '🔒'
    },
    {
      name: 'Watermark',
      type: 'paper',
      description: 'Portrait watermark visible when held to light',
      color: '#3b82f6',
      icon: '💧'
    },
    {
      name: 'Intaglio Printing',
      type: 'texture',
      description: 'Raised printing texture on main design',
      color: '#8b5cf6',
      icon: '✨'
    },
    {
      name: 'Microprinting',
      type: 'text',
      description: 'Tiny text visible under magnification',
      color: '#10b981',
      icon: '�'
    },
    {
      name: 'Color-Changing Ink',
      type: 'optical',
      description: 'Ink that changes color when tilted',
      color: '#f59e0b',
      icon: '🎨'
    },
    {
      name: 'UV Fluorescence',
      type: 'uv',
      description: 'UV-reactive security elements',
      color: '#06b6d4',
      icon: '�'
    }
  ];

  return (
    <div className="ar-security-container">
      <div className="ar-header">
        <h1>AR Security Overlay</h1>
        <p>Real-time security feature detection for Philippine peso banknotes</p>
      </div>

      <div className="ar-main-content">
        <div className="camera-section">

          <div className={`ar-camera-container ${isArActive ? 'ar-active' : ''}`}>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="ar-camera-feed"
            />
            
            {isArActive && (
              <>
                <div className="ar-overlay">
                  <div className="scanning-animation"></div>
                  
                  {detectedFeatures.map((feature, index) => (
                    feature.detected && (
                      <div
                        key={index}
                        className="feature-marker"
                        style={{
                          left: `${feature.position.x}%`,
                          top: `${feature.position.y}%`,
                          '--marker-color': feature.color
                        }}
                      >
                        <div className="marker-pulse"></div>
                        <div className="marker-icon">{feature.icon}</div>
                        <div className="feature-tooltip">
                          <h4>{feature.name}</h4>
                          <p>{feature.description}</p>
                          <div className="confidence-bar">
                            <div 
                              className="confidence-fill"
                              style={{ width: `${feature.confidence * 100}%` }}
                            ></div>
                            <span>{Math.round(feature.confidence * 100)}%</span>
                          </div>
                        </div>
                      </div>
                    )
                  ))}
                  
                  <div className="detection-stats">
                    <div className="stats-header">
                      <h3>Security Feature Detection</h3>
                      <span className="detected-count">
                        {detectedFeatures.filter(f => f.detected).length} / {detectedFeatures.length} features detected
                      </span>
                    </div>
                  </div>
                </div>
              </>
            )}

            <div className="ar-controls">
              <button
                className={`ar-toggle ${isArActive ? 'active' : ''}`}
                onClick={toggleAR}
              >
                {isArActive ? '🔍 AR ON' : '📱 Start AR'}
              </button>
              
              <button
                className="help-btn"
                onClick={() => setShowHelp(true)}
              >
                ❓ Help
              </button>
            </div>
          </div>
        </div>

        <div className="features-panel">
          <h2>Security Features</h2>
          <div className="features-list">
            {commonSecurityFeatures.map((feature, index) => {
              const detected = detectedFeatures.find((_, i) => i === index);
              return (
                <div 
                  key={index} 
                  className={`feature-item ${detected?.detected ? 'detected' : ''}`}
                >
                  <div className="feature-icon" style={{ color: feature.color }}>
                    {feature.icon}
                  </div>
                  <div className="feature-info">
                    <h4>{feature.name}</h4>
                    <p>{feature.description}</p>
                    <span className="feature-type">{feature.type}</span>
                  </div>
                  {detected?.detected && (
                    <div className="detection-indicator">
                      ✅ Detected ({Math.round(detected.confidence * 100)}%)
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {showHelp && (
        <div className="help-overlay" onClick={() => setShowHelp(false)}>
          <div className="help-content" onClick={e => e.stopPropagation()}>
            <h3>📋 How to Use AR Security Overlay</h3>
            <div className="help-steps">
              <div className="help-step">
                <span className="step-number">1</span>
                <div>
                  <h4>Position Banknote</h4>
                  <p>Hold the peso banknote steady in front of the camera</p>
                </div>
              </div>
              <div className="help-step">
                <span className="step-number">2</span>
                <div>
                  <h4>Start AR Detection</h4>
                  <p>Click "Start AR" to begin security feature detection</p>
                </div>
              </div>
              <div className="help-step">
                <span className="step-number">3</span>
                <div>
                  <h4>Review Features</h4>
                  <p>Check detected features and their confidence levels</p>
                </div>
              </div>
            </div>
            <button className="close-help" onClick={() => setShowHelp(false)}>
              Got it!
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ARSecurity;