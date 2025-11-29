import React, { useState, useEffect } from 'react';
import './AROverlay.css';

const AROverlay = ({ isActive, detectedFeatures, imageRef }) => {
  const [overlayElements, setOverlayElements] = useState([]);

  useEffect(() => {
    if (isActive && detectedFeatures && imageRef?.current) {
      const elements = detectedFeatures.map((feature, index) => ({
        id: index,
        name: feature.feature_name || feature.class_name || 'Security Feature',
        confidence: feature.confidence,
        bbox: feature.bbox,
        type: getFeatureType(feature.feature_name || feature.class_name)
      }));
      setOverlayElements(elements);
    } else {
      setOverlayElements([]);
    }
  }, [isActive, detectedFeatures, imageRef]);

  const getFeatureType = (featureName) => {
    if (!featureName) return 'default';
    const name = featureName.toLowerCase();
    
    if (name.includes('watermark') || name.includes('portrait')) return 'watermark';
    if (name.includes('thread') || name.includes('security')) return 'security-thread';
    if (name.includes('serial') || name.includes('number')) return 'serial';
    if (name.includes('eagle') || name.includes('bird')) return 'design';
    if (name.includes('flower') || name.includes('plant')) return 'design';
    if (name.includes('denomination') || name.includes('value')) return 'denomination';
    return 'feature';
  };

  const getOverlayColor = (type) => {
    const colors = {
      watermark: '#8b5cf6',
      'security-thread': '#f59e0b',
      serial: '#10b981',
      design: '#3b82f6',
      denomination: '#ef4444',
      feature: '#6b7280'
    };
    return colors[type] || colors.feature;
  };

  if (!isActive || overlayElements.length === 0) {
    return null;
  }

  return (
    <div className="ar-overlay">
      <div className="ar-header">
        <div className="ar-status">
          <div className="ar-indicator active"></div>
          <span>AR Detection Active</span>
        </div>
        <div className="features-count">
          {overlayElements.length} Features Detected
        </div>
      </div>

      <div className="ar-features-list">
        {overlayElements.map((element) => (
          <div key={element.id} className={`ar-feature-item ${element.type}`}>
            <div 
              className="feature-indicator" 
              style={{ backgroundColor: getOverlayColor(element.type) }}
            ></div>
            <div className="feature-info">
              <span className="feature-name">{element.name}</span>
              <span className="feature-confidence">
                {(element.confidence * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="ar-controls">
        <button className="ar-toggle-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" strokeWidth="2"/>
            <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
          </svg>
          Hide Overlays
        </button>
      </div>

      {/* AR Bounding Boxes Overlay */}
      <div className="ar-bounding-boxes">
        {overlayElements.map((element) => (
          <div
            key={`bbox-${element.id}`}
            className="ar-bbox"
            style={{
              borderColor: getOverlayColor(element.type),
              boxShadow: `0 0 10px ${getOverlayColor(element.type)}40`
            }}
          >
            <div 
              className="ar-label"
              style={{ backgroundColor: getOverlayColor(element.type) }}
            >
              <span className="label-name">{element.name}</span>
              <span className="label-confidence">
                {(element.confidence * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AROverlay;