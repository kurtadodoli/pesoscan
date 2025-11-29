import React, { useState, useRef, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Webcam from 'react-webcam';
import { comprehensiveScan } from '../services/api';
import './ScanPage.css';

const ScanPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  const [mode, setMode] = useState(searchParams.get('mode') || 'camera');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [capturedImage, setCapturedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [facingMode, setFacingMode] = useState('environment');
  
  const webcamRef = useRef(null);
  const fileInputRef = useRef(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
    setPreviewUrl(imageSrc);
  }, [webcamRef]);

  const toggleCamera = () => {
    setFacingMode(prevMode => prevMode === 'environment' ? 'user' : 'environment');
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      setError('');
    }
  };

  const handleScan = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      let result;
      let imageFile;
      
      if (mode === 'camera' && capturedImage) {
        const response = await fetch(capturedImage);
        imageFile = await response.blob();
      } else if (mode === 'upload' && uploadedFile) {
        imageFile = uploadedFile;
      } else {
        throw new Error('No image selected');
      }
      
      // Use comprehensive scan for better counterfeit detection
      result = await comprehensiveScan(imageFile);
      
      navigate('/results', { 
        state: { 
          result, 
          imageUrl: previewUrl,
          mode,
          scanType: 'comprehensive'
        } 
      });
    } catch (err) {
      setError(err.message || 'Failed to process image');
    } finally {
      setIsLoading(false);
    }
  };

  const resetCapture = () => {
    setCapturedImage(null);
    setUploadedFile(null);
    setPreviewUrl('');
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="scan-page">
      <div className="container">
        <div className="scan-header">
          <h1>Scan Peso Banknote</h1>
          <p>Choose your scanning method below</p>
        </div>

        <div className="mode-selector">
          <button
            className={`mode-btn ${mode === 'camera' ? 'active' : ''}`}
            onClick={() => {
              setMode('camera');
              resetCapture();
            }}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" fill="none"/>
              <circle cx="12" cy="13" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
            </svg>
            Camera Scan
          </button>
          
          <button
            className={`mode-btn ${mode === 'upload' ? 'active' : ''}`}
            onClick={() => {
              setMode('upload');
              resetCapture();
            }}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" strokeWidth="2" fill="none"/>
              <polyline points="17 8 12 3 7 8" stroke="currentColor" strokeWidth="2" fill="none"/>
              <line x1="12" y1="3" x2="12" y2="15" stroke="currentColor" strokeWidth="2"/>
            </svg>
            Upload Image
          </button>
        </div>

        <div className="scan-content">
          
          {mode === 'camera' ? (
            <div className="camera-section">
              {!capturedImage ? (
                <div className="webcam-container">
                  <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    videoConstraints={{
                      width: 640,
                      height: 480,
                      facingMode: facingMode
                    }}
                    className="webcam"
                  />
                  <div className="camera-overlay">
                    <button 
                      className="camera-flip-btn" 
                      onClick={toggleCamera}
                      title="Switch camera"
                      aria-label="Switch between front and back camera"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                        <circle cx="12" cy="13" r="4"/>
                        <path d="M17 8 L20 8 M20 8 L20 11 M20 8 L17 11"/>
                      </svg>
                    </button>
                    <div className="viewfinder">
                      <div className="corner top-left"></div>
                      <div className="corner top-right"></div>
                      <div className="corner bottom-left"></div>
                      <div className="corner bottom-right"></div>
                    </div>
                    <p className="camera-instruction">Position the peso banknote within the frame</p>
                  </div>
                </div>
              ) : (
                <div className="preview-container">
                  <img src={capturedImage} alt="Captured" className="preview-image" />
                </div>
              )}
              
              <div className="camera-controls">
                {!capturedImage ? (
                  <button onClick={capture} className="btn btn-primary btn-large">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                      <circle cx="12" cy="12" r="3" fill="currentColor"/>
                    </svg>
                    Capture Photo
                  </button>
                ) : (
                  <div className="captured-controls">
                    <button onClick={resetCapture} className="btn btn-outline">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <polyline points="1,4 1,10 7,10" stroke="currentColor" strokeWidth="2" fill="none"/>
                        <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" stroke="currentColor" strokeWidth="2" fill="none"/>
                      </svg>
                      Retake
                    </button>
                    <button 
                      onClick={handleScan} 
                      className="btn btn-primary btn-large"
                      disabled={isLoading}
                    >
                      {isLoading ? (
                        <>
                          <div className="spinner"></div>
                          Processing...
                        </>
                      ) : (
                        <>
                          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 12l2 2 4-4" stroke="currentColor" strokeWidth="2"/>
                            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                          </svg>
                          Analyze Banknote
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="upload-section">
              <div className="upload-area" onClick={() => fileInputRef.current?.click()}>
                {!uploadedFile ? (
                  <div className="upload-placeholder">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2" fill="none"/>
                      <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2" fill="none"/>
                      <line x1="12" y1="18" x2="12" y2="12" stroke="currentColor" strokeWidth="2"/>
                      <line x1="9" y1="15" x2="12" y2="12" stroke="currentColor" strokeWidth="2"/>
                      <line x1="15" y1="15" x2="12" y2="12" stroke="currentColor" strokeWidth="2"/>
                    </svg>
                    <h3>Upload Image</h3>
                    <p>Click to select or drag and drop an image</p>
                    <p className="file-types">Supports: JPG, PNG, JPEG</p>
                  </div>
                ) : (
                  <div className="upload-preview">
                    <img src={previewUrl} alt="Uploaded" className="preview-image" />
                    <div className="upload-info">
                      <p className="file-name">{uploadedFile.name}</p>
                      <p className="file-size">{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                    </div>
                  </div>
                )}
              </div>
              
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                className="file-input"
                hidden
              />
              
              {uploadedFile && (
                <div className="upload-controls">
                  <button onClick={resetCapture} className="btn btn-outline">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <polyline points="3,6 5,6 21,6" stroke="currentColor" strokeWidth="2" fill="none"/>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke="currentColor" strokeWidth="2" fill="none"/>
                    </svg>
                    Remove
                  </button>
                  <button 
                    onClick={handleScan} 
                    className="btn btn-primary btn-large"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <div className="spinner"></div>
                        Processing...
                      </>
                    ) : (
                      <>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2" fill="none"/>
                          <path d="M21 21l-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
                        </svg>
                        Analyze Banknote
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          )}


        </div>

        {error && (
          <div className="error-message">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
              <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" strokeWidth="2"/>
              <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" strokeWidth="2"/>
            </svg>
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default ScanPage;