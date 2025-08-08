import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [enableOcr, setEnableOcr] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState('');
  const [fileName, setFileName] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [modalMessage, setModalMessage] = useState('');

  // Function to show custom modal
  const showModal = (message) => {
    setModalMessage(message);
    setModalVisible(true);
  };

  const closeModal = () => {
    setModalVisible(false);
    setModalMessage('');
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setFileName(`Selected file: ${file.name}`);
      setStatusMessage('');
      setDownloadUrl(''); // Clear previous download link
    } else {
      setSelectedFile(null);
      setFileName('Please select a PDF file.');
      showModal('Please upload a valid PDF file.');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.target.classList.remove('border-indigo-500', 'bg-indigo-50'); // Unhighlight
    const file = e.dataTransfer.files[0];
    handleFileChange({ target: { files: [file] } });
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.target.classList.add('border-indigo-500', 'bg-indigo-50'); // Highlight
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.target.classList.remove('border-indigo-500', 'bg-indigo-50'); // Unhighlight
  };

  const handleConvert = async () => {
    if (!selectedFile) {
      showModal('No PDF file selected. Please upload a PDF to convert.');
      return;
    }

    setIsLoading(true);
    setStatusMessage('Processing your PDF... This might take a moment.');
    setDownloadUrl(''); // Hide download link during processing

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('enable_ocr', enableOcr); // Pass boolean as string or number if backend expects it differently

    try {
      const response = await axios.post('http://localhost:8000/convert', formData, {
        responseType: 'blob', // Important for receiving binary data (the .docx file)
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
      setStatusMessage('Conversion complete! Your Word document is ready.');
      setFileName(selectedFile.name.replace('.pdf', '.docx')); // Update file name for download
    } catch (error) {
      console.error('Conversion failed:', error);
      setStatusMessage('Conversion failed. Please try again.');
      if (error.response && error.response.data) {
        // Attempt to read error message from blob response
        const reader = new FileReader();
        reader.onload = function() {
          try {
            const errorData = JSON.parse(reader.result);
            showModal(`Error: ${errorData.detail || 'An unknown error occurred.'}`);
          } catch (parseError) {
            showModal('An error occurred during conversion. Please try again later.');
          }
        };
        reader.readAsText(error.response.data);
      } else {
        showModal('An error occurred during conversion. Please try again later.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gray-100">
      <div className="container bg-white p-8 rounded-xl shadow-lg flex flex-col items-center max-w-2xl w-full">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">PDF to Word Converter</h1>

        {/* File Upload Area */}
        <div
          id="drop-area"
          className="w-full p-12 text-center rounded-xl cursor-pointer mb-6 border-2 border-dashed border-gray-300 hover:border-indigo-500 hover:bg-indigo-50 transition-all duration-300"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <input type="file" id="fileInput" accept=".pdf" className="hidden" onChange={handleFileChange} />
          <p className="text-gray-600 text-lg mb-2">Drag & Drop your PDF here, or</p>
          <button
            onClick={() => document.getElementById('fileInput').click()}
            className="bg-indigo-500 text-white px-6 py-3 rounded-lg shadow-md hover:bg-indigo-600 transition-colors"
          >
            Browse Files
          </button>
          <p className="mt-4 text-gray-700 text-sm">{fileName}</p>
        </div>

        {/* OCR Option */}
        <div className="flex items-center mb-6">
          <input
            type="checkbox"
            id="ocrCheckbox"
            className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
            checked={enableOcr}
            onChange={(e) => setEnableOcr(e.target.checked)}
          />
          <label htmlFor="ocrCheckbox" className="ml-2 text-gray-700 text-lg">
            Enable OCR (Optical Character Recognition)
          </label>
        </div>

        {/* Convert Button */}
        <button
          onClick={handleConvert}
          className={`btn-primary text-white px-8 py-4 rounded-xl shadow-lg text-xl font-semibold flex items-center justify-center gap-2 ${
            !selectedFile || isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-indigo-700'
          }`}
          disabled={!selectedFile || isLoading}
        >
          {isLoading ? (
            <>
              <div className="loader border-t-white"></div> {/* Assuming loader style from CSS */}
              <span>Converting...</span>
            </>
          ) : (
            <span>Convert to Word</span>
          )}
        </button>

        {/* Status/Result Area */}
        {statusMessage && (
          <div className="mt-8 text-center text-lg text-gray-700">
            {statusMessage}
          </div>
        )}
        {downloadUrl && (
          <div className="mt-4">
            <a
              href={downloadUrl}
              download={fileName}
              className="bg-green-500 text-white px-6 py-3 rounded-lg shadow-md hover:bg-green-600 transition-colors"
            >
              Download Word Document
            </a>
          </div>
        )}
      </div>

      {/* Custom Modal for Messages */}
      {modalVisible && (
        <div className="modal">
          <div className="modal-content">
            <span className="close-button" onClick={closeModal}>&times;</span>
            <p className="text-lg text-gray-800">{modalMessage}</p>
            <button onClick={closeModal} className="bg-indigo-500 text-white px-6 py-3 rounded-lg mt-4">OK</button>
          </div>
        </div>
      )}

      {/* Global styles for loader and modal (can be moved to index.css) */}
      <style jsx>{`
        .loader {
            border: 4px solid #f3f3f3; /* Light grey */
            border-top: 4px solid #4f46e5; /* Blue */
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .modal {
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.4);
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background-color: #fefefe;
            padding: 20px;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            width: 90%;
            max-width: 500px;
            text-align: center;
        }
        .close-button {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .close-button:hover,
        .close-button:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
      `}</style>
    </div>
  );
}

export default App;
