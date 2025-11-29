import React, { useState, useRef, useEffect } from 'react';
import './Magnifier.css';

const Magnifier = ({ 
  imageUrl, 
  magnificationLevel = 2, 
  magnifierSize = 150,
  isActive = false,
  onToggle 
}) => {
  const [isHovering, setIsHovering] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [imageSize, setImageSize] = useState({ width: 0, height: 0 });
  const imageRef = useRef(null);
  const magnifierRef = useRef(null);

  useEffect(() => {
    const updateImageSize = () => {
      if (imageRef.current) {
        const rect = imageRef.current.getBoundingClientRect();
        setImageSize({
          width: rect.width,
          height: rect.height
        });
      }
    };

    updateImageSize();
    window.addEventListener('resize', updateImageSize);
    return () => window.removeEventListener('resize', updateImageSize);
  }, [imageUrl]);

  const handleMouseMove = (e) => {
    if (!isActive) return;

    const rect = imageRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setMousePosition({ x, y });
  };

  const handleMouseEnter = () => {
    if (isActive) setIsHovering(true);
  };

  const handleMouseLeave = () => {
    setIsHovering(false);
  };

  if (!imageUrl) return null;

  return (
    <div className="magnifier-container">
      <div className="magnifier-controls">
        <button 
          className={`magnifier-toggle ${isActive ? 'active' : ''}`}
          onClick={onToggle}
          title="Toggle Magnifier"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2" fill="none"/>
            <path d="M21 21l-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
            <line x1="11" y1="8" x2="11" y2="14" stroke="currentColor" strokeWidth="2"/>
            <line x1="8" y1="11" x2="14" y2="11" stroke="currentColor" strokeWidth="2"/>
          </svg>
          {isActive ? 'Disable Magnifier' : 'Enable Magnifier'}
        </button>
        
        {isActive && (
          <div className="magnifier-info">
            <span className="magnifier-level">
              {magnificationLevel}x Zoom
            </span>
            <small>Hover over the bill to magnify details</small>
          </div>
        )}
      </div>

      <div 
        className={`magnifier-image-container ${isActive ? 'magnifier-enabled' : ''}`}
        onMouseMove={handleMouseMove}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <img
          ref={imageRef}
          src={imageUrl}
          alt="Philippine Peso Bill"
          className="magnifier-target-image"
        />
        
        {isActive && isHovering && (
          <>
            {/* Crosshair */}
            <div 
              className="magnifier-crosshair"
              style={{
                left: mousePosition.x,
                top: mousePosition.y,
                transform: 'translate(-50%, -50%)'
              }}
            />
            
            {/* Magnifier lens */}
            <div
              ref={magnifierRef}
              className="magnifier-lens"
              style={{
                width: magnifierSize,
                height: magnifierSize,
                left: mousePosition.x + 20,
                top: mousePosition.y - magnifierSize / 2,
                backgroundImage: `url(${imageUrl})`,
                backgroundSize: `${imageSize.width * magnificationLevel}px ${imageSize.height * magnificationLevel}px`,
                backgroundPosition: `${-mousePosition.x * magnificationLevel + magnifierSize / 2}px ${-mousePosition.y * magnificationLevel + magnifierSize / 2}px`,
                transform: mousePosition.x > imageSize.width - magnifierSize - 40 
                  ? 'translateX(-100%) translateX(-40px)' 
                  : 'none'
              }}
            >
              <div className="magnifier-overlay">
                <div className="magnifier-details">
                  <div className="zoom-indicator">{magnificationLevel}x</div>
                  <div className="security-hints">
                    <div className="hint-item">🔍 Look for watermarks</div>
                    <div className="hint-item">💎 Check security thread</div>
                    <div className="hint-item">🌟 Examine microprint</div>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {isActive && (
        <div className="magnifier-guide">
          <h4>🔍 Magnification Guide</h4>
          <div className="guide-grid">
            <div className="guide-item">
              <div className="guide-icon">💧</div>
              <div>
                <strong>Watermarks</strong>
                <p>Look for translucent designs visible when held to light</p>
              </div>
            </div>
            <div className="guide-item">
              <div className="guide-icon">🧵</div>
              <div>
                <strong>Security Thread</strong>
                <p>Embedded strip with microtext running through the bill</p>
              </div>
            </div>
            <div className="guide-item">
              <div className="guide-icon">📝</div>
              <div>
                <strong>Microprint</strong>
                <p>Tiny text that's difficult to reproduce clearly</p>
              </div>
            </div>
            <div className="guide-item">
              <div className="guide-icon">🎨</div>
              <div>
                <strong>Intaglio Printing</strong>
                <p>Raised ink texture that can be felt by touch</p>
              </div>
            </div>
            <div className="guide-item">
              <div className="guide-icon">🌈</div>
              <div>
                <strong>Color-Changing Ink</strong>
                <p>Optically variable ink that shifts colors</p>
              </div>
            </div>
            <div className="guide-item">
              <div className="guide-icon">🔢</div>
              <div>
                <strong>Serial Numbers</strong>
                <p>Unique identifiers with specific fonts and spacing</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Magnifier;