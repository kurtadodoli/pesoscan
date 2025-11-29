import React from 'react';

const PesoScanLogo = ({ 
  size = 120, 
  className = '', 
  variant = 'default' // 'default', 'small', 'monochrome'
}) => {
  const isSmall = variant === 'small' || size <= 48;
  const isMonochrome = variant === 'monochrome';
  
  const gradients = isMonochrome ? {
    shield: '#6b7280',
    eye: '#ffffff',
    pupil: '#374151'
  } : {
    shield: 'url(#shieldGradient)',
    eye: 'url(#eyeGradient)',
    pupil: 'url(#pupilGradient)'
  };

  return (
    <svg 
      width={size} 
      height={size} 
      viewBox={`0 0 ${size} ${size}`} 
      className={className}
      xmlns="http://www.w3.org/2000/svg"
    >
      {!isMonochrome && (
        <defs>
          <linearGradient id="shieldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{stopColor:'#6366f1', stopOpacity:1}} />
            <stop offset="50%" style={{stopColor:'#3b82f6', stopOpacity:1}} />
            <stop offset="100%" style={{stopColor:'#1d4ed8', stopOpacity:1}} />
          </linearGradient>
          <linearGradient id="eyeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{stopColor:'#ffffff', stopOpacity:1}} />
            <stop offset="100%" style={{stopColor:'#e2e8f0', stopOpacity:1}} />
          </linearGradient>
          <linearGradient id="pupilGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{stopColor:'#1e293b', stopOpacity:1}} />
            <stop offset="100%" style={{stopColor:'#475569', stopOpacity:1}} />
          </linearGradient>
          <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
            <feDropShadow dx="2" dy="4" stdDeviation="3" floodColor="#000000" floodOpacity="0.2"/>
          </filter>
        </defs>
      )}
      
      {/* Shield Background */}
      <path 
        d={isSmall 
          ? `M${size/2} ${size*0.083} L${size*0.792} ${size*0.208} L${size*0.792} ${size*0.583} Q${size*0.792} ${size*0.708} ${size*0.708} ${size*0.792} Q${size*0.625} ${size*0.875} ${size/2} ${size*0.875} Q${size*0.375} ${size*0.875} ${size*0.292} ${size*0.792} Q${size*0.208} ${size*0.708} ${size*0.208} ${size*0.583} L${size*0.208} ${size*0.208} Z`
          : `M${size/2} ${size*0.083} L${size*0.792} ${size*0.208} L${size*0.792} ${size*0.583} Q${size*0.792} ${size*0.708} ${size*0.708} ${size*0.792} Q${size*0.625} ${size*0.875} ${size/2} ${size*0.875} Q${size*0.375} ${size*0.875} ${size*0.292} ${size*0.792} Q${size*0.208} ${size*0.708} ${size*0.208} ${size*0.583} L${size*0.208} ${size*0.208} Z`
        }
        fill={gradients.shield}
        stroke={isMonochrome ? '#9ca3af' : '#1e40af'}
        strokeWidth={isSmall ? 1 : 2}
        filter={!isMonochrome ? 'url(#shadow)' : undefined}
      />
      
      {/* Letter P with integrated eye */}
      {/* P vertical line */}
      <path 
        d={`M${size*0.333} ${size*0.292} L${size*0.333} ${size*0.708}`}
        fill="none"
        stroke="#ffffff"
        strokeWidth={isSmall ? 2.5 : 6}
        strokeLinecap="round"
      />
      
      {/* P outline */}
      <path 
        d={`M${size*0.333} ${size*0.292} L${size*0.542} ${size*0.292} Q${size*0.625} ${size*0.292} ${size*0.667} ${size*0.35} Q${size*0.708} ${size*0.408} ${size*0.708} ${size*0.475} Q${size*0.708} ${size*0.542} ${size*0.667} ${size*0.6} Q${size*0.625} ${size*0.658} ${size*0.542} ${size*0.658} L${size*0.333} ${size*0.658}`}
        fill="none"
        stroke="#ffffff"
        strokeWidth={isSmall ? 2.5 : 6}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      
      {/* P middle horizontal (partial to make room for eye) */}
      <path 
        d={isSmall 
          ? `M${size*0.333} ${size*0.479} L${size*0.438} ${size*0.479}`
          : `M${size*0.333} ${size*0.475} L${size*0.433} ${size*0.475}`
        }
        fill="none"
        stroke="#ffffff"
        strokeWidth={isSmall ? 2.5 : 6}
        strokeLinecap="round"
      />
      
      {/* Eye integrated inside P's upper section */}
      <ellipse 
        cx={isSmall ? size*0.521 : size*0.517}
        cy={isSmall ? size*0.396 : size*0.392}
        rx={isSmall ? size*0.083 : size*0.083}
        ry={isSmall ? size*0.052 : size*0.058}
        fill={gradients.eye}
        stroke={isMonochrome ? '#d1d5db' : '#cbd5e1'}
        strokeWidth={isSmall ? 0.5 : 1}
      />
      
      {/* Iris */}
      <ellipse 
        cx={isSmall ? size*0.521 : size*0.517}
        cy={isSmall ? size*0.396 : size*0.392}
        rx={isSmall ? size*0.052 : size*0.05}
        ry={isSmall ? size*0.0375 : size*0.0375}
        fill={isMonochrome ? '#6b7280' : '#3b82f6'}
        opacity={isMonochrome ? 1 : 0.9}
      />
      
      {/* Pupil */}
      <ellipse 
        cx={isSmall ? size*0.521 : size*0.517}
        cy={isSmall ? size*0.396 : size*0.392}
        rx={isSmall ? size*0.025 : size*0.025}
        ry={isSmall ? size*0.021 : size*0.021}
        fill={gradients.pupil}
      />
      
      {/* Eye highlight */}
      <ellipse 
        cx={isSmall ? size*0.5 : size*0.5}
        cy={isSmall ? size*0.385 : size*0.375}
        rx={isSmall ? size*0.0104 : size*0.01}
        ry={isSmall ? size*0.0083 : size*0.0083}
        fill="#ffffff"
        opacity={isMonochrome ? 0.6 : 0.8}
      />
      
      {/* Scan lines effect (only for larger sizes) */}
      {!isSmall && (
        <g opacity="0.3">
          <line x1={size*0.433} y1={size*0.367} x2={size*0.6} y2={size*0.367} stroke="#ffffff" strokeWidth="0.5"/>
          <line x1={size*0.433} y1={size*0.392} x2={size*0.6} y2={size*0.392} stroke="#ffffff" strokeWidth="0.5"/>
          <line x1={size*0.433} y1={size*0.417} x2={size*0.6} y2={size*0.417} stroke="#ffffff" strokeWidth="0.5"/>
        </g>
      )}
      
      {/* Corner accents (only for larger sizes) */}
      {!isSmall && (
        <g opacity="0.6">
          <circle cx={size*0.292} cy={size*0.292} r={size*0.017} fill="#ffffff"/>
          <circle cx={size*0.708} cy={size*0.292} r={size*0.017} fill="#ffffff"/>
          <circle cx={size*0.292} cy={size*0.625} r={size*0.017} fill="#ffffff"/>
          <circle cx={size*0.708} cy={size*0.625} r={size*0.017} fill="#ffffff"/>
        </g>
      )}
    </svg>
  );
};

export default PesoScanLogo;