import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './HistoryPage.css';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'authentic', 'counterfeit'
  const [sortBy, setSortBy] = useState('newest'); // 'newest', 'oldest', 'confidence'

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = () => {
    try {
      const savedHistory = JSON.parse(localStorage.getItem('pesoscan_history') || '[]');
      setHistory(savedHistory);
    } catch (error) {
      console.error('Error loading history:', error);
      setHistory([]);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteHistoryItem = (id) => {
    if (window.confirm('Are you sure you want to delete this scan record?')) {
      const updatedHistory = history.filter(item => item.id !== id);
      setHistory(updatedHistory);
      localStorage.setItem('pesoscan_history', JSON.stringify(updatedHistory));
    }
  };

  const clearAllHistory = () => {
    if (window.confirm('Are you sure you want to clear all scan history? This action cannot be undone.')) {
      setHistory([]);
      localStorage.removeItem('pesoscan_history');
    }
  };

  const exportHistory = () => {
    const dataStr = JSON.stringify(history, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `pesoscan-history-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  // Filter and sort history
  const filteredHistory = history
    .filter(item => {
      if (filter === 'all') return true;
      return filter === 'authentic' ? item.result.authentic : !item.result.authentic;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'oldest':
          return new Date(a.timestamp) - new Date(b.timestamp);
        case 'confidence':
          return (b.result.confidence || 0) - (a.result.confidence || 0);
        case 'newest':
        default:
          return new Date(b.timestamp) - new Date(a.timestamp);
      }
    });

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-PH', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <div className="history-page">
        <div className="container">
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading scan history...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <div className="container">
        <div className="history-header">
          <h1>Scan History</h1>
          <p>View and manage your previous peso bill scans</p>
        </div>

        {history.length > 0 ? (
          <>
            <div className="history-controls">
              <div className="filters">
                <label>
                  Filter:
                  <select value={filter} onChange={(e) => setFilter(e.target.value)}>
                    <option value="all">All Scans</option>
                    <option value="authentic">Authentic Only</option>
                    <option value="counterfeit">Counterfeit Only</option>
                  </select>
                </label>

                <label>
                  Sort by:
                  <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                    <option value="newest">Newest First</option>
                    <option value="oldest">Oldest First</option>
                    <option value="confidence">Highest Confidence</option>
                  </select>
                </label>
              </div>

              <div className="actions">
                <button onClick={exportHistory} className="btn btn-outline">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <polyline points="7,10 12,15 17,10" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" strokeWidth="2"/>
                  </svg>
                  Export
                </button>
                
                <button onClick={clearAllHistory} className="btn btn-outline danger">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <polyline points="3,6 5,6 21,6" stroke="currentColor" strokeWidth="2" fill="none"/>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke="currentColor" strokeWidth="2" fill="none"/>
                  </svg>
                  Clear All
                </button>
              </div>
            </div>

            <div className="history-stats">
              <div className="stat-card">
                <span className="stat-number">{history.length}</span>
                <span className="stat-label">Total Scans</span>
              </div>
              <div className="stat-card">
                <span className="stat-number">
                  {history.filter(item => item.result.authentic).length}
                </span>
                <span className="stat-label">Authentic</span>
              </div>
              <div className="stat-card">
                <span className="stat-number">
                  {history.filter(item => !item.result.authentic).length}
                </span>
                <span className="stat-label">Counterfeit</span>
              </div>
              <div className="stat-card">
                <span className="stat-number">
                  {history.length > 0 
                    ? Math.round(history.reduce((acc, item) => acc + (item.result.confidence || 0), 0) / history.length)
                    : 0}%
                </span>
                <span className="stat-label">Avg. Confidence</span>
              </div>
            </div>

            <div className="history-list">
              {filteredHistory.map((item) => (
                <div key={item.id} className="history-item">
                  <div className="item-image">
                    <img src={item.imageUrl} alt="Scanned bill" />
                  </div>
                  
                  <div className="item-details">
                    <div className="item-header">
                      <span className={`result-badge ${item.result.authentic ? 'authentic' : 'counterfeit'}`}>
                        {item.result.authentic ? '✓ Authentic' : '✗ Counterfeit'}
                      </span>
                      <span className="scan-date">{formatDate(item.timestamp)}</span>
                    </div>
                    
                    <div className="item-info">
                      <div className="info-row">
                        <span className="label">Confidence:</span>
                        <span className="value">{Math.round(item.result.confidence || 0)}%</span>
                      </div>
                      
                      {item.result.denomination && (
                        <div className="info-row">
                          <span className="label">Denomination:</span>
                          <span className="value">₱{item.result.denomination}</span>
                        </div>
                      )}
                      
                      <div className="info-row">
                        <span className="label">Method:</span>
                        <span className="value">{item.mode === 'camera' ? 'Camera' : 'Upload'}</span>
                      </div>
                      
                      {item.processingTime && (
                        <div className="info-row">
                          <span className="label">Processing:</span>
                          <span className="value">{item.processingTime.toFixed(2)}s</span>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="item-actions">
                    <button
                      onClick={() => deleteHistoryItem(item.id)}
                      className="btn btn-outline danger small"
                      title="Delete this record"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <polyline points="3,6 5,6 21,6" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke="currentColor" strokeWidth="2" fill="none"/>
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="empty-state">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
              <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke="currentColor" strokeWidth="2" fill="none"/>
              <line x1="9" y1="9" x2="9.01" y2="9" stroke="currentColor" strokeWidth="2"/>
              <line x1="15" y1="9" x2="15.01" y2="9" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <h3>No Scan History</h3>
            <p>You haven't performed any peso bill scans yet.</p>
            <Link to="/scan" className="btn btn-primary">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
                <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
              </svg>
              Start Scanning
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;