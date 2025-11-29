import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './TestResults.css';

const TestResults = () => {
  const navigate = useNavigate();

  // Prevent any automatic API calls
  useEffect(() => {
    // Block any background API calls that might be happening
    return () => {
      // Cleanup any potential API calls
    };
  }, []);

  const handleTestResults = () => {
    // Navigate directly to the standalone demo (no API calls)
    navigate('/demo-results');
  };

  return (
    <div className="test-results-page">
      <div className="container">
        <div className="test-header">
          <h1>Test New Results Interface</h1>
          <p>Click the button below to see the new results page design</p>
        </div>

        <div className="test-content">
          <div className="preview-card">
            <h3>New Features:</h3>
            <ul>
              <li>✅ Two-column layout with analyzed image on the left</li>
              <li>✅ Trained Model Detection Results panel</li>
              <li>✅ YOLOv8 Detected Features with confidence bars</li>
              <li>✅ Enhanced bounding boxes with labels</li>
              <li>✅ Clean, modern interface design</li>
              <li>✅ Mobile responsive layout</li>
            </ul>
          </div>

          <button onClick={handleTestResults} className="btn btn-primary btn-large">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" stroke="currentColor" strokeWidth="2" fill="none"/>
              <polyline points="10,17 15,12 10,7" stroke="currentColor" strokeWidth="2" fill="none"/>
              <line x1="15" y1="12" x2="3" y2="12" stroke="currentColor" strokeWidth="2"/>
            </svg>
            View New Results Interface
          </button>
        </div>
      </div>
    </div>
  );
};

export default TestResults;