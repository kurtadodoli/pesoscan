import React from 'react';

const Logo = ({ size = 'medium', color = 'primary', animated = false }) => {
  const dimensions = {
    small: { width: 32, height: 32 },
    medium: { width: 48, height: 48 },
    large: { width: 64, height: 64 },
    xl: { width: 96, height: 96 }
  };

  const colors = {
    primary: '#1a365d',
    teal: '#319795',
    white: '#ffffff',
    accent: '#4299e1'
  };

  const { width, height } = dimensions[size];
  const fillColor = colors[color];
  const accentColor = colors.accent;

  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 80 80"
      xmlns="http://www.w3.org/2000/svg"
      className={`logo ${animated ? 'logo-animated' : ''}`}
    >
      {/* Gradient definitions */}
      <defs>
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor={fillColor} />
          <stop offset="100%" stopColor={accentColor} />
        </linearGradient>
        <linearGradient id="eyeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor={accentColor} />
          <stop offset="100%" stopColor={fillColor} />
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      {/* Modern hexagonal background */}
      <polygon
        points="40,8 64,24 64,56 40,72 16,56 16,24"
        fill="url(#logoGradient)"
        fillOpacity="0.1"
        stroke="url(#logoGradient)"
        strokeWidth="2"
        filter="url(#glow)"
      />
      
      {/* Inner hexagon for depth */}
      <polygon
        points="40,16 56,28 56,52 40,64 24,52 24,28"
        fill="none"
        stroke={fillColor}
        strokeWidth="1"
        opacity="0.3"
        strokeDasharray="3,2"
      />
      
      {/* Enhanced Peso symbol (₱) */}
      <g transform="translate(20, 20)">
        {/* P shape with modern styling */}
        <path
          d="M8 12 L8 32 M8 12 L20 12 Q26 12 26 18 Q26 24 20 24 L8 24"
          stroke="url(#logoGradient)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
          filter="url(#glow)"
        />
        
        {/* Horizontal lines for peso symbol with gradient */}
        <line
          x1="5"
          y1="16"
          x2="18"
          y2="16"
          stroke="url(#logoGradient)"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <line
          x1="5"
          y1="20"
          x2="18"
          y2="20"
          stroke="url(#logoGradient)"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </g>
      
      {/* Enhanced Eye symbol with scanning effect */}
      <g transform="translate(42, 42)">
        {/* Outer eye shape */}
        <ellipse
          cx="12"
          cy="8"
          rx="14"
          ry="8"
          fill="none"
          stroke="url(#eyeGradient)"
          strokeWidth="2.5"
          filter="url(#glow)"
        />
        
        {/* Inner iris */}
        <circle
          cx="12"
          cy="8"
          r="5"
          fill="url(#eyeGradient)"
          opacity="0.8"
        />
        
        {/* Pupil */}
        <circle
          cx="12"
          cy="8"
          r="2.5"
          fill={fillColor}
        />
        
        {/* Highlight */}
        <circle
          cx="13.5"
          cy="6.5"
          r="1"
          fill={color === 'white' ? fillColor : 'white'}
          opacity="0.9"
        />
        
        {/* Scanning beam effect */}
        <line
          x1="0"
          y1="8"
          x2="24"
          y2="8"
          stroke={accentColor}
          strokeWidth="1"
          opacity="0.6"
          strokeDasharray="2,4"
        >
          {animated && (
            <animate
              attributeName="stroke-dashoffset"
              values="0;-6;0"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </line>
      </g>
      
      {/* Modern scanning grid pattern */}
      <g opacity="0.4">
        <line
          x1="12"
          y1="40"
          x2="68"
          y2="40"
          stroke={accentColor}
          strokeWidth="0.5"
          strokeDasharray="2,3"
        />
        <line
          x1="16"
          y1="35"
          x2="64"
          y2="35"
          stroke={accentColor}
          strokeWidth="0.5"
          strokeDasharray="2,3"
        />
        <line
          x1="16"
          y1="45"
          x2="64"
          y2="45"
          stroke={accentColor}
          strokeWidth="0.5"
          strokeDasharray="2,3"
        />
        
        {/* Vertical scanning lines */}
        <line
          x1="30"
          y1="20"
          x2="30"
          y2="60"
          stroke={accentColor}
          strokeWidth="0.5"
          strokeDasharray="1,4"
          opacity="0.6"
        />
        <line
          x1="50"
          y1="20"
          x2="50"
          y2="60"
          stroke={accentColor}
          strokeWidth="0.5"
          strokeDasharray="1,4"
          opacity="0.6"
        />
      </g>
      
      {/* Corner accent marks */}
      <g stroke={accentColor} strokeWidth="2" strokeLinecap="round" opacity="0.7">
        <path d="M15,15 L15,20 L20,20" fill="none" />
        <path d="M65,15 L65,20 L60,20" fill="none" />
        <path d="M15,65 L15,60 L20,60" fill="none" />
        <path d="M65,65 L65,60 L60,60" fill="none" />
      </g>
    </svg>
  );
};

export default Logo;