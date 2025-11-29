import React, { useState, useRef, useEffect, useCallback } from 'react';
import './DigitalMagnifier.css';

const DigitalMagnifier = () => {
  const [isActive, setIsActive] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(2);
  const [isFlashlightOn, setIsFlashlightOn] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [magnifierPosition, setMagnifierPosition] = useState({ x: 50, y: 50 });
  const [isDragging, setIsDragging] = useState(false);
  const [cameraStream, setCameraStream] = useState(null);
  const [showGrid, setShowGrid] = useState(true);
  const [measurementMode, setMeasurementMode] = useState(false);
  const [measurements, setMeasurements] = useState([]);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const magnifierRef = useRef(null);

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

  const toggleMagnifier = () => {
    setIsActive(!isActive);
  };

  const handleZoomChange = (newZoom) => {
    setZoomLevel(Math.max(1, Math.min(10, newZoom)));
  };

  const toggleFlashlight = async () => {
    if (cameraStream) {
      const track = cameraStream.getVideoTracks()[0];
      if (track && track.getCapabilities().torch) {
        try {
          await track.applyConstraints({
            advanced: [{ torch: !isFlashlightOn }]
          });
          setIsFlashlightOn(!isFlashlightOn);
        } catch (error) {
          console.error('Flashlight not supported:', error);
        }
      }
    }
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      const ctx = canvas.getContext('2d');
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);
      
      const imageData = canvas.toDataURL('image/jpeg', 0.9);
      setCapturedImage(imageData);
    }
  };

  const handleMouseMove = useCallback((e) => {
    if (!isDragging) return;
    
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    
    setMagnifierPosition({
      x: Math.max(0, Math.min(100, x)),
      y: Math.max(0, Math.min(100, y))
    });
  }, [isDragging]);

  const handleMouseDown = () => {
    setIsDragging(true);
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const addMeasurement = (e) => {
    if (!measurementMode) return;
    
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    
    setMeasurements(prev => [...prev, { 
      id: Date.now(), 
      x, 
      y, 
      label: `Point ${prev.length + 1}` 
    }]);
  };

  const clearMeasurements = () => {
    setMeasurements([]);
  };

  const magnifierFeatures = [
    {
      title: 'High-Quality Zoom',
      description: 'Magnify up to 10x for detailed inspection',
      icon: '🔍'
    },
    {
      title: 'Grid Overlay',
      description: 'Reference grid for precise measurements',
      icon: '📐'
    },
    {
      title: 'Image Capture',
      description: 'Save magnified images for analysis',
      icon: '📸'
    },
    {
      title: 'Flashlight Support',
      description: 'Built-in LED flash for better visibility',
      icon: '🔦'
    },
    {
      title: 'Measurement Tools',
      description: 'Mark and measure specific features',
      icon: '📏'
    },
    {
      title: 'Real-Time Preview',
      description: 'Live magnification with smooth controls',
      icon: '⚡'
    }
  ];

  const securityElements = [
    {
      element: 'Microprinting',
      description: 'Tiny text visible only under magnification',
      zoomLevel: '5-8x',
      tip: 'Look for sharp, clear text that becomes readable only when magnified'
    },
    {
      element: 'Security Thread',
      description: 'Embedded thread with detailed patterns',
      zoomLevel: '3-5x',
      tip: 'Check for continuous thread with microtext or patterns'
    },
    {
      element: 'Intaglio Printing',
      description: 'Raised printing texture',
      zoomLevel: '2-4x',
      tip: 'Look for raised areas that cast shadows under angled light'
    },
    {
      element: 'Watermark Details',
      description: 'Fine details in watermark design',
      zoomLevel: '3-6x',
      tip: 'Examine the shading and fine lines in watermark areas'
    },
    {
      element: 'Color-Changing Ink',
      description: 'Optical variable ink patterns',
      zoomLevel: '4-7x',
      tip: 'Look for color shifts and holographic patterns'
    }
  ];

  return (
    <div className="magnifier-container">
      <div className="magnifier-header">
        <h1>🔎 Digital Magnifier</h1>
        <p>Professional magnification tool for detailed peso banknote inspection</p>
      </div>

      <div className="magnifier-main">
        <div className="camera-section">
          <div 
            className={`magnifier-camera ${isActive ? 'magnifier-active' : ''}`}
            onMouseMove={handleMouseMove}
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
            onClick={measurementMode ? addMeasurement : undefined}
          >
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="magnifier-video"
            />
            
            <canvas ref={canvasRef} style={{ display: 'none' }} />
            
            {isActive && (
              <>
                {showGrid && <div className="magnifier-grid"></div>}
                
                <div 
                  ref={magnifierRef}
                  className="magnifier-lens"
                  style={{
                    left: `${magnifierPosition.x}%`,
                    top: `${magnifierPosition.y}%`,
                    transform: `translate(-50%, -50%) scale(${zoomLevel})`
                  }}
                >
                  <div className="lens-border"></div>
                  <div className="lens-crosshair"></div>
                  <div className="zoom-indicator">{zoomLevel}x</div>
                </div>

                {measurements.map((point) => (
                  <div
                    key={point.id}
                    className="measurement-point"
                    style={{
                      left: `${point.x}%`,
                      top: `${point.y}%`
                    }}
                  >
                    <div className="point-marker"></div>
                    <div className="point-label">{point.label}</div>
                  </div>
                ))}
              </>
            )}

            <div className="magnifier-controls">
              <div className="control-group">
                <button
                  className={`magnifier-toggle ${isActive ? 'active' : ''}`}
                  onClick={toggleMagnifier}
                >
                  {isActive ? '🔍 ON' : '🔎 START'}
                </button>
                
                <button
                  className={`flashlight-btn ${isFlashlightOn ? 'active' : ''}`}
                  onClick={toggleFlashlight}
                  title="Toggle Flashlight"
                >
                  {isFlashlightOn ? '🔦' : '💡'}
                </button>
                
                <button
                  className="capture-btn"
                  onClick={captureImage}
                  title="Capture Image"
                >
                  📸
                </button>
              </div>

              {isActive && (
                <div className="zoom-controls">
                  <button 
                    onClick={() => handleZoomChange(zoomLevel - 0.5)}
                    disabled={zoomLevel <= 1}
                  >
                    -
                  </button>
                  <span className="zoom-display">{zoomLevel}x</span>
                  <button 
                    onClick={() => handleZoomChange(zoomLevel + 0.5)}
                    disabled={zoomLevel >= 10}
                  >
                    +
                  </button>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    step="0.5"
                    value={zoomLevel}
                    onChange={(e) => handleZoomChange(parseFloat(e.target.value))}
                    className="zoom-slider"
                  />
                </div>
              )}
            </div>
          </div>

          <div className="magnifier-options">
            <div className="option-group">
              <label className="option-label">
                <input
                  type="checkbox"
                  checked={showGrid}
                  onChange={(e) => setShowGrid(e.target.checked)}
                />
                <span>Show Grid</span>
              </label>
              
              <label className="option-label">
                <input
                  type="checkbox"
                  checked={measurementMode}
                  onChange={(e) => setMeasurementMode(e.target.checked)}
                />
                <span>Measurement Mode</span>
              </label>
              
              {measurements.length > 0 && (
                <button 
                  className="clear-measurements"
                  onClick={clearMeasurements}
                >
                  Clear Points ({measurements.length})
                </button>
              )}
            </div>
          </div>
        </div>

        <div className="info-panels">
          <div className="features-panel">
            <h3>🛠️ Magnifier Features</h3>
            <div className="features-grid">
              {magnifierFeatures.map((feature, index) => (
                <div key={index} className="feature-card">
                  <div className="feature-icon">{feature.icon}</div>
                  <div className="feature-content">
                    <h4>{feature.title}</h4>
                    <p>{feature.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="inspection-guide">
            <h3>🔍 Security Elements Guide</h3>
            <div className="elements-list">
              {securityElements.map((element, index) => (
                <div key={index} className="element-card">
                  <div className="element-header">
                    <h4>{element.element}</h4>
                    <span className="zoom-badge">{element.zoomLevel}</span>
                  </div>
                  <p className="element-description">{element.description}</p>
                  <div className="element-tip">
                    <strong>💡 Tip:</strong> {element.tip}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {capturedImage && (
            <div className="captured-image-panel">
              <h3>📸 Captured Image</h3>
              <div className="image-preview">
                <img src={capturedImage} alt="Captured magnification" />
                <div className="image-actions">
                  <button 
                    onClick={() => setCapturedImage(null)}
                    className="close-image"
                  >
                    ❌ Close
                  </button>
                  <a 
                    href={capturedImage} 
                    download="magnified-inspection.jpg"
                    className="download-image"
                  >
                    💾 Download
                  </a>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DigitalMagnifier;