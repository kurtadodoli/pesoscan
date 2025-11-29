import React, { useState, useEffect } from 'react';
import './UVDetection.css';

const UVDetection = ({ imageData, detectedFeatures, isActive }) => {
  const [uvMode, setUvMode] = useState(false);
  const [uvFeatures, setUvFeatures] = useState([]);
  const [intensity, setIntensity] = useState(75);

  useEffect(() => {
    if (isActive && detectedFeatures) {
      // Simulate UV-reactive features based on detected elements
      const uvReactiveFeatures = detectedFeatures.filter(feature => 
        isUVReactive(feature.feature_name || feature.class_name)
      ).map(feature => ({
        ...feature,
        uvIntensity: Math.random() * 0.5 + 0.5, // 50-100% UV reactivity
        uvColor: getUVColor(feature.feature_name || feature.class_name)
      }));
      
      setUvFeatures(uvReactiveFeatures);
    }
  }, [isActive, detectedFeatures]);

  const isUVReactive = (featureName) => {
    if (!featureName) return false;
    const uvReactiveTerms = [
      'watermark', 'security_thread', 'serial_number', 
      'denomination', 'microprint', 'uv_feature'
    ];
    return uvReactiveTerms.some(term => 
      featureName.toLowerCase().includes(term.replace('_', ''))
    );
  };

  const getUVColor = (featureName) => {
    if (!featureName) return '#00ffff';
    const name = featureName.toLowerCase();
    
    if (name.includes('watermark')) return '#00ffff'; // Cyan
    if (name.includes('thread')) return '#ff00ff'; // Magenta
    if (name.includes('serial')) return '#ffff00'; // Yellow
    if (name.includes('denomination')) return '#00ff00'; // Green
    return '#8a2be2'; // Blue Violet
  };

  const toggleUVMode = () => {
    setUvMode(!uvMode);
  };

  if (!isActive) {
    return null;
  }

  return (
    <div className="uv-detection">
      <div className="uv-controls">
        <div className="uv-header">
          <h3>UV Detection Simulation</h3>
          <div className="uv-status">
            <div className={`uv-indicator ${uvMode ? 'active' : ''}`}></div>
            <span>{uvMode ? 'UV Light ON' : 'UV Light OFF'}</span>
          </div>
        </div>

        <div className="uv-control-panel">
          <button 
            className={`uv-toggle ${uvMode ? 'active' : ''}`}
            onClick={toggleUVMode}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="2"/>
              <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" strokeWidth="2"/>
              <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" strokeWidth="2"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" strokeWidth="2"/>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" strokeWidth="2"/>
              <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" strokeWidth="2"/>
              <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" strokeWidth="2"/>
            </svg>
            {uvMode ? 'Turn Off UV' : 'Turn On UV'}
          </button>

          {uvMode && (
            <div className="uv-intensity-control">
              <label>UV Intensity: {intensity}%</label>
              <input
                type="range"
                min="0"
                max="100"
                value={intensity}
                onChange={(e) => setIntensity(e.target.value)}
                className="intensity-slider"
              />
            </div>
          )}
        </div>
      </div>

      {uvMode && (
        <div className="uv-overlay" style={{ opacity: intensity / 100 }}>
          <div className="uv-background"></div>
          
          <div className="uv-features">
            {uvFeatures.map((feature, index) => (
              <div
                key={index}
                className="uv-feature"
                style={{
                  borderColor: feature.uvColor,
                  boxShadow: `0 0 15px ${feature.uvColor}`,
                  opacity: feature.uvIntensity
                }}
              >
                <div 
                  className="uv-glow"
                  style={{ 
                    backgroundColor: feature.uvColor,
                    opacity: 0.3 * feature.uvIntensity
                  }}
                ></div>
                <div 
                  className="uv-label"
                  style={{ backgroundColor: feature.uvColor }}
                >
                  UV: {feature.feature_name || 'Security Feature'}
                </div>
              </div>
            ))}
          </div>

          <div className="uv-info-panel">
            <h4>UV-Reactive Features Detected</h4>
            <div className="uv-features-list">
              {uvFeatures.length === 0 ? (
                <p className="no-uv-features">No UV-reactive features detected</p>
              ) : (
                uvFeatures.map((feature, index) => (
                  <div key={index} className="uv-feature-item">
                    <div 
                      className="uv-color-indicator"
                      style={{ backgroundColor: feature.uvColor }}
                    ></div>
                    <div className="uv-feature-info">
                      <span className="uv-feature-name">
                        {feature.feature_name || 'Security Feature'}
                      </span>
                      <span className="uv-reactivity">
                        {(feature.uvIntensity * 100).toFixed(0)}% Reactive
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      <div className="uv-disclaimer">
        <p>
          <strong>Note:</strong> This is an AI simulation of UV light detection. 
          For official authentication, use actual UV light sources.
        </p>
      </div>
    </div>
  );
};

export default UVDetection;