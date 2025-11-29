import React, { useState, useEffect } from 'react';
import './UVLight.css';

const UVLight = () => {
  const [isUVOn, setIsUVOn] = useState(false);
  const [intensity, setIntensity] = useState(75);
  const [selectedPalette, setSelectedPalette] = useState('standard');
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    const handleFullscreenChange = () => {
      const isCurrentlyFullscreen = !!(
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.msFullscreenElement
      );
      setIsFullscreen(isCurrentlyFullscreen);
      
      // Manage the fallback class
      const uvDisplay = document.querySelector('.uv-light-display');
      if (uvDisplay) {
        if (isCurrentlyFullscreen) {
          uvDisplay.classList.add('in-fullscreen');
        } else {
          uvDisplay.classList.remove('in-fullscreen');
        }
      }
    };

    const handleKeyPress = (event) => {
      if (event.key === 'Escape' && isFullscreen) {
        setIsFullscreen(false);
      }
      if (event.key === 'f' || event.key === 'F') {
        toggleFullscreen();
      }
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
    document.addEventListener('msfullscreenchange', handleFullscreenChange);
    document.addEventListener('keydown', handleKeyPress);

    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
      document.removeEventListener('webkitfullscreenchange', handleFullscreenChange);
      document.removeEventListener('msfullscreenchange', handleFullscreenChange);
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, [isFullscreen]); // eslint-disable-line react-hooks/exhaustive-deps

  const uvPalettes = {
    standard: {
      name: 'Standard UV',
      colors: ['#9D4EDD', '#7B2CBF', '#5A189A'],
      description: 'Professional UV authentication'
    },
    security: {
      name: 'Security Grade',
      colors: ['#4CC9F0', '#4895EF', '#4361EE'],
      description: 'High-security document verification'
    },
    forensic: {
      name: 'Forensic',
      colors: ['#7209B7', '#560BAD', '#3C096C'],
      description: 'Forensic analysis mode'
    }
  };

  const toggleUV = () => {
    setIsUVOn(!isUVOn);
  };

  const toggleFullscreen = async () => {
    try {
      if (!isFullscreen) {
        // Enter fullscreen
        const uvDisplay = document.querySelector('.uv-light-display');
        if (uvDisplay.requestFullscreen) {
          await uvDisplay.requestFullscreen();
        } else if (uvDisplay.webkitRequestFullscreen) {
          await uvDisplay.webkitRequestFullscreen();
        } else if (uvDisplay.msRequestFullscreen) {
          await uvDisplay.msRequestFullscreen();
        }
        // Add a class-based fallback to hide controls
        uvDisplay.classList.add('in-fullscreen');
        setIsFullscreen(true);
      } else {
        // Exit fullscreen
        if (document.exitFullscreen) {
          await document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
          await document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
          await document.msExitFullscreen();
        }
        // Remove the class-based fallback
        const uvDisplay = document.querySelector('.uv-light-display');
        uvDisplay.classList.remove('in-fullscreen');
        setIsFullscreen(false);
      }
    } catch (error) {
      console.error('Error toggling fullscreen:', error);
    }
  };



  return (
    <div className="uv-container">
      {/* Header */}
      <header className="uv-header">
        <div className="header-content">
          <div className="title-section">
            <h1>UV Light Detection</h1>
            <p>Professional UV authentication for Philippine peso banknotes</p>
          </div>
          <div className="status-section">
            <div className={`uv-status ${isUVOn ? 'active' : 'inactive'}`}>
              <div className="status-indicator"></div>
              <span>{isUVOn ? 'UV Active' : 'UV Inactive'}</span>
            </div>
          </div>
        </div>
      </header>

      <div className="uv-main">
        {/* UV Light Display Section */}
        <div className="uv-display-section">
          <div className={`uv-light-display ${isUVOn ? 'active' : 'inactive'} ${isFullscreen ? 'fullscreen' : ''}`}>
            <div 
              className="uv-light-surface"
              style={{
                background: isUVOn ? `radial-gradient(circle, ${uvPalettes[selectedPalette].colors.join(', ')})` : '#1a1a1a',
                opacity: isUVOn ? intensity / 100 : 0.1
              }}
            >
              {!isUVOn && (
                <div className="uv-off-message">
                  <h3>UV Light Inactive</h3>
                  <p>Click "Enable UV" to activate</p>
                </div>
              )}
              
              {isUVOn && (
                <div className="uv-active-overlay">
                  <div className="uv-glow-center"></div>
                </div>
              )}
            </div>

            {/* UV Controls */}
            <div className="uv-controls">
              <button
                className={`uv-button ${isUVOn ? 'active' : ''}`}
                onClick={toggleUV}
              >
                <span>{isUVOn ? 'Disable UV' : 'Enable UV'}</span>
              </button>

              <div className="intensity-control">
                <label>UV Intensity</label>
                <input
                  type="range"
                  min="25"
                  max="100"
                  value={intensity}
                  onChange={(e) => setIntensity(e.target.value)}
                  className="intensity-slider"
                />
                <span className="intensity-value">{intensity}%</span>
              </div>

              <button
                className="fullscreen-button"
                onClick={toggleFullscreen}
              >
                <span>{isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* UV Palette Selection Panel */}
        <div className="palette-panel">
          <div className="palette-selector-card">
            <h3>UV Palette</h3>
            <div className="palettes-grid">
              {Object.entries(uvPalettes).map(([key, palette]) => (
                <button
                  key={key}
                  className={`palette-option ${selectedPalette === key ? 'active' : ''}`}
                  onClick={() => setSelectedPalette(key)}
                >
                  <div className="palette-preview">
                    <div 
                      className="color-strip"
                      style={{
                        background: `linear-gradient(45deg, ${palette.colors.join(', ')})`
                      }}
                    ></div>
                  </div>
                  <div className="palette-info">
                    <h4>{palette.name}</h4>
                    <p>{palette.description}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="uv-usage-card">
            <h3>How to Use</h3>
            <div className="usage-steps">
              <div className="usage-step">
                <div className="step-number">1</div>
                <div className="step-text">Select your preferred UV palette</div>
              </div>
              <div className="usage-step">
                <div className="step-number">2</div>
                <div className="step-text">Enable UV light simulation</div>
              </div>
              <div className="usage-step">
                <div className="step-number">3</div>
                <div className="step-text">Adjust intensity as needed</div>
              </div>
              <div className="usage-step">
                <div className="step-number">4</div>
                <div className="step-text">Use fullscreen for immersive experience</div>
              </div>
            </div>
          </div>

          <div className="current-palette-info">
            <h3>Current Palette</h3>
            <div className="active-palette-display">
              <div className="palette-name">{uvPalettes[selectedPalette].name}</div>
              <div className="palette-description">{uvPalettes[selectedPalette].description}</div>
              <div className="color-samples">
                {uvPalettes[selectedPalette].colors.map((color, index) => (
                  <div 
                    key={index}
                    className="color-sample"
                    style={{ backgroundColor: color }}
                    title={color}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Notice */}
      <footer className="uv-footer">
        <div className="notice">
          <div className="notice-text">
            <strong>Note:</strong> This UV light simulation is for educational purposes. 
            For actual authentication, use professional UV equipment.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default UVLight;