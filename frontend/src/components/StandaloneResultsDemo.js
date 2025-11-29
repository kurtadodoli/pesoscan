import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../pages/ResultsPage.css';

const StandaloneResultsDemo = () => {
  const navigate = useNavigate();

  // Sample data that matches your reference image
  const sampleResult = {
    id: "demo_scan_001",
    result: {
      detections: [
        {
          class_name: "20",
          feature_name: "20 Peso Bill",
          confidence: 0.793,
          bbox: [0.15, 0.12, 0.45, 0.38]
        },
        {
          class_name: "1000", 
          feature_name: "1000 Peso Bill",
          confidence: 0.772,
          bbox: [0.50, 0.15, 0.85, 0.45]
        },
        {
          class_name: "50",
          feature_name: "50 Peso Bill", 
          confidence: 0.610,
          bbox: [0.25, 0.55, 0.75, 0.85]
        }
      ],
      authentic: true,
      confidence: 0.85,
      denomination: "Mixed Denominations",
      features: {
        security_thread: true,
        watermark: true,
        microprinting: false,
        color_changing_ink: true,
        uv_features: false,
        raised_printing: true
      }
    },
    peso_scan: {
      result: {
        detections: [
          {
            class_name: "20",
            feature_name: "20 Peso Bill",
            confidence: 0.793,
            bbox: [0.15, 0.12, 0.45, 0.38]
          },
          {
            class_name: "1000", 
            feature_name: "1000 Peso Bill",
            confidence: 0.772,
            bbox: [0.50, 0.15, 0.85, 0.45]
          },
          {
            class_name: "50",
            feature_name: "50 Peso Bill", 
            confidence: 0.610,
            bbox: [0.25, 0.55, 0.75, 0.85]
          }
        ]
      }
    },
    processing_time: 2.14,
    timestamp: "2025-10-04T03:30:00Z"
  };

  const sampleImageUrl = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250' viewBox='0 0 400 250'%3E%3Crect width='400' height='250' fill='%23f3f4f6'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%236b7280' font-family='Arial, sans-serif' font-size='18'%3ESample Philippine Peso Bill%3C/text%3E%3C/svg%3E";

  // Extract data for the interface
  const yoloDetections = sampleResult.peso_scan?.result?.detections || [];
  const isAuthentic = sampleResult.result?.authentic;
  const confidence = Math.round(sampleResult.result?.confidence || 0);
  const denomination = sampleResult.result?.denomination;
  const processingTime = sampleResult.processing_time?.toFixed(2);
  const features = sampleResult.result?.features || {};

  const getAuthenticatedFeaturesCount = () => {
    const featuresArray = [
      features.security_thread,
      features.watermark,
      features.microprinting,
      features.color_changing_ink,
      features.uv_features,
      features.raised_printing
    ];
    return featuresArray.filter(Boolean).length;
  };

  const getSecurityScore = () => {
    const authenticatedCount = getAuthenticatedFeaturesCount();
    return Math.round((authenticatedCount / 6) * 100);
  };

  const getSecurityScoreClass = () => {
    const score = getSecurityScore();
    if (score >= 80) return 'excellent';
    if (score >= 60) return 'good';
    if (score >= 40) return 'fair';
    return 'poor';
  };

  return (
    <div className="results-page">
      <div className="container-wide">
        <div className="results-header">
          <h1>Scan Results Demo</h1>
          <p>Analysis completed in {processingTime || '2.1'}s</p>
        </div>

        <div className="results-content">
          {/* Scan Results Layout - Two Column Design */}
          <div className="scan-results-layout">
            {/* Left Column - Analyzed Image */}
            <div className="analyzed-image-section">
              <div className="section-header">
                <h3>Analyzed Image</h3>
              </div>
              
              <div className="analyzed-image">
                <img src={sampleImageUrl} alt="Sample peso bill" />
                
                {/* Sample bounding boxes */}
                {yoloDetections.map((detection, index) => {
                  if (!detection.bbox) return null;
                  
                  return (
                    <div 
                      key={`demo-${index}`}
                      className={`detection-box enhanced-bbox feature-box-${index % 6}`}
                      style={{
                        left: `${detection.bbox[0] * 100}%`,
                        top: `${detection.bbox[1] * 100}%`,
                        width: `${(detection.bbox[2] - detection.bbox[0]) * 100}%`,
                        height: `${(detection.bbox[3] - detection.bbox[1]) * 100}%`,
                      }}
                      title={`${detection.class_name} (${(detection.confidence * 100).toFixed(1)}%)`}
                    >
                      <div className="feature-label-enhanced">
                        <span className="feature-name">{detection.class_name}</span>
                        <span className="model-source">yolo_model</span>
                      </div>
                      <div className="confidence-badge-enhanced">
                        {(detection.confidence * 100).toFixed(0)}%
                      </div>
                      <div className="bbox-border"></div>
                    </div>
                  );
                })}
              </div>

              {/* Detection Summary */}
              <div className="detection-summary">
                <p className="features-count">
                  🎯 <strong>{yoloDetections.length} security features</strong> detected by trained YOLOv8 model
                </p>
                <div className="feature-tags">
                  {yoloDetections.map((detection, index) => (
                    <span key={index} className={`feature-tag tag-${index % 6}`}>
                      {detection.class_name}
                    </span>
                  ))}
                </div>
                <div className="model-accuracy">
                  <span className="accuracy-badge">93.99% mAP50 Model</span>
                </div>
              </div>
            </div>

            {/* Right Column - Detection Results and Features */}
            <div className="results-panels">
              {/* Top Panel - Trained Model Detection Results */}
              <div className="detection-results-panel">
                <div className="panel-header">
                  <h3>🤖 Trained Model Detection Results</h3>
                </div>
                <div className="detection-stats">
                  <div className="stat-item">
                    <span className="stat-label">Total Features Found:</span>
                    <span className="stat-value">{yoloDetections.length}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Primary Detection:</span>
                    <span className="stat-value">{yoloDetections[0]?.class_name}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Highest Confidence:</span>
                    <span className="stat-value">{(yoloDetections[0]?.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Model Performance:</span>
                    <span className="stat-value">YOLOv8 (93.99% mAP50) - 100 Epochs</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Training Dataset:</span>
                    <span className="stat-value">Counterfeit Money Detector v5</span>
                  </div>
                </div>
              </div>

              {/* Bottom Panel - YOLOv8 Detected Features */}
              <div className="detected-features-panel">
                <div className="panel-header">
                  <h3>🎯 YOLOv8 Detected Features:</h3>
                </div>
                <div className="feature-confidence-bars">
                  {yoloDetections.map((detection, index) => {
                    const confidence = (detection.confidence * 100).toFixed(1);
                    const barColors = [
                      '#ef4444', // Red
                      '#10b981', // Green  
                      '#f59e0b', // Orange
                      '#8b5cf6', // Purple
                      '#06b6d4', // Cyan
                      '#ec4899', // Pink
                    ];
                    
                    return (
                      <div key={index} className="confidence-bar-item">
                        <div className="feature-info">
                          <span className="feature-name">{detection.class_name}</span>
                          <span className="confidence-percentage">{confidence}%</span>
                        </div>
                        <div className="confidence-bar">
                          <div 
                            className="confidence-fill"
                            style={{
                              width: `${confidence}%`,
                              backgroundColor: barColors[index % barColors.length]
                            }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>

          {/* Status Summary Section */}
          <div className="status-summary">
            <div className={`status-indicator ${isAuthentic ? 'authentic' : 'counterfeit'}`}>
              <div className="status-icon">
                {isAuthentic ? (
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12l2 2 4-4" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                  </svg>
                ) : (
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" strokeWidth="3"/>
                    <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" strokeWidth="3"/>
                  </svg>
                )}
              </div>
              
              <h2 className="status-text">
                {isAuthentic ? 'Authentic' : 'Counterfeit'}
              </h2>
              
              <div className="confidence-display">
                <div className="confidence-score">
                  <span className="confidence-label">Authenticity:</span>
                  <span className="confidence-value">{confidence}%</span>
                </div>
              </div>
              
              {denomination && (
                <div className="denomination">
                  <span className="denomination-label">Detected:</span>
                  <span className="denomination-value">₱{denomination}</span>
                </div>
              )}
            </div>
          </div>

          {/* Security Features Analysis */}
          <div className="features-section">
            <h3>🛡️ Security Features Analysis</h3>
            
            <div className="security-features-container">
              {/* Security Score Summary */}
              <div className="security-summary-card">
                <div className="summary-header">
                  <h4>🏆 Security Assessment</h4>
                </div>
                <div className="summary-content">
                  <div className="score-display">
                    <div className={`security-score ${getSecurityScoreClass()}`}>
                      {getSecurityScore()}%
                    </div>
                    <div className="score-label">Security Score</div>
                  </div>
                  <div className="features-summary">
                    <div className="summary-item">
                      <span className="summary-count">{getAuthenticatedFeaturesCount()}</span>
                      <span className="summary-text">Features Detected</span>
                    </div>
                    <div className="summary-item">
                      <span className="summary-count">{6 - getAuthenticatedFeaturesCount()}</span>
                      <span className="summary-text">Features Missing</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="results-actions">
          <button onClick={() => navigate('/scan')} className="btn btn-primary btn-large">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
              <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
            </svg>
            Scan Another Bill
          </button>
          
          <button onClick={() => navigate('/')} className="btn btn-secondary">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="currentColor" strokeWidth="2" fill="none"/>
            </svg>
            Back to Home
          </button>
        </div>
      </div>
    </div>
  );
};

export default StandaloneResultsDemo;