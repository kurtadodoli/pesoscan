import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ResultsPage.css';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get result data from navigation state
  const { result, imageUrl, mode, scanType } = location.state || {};
  
  // Scroll to top when component mounts to show results from the beginning
  useEffect(() => {
    if (result) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, [result]);
  
  // Redirect to scan page if no data
  if (!result) {
    navigate('/scan');
    return null;
  }

  // Handle different result formats
  const isComprehensive = scanType === 'comprehensive';
  
  // For comprehensive scan with enhanced counterfeit detection
  const overallAssessment = result.overall_assessment;
  const counterfeitAnalysis = result.counterfeit_analysis;
  const pesoScan = result.peso_scan;
  
  // Extract detected features from the trained YOLO model
  const yoloDetections = pesoScan?.result?.detections || [];
  
  // For basic scan (maintain backward compatibility)
  const basicResult = result.result;
  
  // Extract common values based on scan type with enhanced counterfeit detection
  const isAuthentic = isComprehensive 
    ? overallAssessment?.authenticity_score >= 0.55  // Lowered threshold for clearer detection
    : basicResult?.authentic;
    
  const confidence = isComprehensive
    ? Math.round((overallAssessment?.authenticity_score || 0) * 100)
    : Math.round(basicResult?.confidence || 0);
    
  const counterfeitProbability = isComprehensive
    ? Math.round((overallAssessment?.counterfeit_probability || 0) * 100)
    : (100 - confidence);
    
  // Extract peso denomination from detections
  const getPesoDenomination = () => {
    // Debug: Log all available data
    console.log('DEBUG - Full result data:', result);
    console.log('DEBUG - isComprehensive:', isComprehensive);
    console.log('DEBUG - overallAssessment:', overallAssessment);
    console.log('DEBUG - basicResult:', basicResult);
    console.log('DEBUG - yoloDetections:', yoloDetections);
    console.log('DEBUG - pesoScan:', pesoScan);
    
    // First try the official denomination field
    const officialDenomination = isComprehensive
      ? overallAssessment?.denomination
      : basicResult?.denomination;
    
    console.log('DEBUG - officialDenomination:', officialDenomination);
    
    if (officialDenomination && /^\d+$/.test(officialDenomination.toString())) {
      return officialDenomination;
    }
    
    // Check peso scan results
    if (pesoScan?.result?.denomination) {
      console.log('DEBUG - peso scan denomination:', pesoScan.result.denomination);
      const value = parseInt(pesoScan.result.denomination);
      if ([1, 5, 10, 20, 50, 100, 200, 500, 1000].includes(value)) {
        return value;
      }
    }
    
    // Extract from YOLO detections (look for peso class names)
    if (yoloDetections && yoloDetections.length > 0) {
      console.log('DEBUG - yoloDetections details:', yoloDetections);
      for (const detection of yoloDetections) {
        const className = detection.class_name || detection.feature_name || '';
        console.log('DEBUG - checking class name:', className);
        // Look for peso values (1, 5, 10, 20, 50, 100, 200, 500, 1000)
        const pesoMatch = className.match(/(\d+)/);
        if (pesoMatch) {
          const value = parseInt(pesoMatch[1]);
          console.log('DEBUG - matched peso value:', value);
          if ([1, 5, 10, 20, 50, 100, 200, 500, 1000].includes(value)) {
            return value;
          }
        }
      }
    }
    
    // Extract from combined detections
    if (result.combined_detections?.peso_features) {
      console.log('DEBUG - peso features:', result.combined_detections.peso_features);
      for (const feature of result.combined_detections.peso_features) {
        const featureName = feature.feature_name || feature.feature || '';
        console.log('DEBUG - peso feature name:', featureName);
        const pesoMatch = featureName.match(/(\d+)/);
        if (pesoMatch) {
          const value = parseInt(pesoMatch[1]);
          console.log('DEBUG - peso feature value:', value);
          if ([1, 5, 10, 20, 50, 100, 200, 500, 1000].includes(value)) {
            return value;
          }
        }
      }
    }
    
    // Extract from basic result detections
    if (result.result?.detections) {
      console.log('DEBUG - basic detections:', result.result.detections);
      for (const detection of result.result.detections) {
        const className = detection.class_name || detection.feature_name || '';
        console.log('DEBUG - basic detection class name:', className);
        const pesoMatch = className.match(/(\d+)/);
        if (pesoMatch) {
          const value = parseInt(pesoMatch[1]);
          console.log('DEBUG - basic detection value:', value);
          if ([1, 5, 10, 20, 50, 100, 200, 500, 1000].includes(value)) {
            return value;
          }
        }
      }
    }
    
    console.log('DEBUG - No peso denomination found');
    return null;
  };
  
  const denomination = getPesoDenomination();
  const processingTime = result.processing_time?.toFixed(2);
  
  const features = isComprehensive
    ? counterfeitAnalysis?.security_analysis || {}
    : basicResult?.features || {};
  
  // These variables are available for future use
  // const overallRecommendation = isComprehensive ? overallAssessment?.recommendation : null;
  // const counterfeitRecommendations = isComprehensive ? counterfeitAnalysis?.recommendations || [] : [];
  // const detectedFeatures = isComprehensive ? counterfeitAnalysis?.detected_features || [] : [];
  
  // Determine authenticity status with clear messaging
  const getAuthenticityStatus = () => {
    if (!isComprehensive) {
      return isAuthentic ? 'Authentic' : 'Counterfeit';
    }
    
    const score = overallAssessment?.authenticity_score || 0;
    if (score >= 0.75) return 'Authentic';
    if (score >= 0.55) return 'Likely Authentic';
    if (score >= 0.35) return 'Suspicious';
    return 'Likely Counterfeit';
  };
  
  const getStatusColor = () => {
    if (!isComprehensive) {
      return isAuthentic ? 'authentic' : 'counterfeit';
    }
    
    const score = overallAssessment?.authenticity_score || 0;
    if (score >= 0.75) return 'authentic';
    if (score >= 0.55) return 'likely-authentic';
    if (score >= 0.35) return 'suspicious';
    return 'counterfeit';
  };

  // Helper functions for security features analysis
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

  const handleNewScan = () => {
    navigate('/scan');
  };

  const handleSaveToHistory = () => {
    // Save to local storage for now (in production, this would save to backend)
    const existingHistory = JSON.parse(localStorage.getItem('pesoscan_history') || '[]');
    const scanRecord = {
      id: result.id || Date.now().toString(),
      timestamp: result.timestamp || new Date().toISOString(),
      result: result.result,
      imageUrl: imageUrl,
      mode: mode,
      processingTime: result.processing_time
    };
    
    existingHistory.unshift(scanRecord); // Add to beginning
    localStorage.setItem('pesoscan_history', JSON.stringify(existingHistory.slice(0, 50))); // Keep last 50
    
    alert('Scan saved to history!');
  };

  return (
    <div className="results-page">
      <div className="container-wide">
        <div className="results-header">
          <h1>Scan Results</h1>
          
          {/* Main Authentication Status Indicator */}
          <div className="main-status-indicator">
            <div className={`main-status ${getStatusColor()}`}>
              <div className="main-status-icon">
                {isAuthentic ? (
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12l2 2 4-4" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                  </svg>
                ) : (
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" strokeWidth="3"/>
                    <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" strokeWidth="3"/>
                  </svg>
                )}
              </div>
              <div className="main-status-content">
                <span className="main-status-text">{getAuthenticityStatus()}</span>
                <span className="main-confidence">{confidence}% Confidence</span>
                {denomination && (
                  <span className="main-denomination">₱{denomination}</span>
                )}
              </div>
            </div>
          </div>
          
          <p>Analysis completed in {processingTime || '1.2'}s</p>
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
                <img src={imageUrl} alt="Analyzed peso bill" />
                
                {/* Enhanced bounding boxes from trained models */}
                {(() => {
                  // Get all available detections from different sources
                  const pesoDetections = pesoScan?.result?.detections || [];
                  const combinedDetections = result.combined_detections;
                  
                  // Helper function to convert bbox format and ensure valid positioning
                  const normalizeBbox = (bbox) => {
                    if (!bbox) return null;
                    
                    let normalized = null;
                    
                    // Handle array format [x1, y1, x2, y2] (normalized 0-1)
                    if (Array.isArray(bbox) && bbox.length >= 4) {
                      normalized = bbox;
                    }
                    // Handle object format {x, y, width, height} (normalized 0-1)
                    else if (typeof bbox === 'object' && bbox.x !== undefined) {
                      normalized = [bbox.x, bbox.y, bbox.x + bbox.width, bbox.y + bbox.height];
                    }
                    
                    if (!normalized) return null;
                    
                    // Ensure coordinates are within valid bounds and properly ordered
                    const x1 = Math.max(0, Math.min(1, normalized[0]));
                    const y1 = Math.max(0, Math.min(1, normalized[1]));
                    const x2 = Math.max(x1 + 0.01, Math.min(1, normalized[2])); // Ensure minimum width
                    const y2 = Math.max(y1 + 0.01, Math.min(1, normalized[3])); // Ensure minimum height
                    
                    return [x1, y1, x2, y2];
                  };
                  
                  // Prioritize combined detections if available
                  let allDetections = [];
                  
                  if (combinedDetections) {
                    // Add peso features
                    allDetections = allDetections.concat(
                      (combinedDetections.peso_features || []).map((d, i) => ({
                        ...d,
                        source: 'peso_model',
                        display_name: d.feature_name || `₱${d.class_name}`,
                        bbox: normalizeBbox(d.bbox),
                        confidence: d.confidence,
                        color_class: `peso-feature-${i % 4}`
                      }))
                    );
                    
                    // Add security features
                    allDetections = allDetections.concat(
                      (combinedDetections.security_features || []).map((d, i) => ({
                        ...d,
                        source: 'counterfeit_model', 
                        display_name: d.feature_name || d.feature,
                        bbox: normalizeBbox(d.bbox),
                        confidence: d.confidence,
                        color_class: `security-feature-${i % 6}`
                      }))
                    );
                  } else if (yoloDetections && yoloDetections.length > 0) {
                    allDetections = yoloDetections.map((d, i) => ({
                      ...d,
                      source: 'yolo_model',
                      display_name: d.feature_name || d.class_name,
                      bbox: normalizeBbox(d.bbox),
                      confidence: d.confidence,
                      color_class: `feature-box-${i % 6}`
                    }));
                  } else if (pesoDetections.length > 0) {
                    allDetections = pesoDetections.map((d, i) => ({
                      ...d,
                      source: 'peso_model',
                      display_name: d.feature_name || `₱${d.class_name}`,
                      bbox: normalizeBbox(d.bbox),
                      confidence: d.confidence,
                      color_class: `peso-feature-${i % 4}`
                    }));
                  }
                  
                  // Filter out detections without valid bounding boxes and sort by confidence
                  const validDetections = allDetections
                    .filter(d => d.bbox && d.bbox.length >= 4)
                    .sort((a, b) => (b.confidence || 0) - (a.confidence || 0)) // Sort by confidence (highest first)
                    .slice(0, 8); // Limit to top 8 detections to avoid clutter
                  
                  return validDetections.length > 0 ? (
                    validDetections.map((detection, index) => {
                      const bbox = detection.bbox;
                      const confidence = detection.confidence || 0;
                      
                      // Calculate position and size with better bounds checking
                      const left = bbox[0] * 100;
                      const top = bbox[1] * 100;
                      const width = (bbox[2] - bbox[0]) * 100;
                      const height = (bbox[3] - bbox[1]) * 100;
                      
                      return (
                        <div 
                          key={`${detection.source}-${index}`}
                          className={`detection-box enhanced-bbox ${detection.color_class}`}
                          style={{
                            left: `${left}%`,
                            top: `${top}%`,
                            width: `${width}%`,
                            height: `${height}%`,
                            zIndex: 10 + index, // Higher z-index for higher confidence detections
                          }}
                          title={`${detection.display_name} (${(confidence * 100).toFixed(1)}%)`}
                        >
                          <div className="feature-label-enhanced">
                            {detection.display_name}
                          </div>
                          <div className="confidence-badge-enhanced">
                            {(confidence * 100).toFixed(0)}%
                          </div>
                          <div className="bbox-border"></div>
                        </div>
                      );
                    })
                  ) : null;
                })()}
                
                {/* Fallback to basic detections */}
                {!yoloDetections && result.result?.detections && result.result.detections.length > 0 ? (
                  // Basic scan detections
                  result.result.detections.map((detection, index) => (
                    <div 
                      key={index}
                      className={`detection-box feature-box-${index % 6}`}
                      style={{
                        left: `${detection.bbox[0] * 100}%`,
                        top: `${detection.bbox[1] * 100}%`,
                        width: `${(detection.bbox[2] - detection.bbox[0]) * 100}%`,
                        height: `${(detection.bbox[3] - detection.bbox[1]) * 100}%`,
                      }}
                      title={`${detection.feature_name || detection.class_name} (${(detection.confidence * 100).toFixed(1)}%)`}
                    >
                      <div className="feature-label">
                        {detection.feature_name || `₱${detection.class_name}`}
                      </div>
                      <div className="confidence-badge">
                        {(detection.confidence * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))
                ) : result.result?.detection?.bbox ? (
                  // Fallback to single detection box for backward compatibility
                  <div 
                    className="detection-box"
                    style={{
                      left: `${result.result.detection.bbox[0] * 100}%`,
                      top: `${result.result.detection.bbox[1] * 100}%`,
                      width: `${(result.result.detection.bbox[2] - result.result.detection.bbox[0]) * 100}%`,
                      height: `${(result.result.detection.bbox[3] - result.result.detection.bbox[1]) * 100}%`,
                    }}
                    title={`Detection (${(result.result.detection.confidence * 100).toFixed(1)}%)`}
                  >
                    <div className="feature-label">
                      {result.result.detection.feature_name || 'Detection'}
                    </div>
                    <div className="confidence-badge">
                      {(result.result.detection.confidence * 100).toFixed(0)}%
                    </div>
                  </div>
                ) : null}
              </div>

              {/* Detection Summary */}
              <div className="detection-summary">
                {(() => {
                  const combinedDetections = result.combined_detections;
                  const pesoDetections = pesoScan?.result?.detections || [];
                  const yoloDetections = pesoDetections;
                  
                  if (combinedDetections) {
                    const pesoFeatures = combinedDetections.peso_features || [];
                    const securityFeatures = combinedDetections.security_features || [];
                    const totalFeatures = pesoFeatures.length + securityFeatures.length;
                    
                    return (
                      <>
                        <p className="features-count">
                          <strong>{totalFeatures} features detected</strong> by trained AI models
                        </p>
                        <div className="feature-tags">
                          {pesoFeatures.slice(0, 4).map((detection, index) => (
                            <span key={`peso-${index}`} className={`feature-tag tag-${index % 6}`}>
                              ₱{detection.feature_name}
                            </span>
                          ))}
                          {securityFeatures.slice(0, 4).map((detection, index) => (
                            <span key={`security-${index}`} className={`feature-tag tag-${(index + 4) % 6}`}>
                              {detection.feature_name}
                            </span>
                          ))}
                          {totalFeatures > 8 && (
                            <span className="feature-tag more">+{totalFeatures - 8} more</span>
                          )}
                        </div>
                        <div className="model-accuracy">
                          <span className="accuracy-badge">94.0% mAP50 Models</span>
                        </div>
                      </>
                    );
                  } else if (yoloDetections && yoloDetections.length > 0) {
                    return (
                      <>
                        <p className="features-count">
                          <strong>{yoloDetections.length} features detected</strong> by trained AI models
                        </p>
                        <div className="feature-tags">
                          {yoloDetections.slice(0, 8).map((detection, index) => (
                            <span key={index} className={`feature-tag tag-${index % 6}`}>
                              {detection.class_name}
                            </span>
                          ))}
                          {yoloDetections.length > 8 && (
                            <span className="feature-tag more">+{yoloDetections.length - 8} more</span>
                          )}
                        </div>
                        <div className="model-accuracy">
                          <span className="accuracy-badge">93.99% mAP50 Model</span>
                        </div>
                      </>
                    );
                  } else if (result.result?.detections && result.result.detections.length > 0) {
                    return (
                      <>
                        <p className="features-count">
                          <strong>{result.result.detections.length} features detected</strong> by trained AI models
                        </p>
                        <div className="feature-tags">
                          {result.result.detections.slice(0, 8).map((detection, index) => (
                            <span key={index} className={`feature-tag tag-${index % 6}`}>
                              {detection.feature_name || `₱${detection.class_name}`}
                            </span>
                          ))}
                          {result.result.detections.length > 8 && (
                            <span className="feature-tag more">+{result.result.detections.length - 8} more</span>
                          )}
                        </div>
                      </>
                    );
                  } else {
                    return (
                      <p className="scan-method">
                        Method: {mode === 'camera' ? 'Camera Scan' : 'File Upload'}
                      </p>
                    );
                  }
                })()}
              </div>


            </div>

            {/* Right Column - Detection Results and Features */}
            <div className="results-panels">
              {/* Detected Features */}
              <div className="detected-features-panel">
                <div className="panel-header">
                  <h3>Detected Features</h3>
                </div>
                <div className="feature-confidence-bars">
                  {yoloDetections && yoloDetections.length > 0 ? (
                    yoloDetections.slice(0, 10).map((detection, index) => {
                      const confidence = (detection.confidence * 100).toFixed(1);
                      const barColors = [
                        '#ef4444', // Red
                        '#10b981', // Green  
                        '#f59e0b', // Orange
                        '#8b5cf6', // Purple
                        '#06b6d4', // Cyan
                        '#ec4899', // Pink
                        '#14b8a6', // Teal
                        '#f97316', // Orange-500
                        '#6366f1', // Indigo
                        '#84cc16'  // Lime
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
                    })
                  ) : result.result?.detections && result.result.detections.length > 0 ? (
                    result.result.detections.slice(0, 6).map((detection, index) => {
                      const confidence = (detection.confidence * 100).toFixed(1);
                      const barColors = ['#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#ec4899'];
                      
                      return (
                        <div key={index} className="confidence-bar-item">
                          <div className="feature-info">
                            <span className="feature-name">{detection.feature_name || `₱${detection.class_name}`}</span>
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
                    })
                  ) : (
                    <div className="no-features-detected">
                      <span className="placeholder-icon">🔍</span>
                      <p>No features detected with confidence scores</p>
                      <p className="sub-text">Try using the comprehensive scan mode</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>



          {/* Enhanced Security Features Analysis - Collapsible Section */}
          {(features.security_thread || features.watermark || features.microprinting || 
            features.color_changing_ink || features.uv_features || features.raised_printing) && (
            <div className="features-section">
              <h3>🛡️ Security Features Analysis</h3>
              
              {/* Enhanced Security Features Grid */}
              <div className="security-features-container">
                {/* Primary Security Features */}
                <div className="security-category">
                  <h4 className="category-title">🔒 Primary Security Features</h4>
                  <div className="features-grid primary-features">
                    <div className={`feature-card ${features.security_thread ? 'authenticated' : 'missing'}`}>
                      <div className="feature-icon-wrapper">
                        <div className="feature-icon">
                          {features.security_thread ? '🔐' : '❌'}
                        </div>
                      </div>
                      <div className="feature-content">
                        <h5 className="feature-name">Security Thread</h5>
                        <p className="feature-description">Embedded metallic strip</p>
                        <span className={`feature-status ${features.security_thread ? 'detected' : 'missing'}`}>
                          {features.security_thread ? '✅ Detected' : '❌ Not Found'}
                        </span>
                      </div>
                    </div>

                    <div className={`feature-card ${features.watermark ? 'authenticated' : 'missing'}`}>
                      <div className="feature-icon-wrapper">
                        <div className="feature-icon">
                          {features.watermark ? '💧' : '❌'}
                        </div>
                      </div>
                      <div className="feature-content">
                        <h5 className="feature-name">Watermark</h5>
                        <p className="feature-description">Portrait visible in light</p>
                        <span className={`feature-status ${features.watermark ? 'detected' : 'missing'}`}>
                          {features.watermark ? '✅ Detected' : '❌ Not Found'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Advanced Security Features */}
                <div className="security-category">
                  <h4 className="category-title">🔬 Advanced Security Features</h4>
                  <div className="features-grid advanced-features">
                    <div className={`feature-card ${features.microprinting ? 'authenticated' : 'missing'}`}>
                      <div className="feature-icon-wrapper">
                        <div className="feature-icon">
                          {features.microprinting ? '🔍' : '❌'}
                        </div>
                      </div>
                      <div className="feature-content">
                        <h5 className="feature-name">Microprinting</h5>
                        <p className="feature-description">Tiny text requiring magnification</p>
                        <span className={`feature-status ${features.microprinting ? 'detected' : 'missing'}`}>
                          {features.microprinting ? '✅ Detected' : '❌ Not Found'}
                        </span>
                      </div>
                    </div>

                    <div className={`feature-card ${features.color_changing_ink ? 'authenticated' : 'missing'}`}>
                      <div className="feature-icon-wrapper">
                        <div className="feature-icon">
                          {features.color_changing_ink ? '🎨' : '❌'}
                        </div>
                      </div>
                      <div className="feature-content">
                        <h5 className="feature-name">Color-Changing Ink</h5>
                        <p className="feature-description">Optically variable device</p>
                        <span className={`feature-status ${features.color_changing_ink ? 'detected' : 'missing'}`}>
                          {features.color_changing_ink ? '✅ Detected' : '❌ Not Found'}
                        </span>
                      </div>
                    </div>

                    <div className={`feature-card ${features.uv_features ? 'authenticated' : 'missing'}`}>
                      <div className="feature-icon-wrapper">
                        <div className="feature-icon">
                          {features.uv_features ? '💡' : '❌'}
                        </div>
                      </div>
                      <div className="feature-content">
                        <h5 className="feature-name">UV Features</h5>
                        <p className="feature-description">Ultraviolet reactive elements</p>
                        <span className={`feature-status ${features.uv_features ? 'detected' : 'missing'}`}>
                          {features.uv_features ? '✅ Detected' : '❌ Not Found'}
                        </span>
                      </div>
                    </div>

                    <div className={`feature-card ${features.raised_printing ? 'authenticated' : 'missing'}`}>
                      <div className="feature-icon-wrapper">
                        <div className="feature-icon">
                          {features.raised_printing ? '📝' : '❌'}
                        </div>
                      </div>
                      <div className="feature-content">
                        <h5 className="feature-name">Raised Printing</h5>
                        <p className="feature-description">Tactile intaglio printing</p>
                        <span className={`feature-status ${features.raised_printing ? 'detected' : 'missing'}`}>
                          {features.raised_printing ? '✅ Detected' : '❌ Not Found'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

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
          )}
          
          {/* Comprehensive Analysis Section */}
          {isComprehensive && counterfeitAnalysis && (
            <div className="comprehensive-section">
              <h3>Comprehensive Counterfeit Analysis</h3>
              
              <div className="analysis-summary">
                <div className="summary-item">
                  <span className="summary-label">Authenticity Score:</span>
                  <span className={`summary-value ${overallAssessment?.authenticity_score >= 0.6 ? 'positive' : 'negative'}`}>
                    {Math.round((overallAssessment?.authenticity_score || 0) * 100)}%
                  </span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Counterfeit Probability:</span>
                  <span className={`summary-value ${overallAssessment?.counterfeit_probability <= 0.4 ? 'positive' : 'negative'}`}>
                    {Math.round((overallAssessment?.counterfeit_probability || 0) * 100)}%
                  </span>
                </div>
              </div>
              
              <div className="analysis-recommendation">
                <h4>Recommendation</h4>
                <p className={`recommendation-text ${overallAssessment?.authenticity_score >= 0.6 ? 'positive' : 'negative'}`}>
                  {overallAssessment?.recommendation || 'Analysis incomplete'}
                </p>
              </div>
              
              {counterfeitAnalysis?.detected_features && counterfeitAnalysis.detected_features.length > 0 && (
                <div className="detected-features">
                  <h4>Detected Counterfeit Analysis Features</h4>
                  <div className="features-list">
                    {counterfeitAnalysis.detected_features.slice(0, 6).map((feature, index) => (
                      <div key={index} className="feature-badge">
                        <span className="feature-name">{feature.feature}</span>
                        <span className="feature-confidence">{Math.round(feature.confidence * 100)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {counterfeitAnalysis?.recommendations && counterfeitAnalysis.recommendations.length > 0 && (
                <div className="analysis-recommendations">
                  <h4>Additional Recommendations</h4>
                  <ul className="recommendations-list">
                    {counterfeitAnalysis.recommendations.map((rec, index) => (
                      <li key={index}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="results-actions">
          <button onClick={handleNewScan} className="btn btn-primary btn-large">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
              <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
            </svg>
            Scan Another Bill
          </button>
          
          <button onClick={handleSaveToHistory} className="btn btn-secondary">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
            </svg>
            Save to History
          </button>
        </div>

        <div className="disclaimer-section">
          <div className="disclaimer-card">
            <h4>Important Disclaimer</h4>
            <p>
              This system is designed for educational and research purposes. 
              While our AI model strives for high accuracy, it should not be used as the sole method 
              for currency authentication in critical financial decisions. 
              Always verify suspicious bills through official banking channels and trained professionals.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;