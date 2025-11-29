import axios from 'axios';

// Base URL for the backend API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for image processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.message || error.response.data?.detail || 'Server error occurred';
      throw new Error(message);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error - unable to connect to server');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred');
    }
  }
);

/**
 * Scan image using camera capture
 * @param {Blob} imageBlob - The captured image blob
 * @returns {Promise<Object>} - Analysis result
 */
export const scanImage = async (imageBlob) => {
  const formData = new FormData();
  formData.append('file', imageBlob, 'capture.jpg');
  
  const response = await api.post('/api/scan', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Upload and analyze image file
 * @param {File} imageFile - The uploaded image file
 * @returns {Promise<Object>} - Analysis result
 */
export const uploadImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Get scan history
 * @param {number} limit - Number of records to retrieve
 * @param {number} offset - Offset for pagination
 * @returns {Promise<Object>} - History data
 */
export const getScanHistory = async (limit = 20, offset = 0) => {
  const response = await api.get('/api/history', {
    params: { limit, offset }
  });
  
  return response.data;
};

/**
 * Get specific scan result by ID
 * @param {string} scanId - The scan ID
 * @returns {Promise<Object>} - Scan result
 */
export const getScanById = async (scanId) => {
  const response = await api.get(`/api/scans/${scanId}`);
  return response.data;
};

/**
 * Delete scan from history
 * @param {string} scanId - The scan ID to delete
 * @returns {Promise<Object>} - Deletion result
 */
export const deleteScan = async (scanId) => {
  const response = await api.delete(`/api/scans/${scanId}`);
  return response.data;
};

/**
 * Get system health status
 * @returns {Promise<Object>} - Health status
 */
export const getHealthStatus = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

/**
 * Get system statistics
 * @returns {Promise<Object>} - System stats
 */
export const getSystemStats = async () => {
  const response = await api.get('/api/stats');
  return response.data;
};

/**
 * Analyze image for counterfeit features
 * @param {File|Blob} imageFile - The image to analyze
 * @returns {Promise<Object>} - Counterfeit analysis result
 */
export const analyzeCounterfeit = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await api.post('/api/analyze-counterfeit', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Get counterfeit detection model status
 * @returns {Promise<Object>} - Model status
 */
export const getCounterfeitModelStatus = async () => {
  const response = await api.get('/api/counterfeit-model-status');
  return response.data;
};

/**
 * Comprehensive scan combining peso detection and counterfeit analysis
 * @param {File|Blob} imageFile - The image to analyze
 * @returns {Promise<Object>} - Comprehensive analysis result
 */
export const comprehensiveScan = async (imageFile, options = {}) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  const params = {};
  if (options.dataset && options.dataset !== 'auto') {
    params.dataset = options.dataset;
  }
  
  try {
    const response = await api.post('/api/comprehensive-scan', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 45000, // Increased timeout for comprehensive analysis
      params
    });
    
    return response.data;
  } catch (error) {
    // Enhanced error handling for comprehensive scan
    if (error.message.includes('timeout')) {
      throw new Error('Analysis is taking longer than expected. Please try with a smaller image or check your connection.');
    }
    throw error;
  }
};

// Mock data for development (when backend is not available)
export const mockScanResult = {
  id: 'mock-' + Date.now(),
  timestamp: new Date().toISOString(),
  result: {
    authentic: Math.random() > 0.3, // 70% chance of authentic
    confidence: Math.random() * 30 + 70, // 70-100% confidence
    denomination: ['20', '50', '100', '200', '500', '1000'][Math.floor(Math.random() * 6)],
    detection: {
      bbox: [0.2, 0.2, 0.8, 0.8], // [x1, y1, x2, y2] normalized coordinates
      confidence: Math.random() * 20 + 80 // 80-100% detection confidence
    },
    features: {
      security_thread: Math.random() > 0.2,
      watermark: Math.random() > 0.3,
      microprinting: Math.random() > 0.4,
      color_changing_ink: Math.random() > 0.3
    }
  },
  processing_time: Math.random() * 2 + 0.5 // 0.5-2.5 seconds
};

/**
 * Development mode scan (uses mock data)
 * @param {File|Blob} image - Image to scan
 * @returns {Promise<Object>} - Mock scan result
 */
export const mockScan = async (image) => {
  // Simulate processing delay
  await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));
  
  // Random chance of error for testing
  if (Math.random() < 0.1) {
    throw new Error('Unable to detect peso bill in image');
  }
  
  return mockScanResult;
};

export default api;
export { api };