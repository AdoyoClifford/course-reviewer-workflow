// Global variables
let currentFile = null;
let currentSession = null;

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFile = document.getElementById('removeFile');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadSection = document.querySelector('.upload-section');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    // File upload event listeners
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    
    fileInput.addEventListener('change', handleFileSelect);
    removeFile.addEventListener('click', handleRemoveFile);
    analyzeBtn.addEventListener('click', handleAnalyze);
    
    // Browse link
    document.querySelector('.browse-link').addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    const allowedTypes = ['text/plain', 'text/markdown', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const allowedExtensions = ['txt', 'md', 'doc', 'docx'];
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
        showNotification('Please upload a valid text file (.txt, .md, .doc, .docx)', 'error');
        return;
    }
    
    // Check file size (limit to 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showNotification('File size must be less than 10MB', 'error');
        return;
    }
    
    currentFile = file;
    displayFileInfo(file);
    analyzeBtn.disabled = false;
}

function displayFileInfo(file) {
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    uploadArea.style.display = 'none';
}

function handleRemoveFile() {
    currentFile = null;
    fileInfo.style.display = 'none';
    uploadArea.style.display = 'block';
    analyzeBtn.disabled = true;
    fileInput.value = '';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function handleAnalyze() {
    if (!currentFile) {
        showNotification('Please select a file first', 'error');
        return;
    }
    
    try {
        // Show loading screen
        showLoadingScreen();
        
        // Read file content
        const fileContent = await readFileContent(currentFile);
        
        // Create a session
        const sessionResponse = await fetch('/api/create-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!sessionResponse.ok) {
            throw new Error('Failed to create session');
        }
        
        const sessionData = await sessionResponse.json();
        if (!sessionData.success) {
            throw new Error(sessionData.error || 'Failed to create session');
        }
        
        // Simulate the analysis steps for UI feedback
        const analysisPromise = simulateAnalysisSteps();
        
        // Call the actual Course Reviewer API
        const analysisResponse = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionData.session_id,
                content: fileContent
            })
        });
        
        // Wait for both analysis and UI simulation to complete
        await analysisPromise;
        
        if (!analysisResponse.ok) {
            throw new Error(`Analysis failed: ${analysisResponse.status}`);
        }
        
        const analysisData = await analysisResponse.json();
        if (!analysisData.success) {
            throw new Error(analysisData.error || 'Analysis failed');
        }
        
        // Show results
        displayResults(analysisData.results);
        
    } catch (error) {
        console.error('Analysis error:', error);
        showNotification(`Analysis failed: ${error.message}`, 'error');
        hideLoadingScreen();
    }
}

function readFileContent(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);
        reader.readAsText(file);
    });
}

async function simulateAnalysisSteps() {
    const steps = ['step1', 'step2', 'step3'];
    
    for (let i = 0; i < steps.length; i++) {
        // Activate current step
        document.getElementById(steps[i]).classList.add('active');
        
        // Wait for demonstration
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Deactivate current step (except the last one)
        if (i < steps.length - 1) {
            document.getElementById(steps[i]).classList.remove('active');
        }
    }
}

function showLoadingScreen() {
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    // Reset progress steps
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });
}

function hideLoadingScreen() {
    loadingSection.style.display = 'none';
    uploadSection.style.display = 'block';
}

function displayResults(results) {
    // Hide loading and show results
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Update status badge
    const statusBadge = document.getElementById('statusBadge');
    const statusText = document.getElementById('statusText');
    
    if (results.passed) {
        statusBadge.className = 'status-badge passed';
        statusText.textContent = 'Passed';
    } else {
        statusBadge.className = 'status-badge failed';
        statusText.textContent = 'Failed';
    }
    
    // Update scores
    document.getElementById('finalScore').textContent = results.final_score.toFixed(1);
    document.getElementById('courseCategory').textContent = results.category;
    document.getElementById('passStatus').textContent = results.passed ? 'PASSED' : 'FAILED';
    document.getElementById('passStatus').className = results.passed ? 'value status-pass' : 'value status-fail';
    
    // Update individual scores
    displayIndividualScores(results.individual_scores, results.category_weights);
    
    // Update feedback
    document.getElementById('summaryText').textContent = results.summary;
    document.getElementById('recommendationText').textContent = results.recommendation;
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayIndividualScores(scores, weights) {
    const scoresGrid = document.getElementById('scoresGrid');
    scoresGrid.innerHTML = '';
    
    Object.entries(scores).forEach(([element, score]) => {
        const weight = weights[element] || 0;
        const scoreBar = createScoreBar(element, score, weight);
        scoresGrid.appendChild(scoreBar);
    });
}

function createScoreBar(title, score, weight) {
    const scoreBar = document.createElement('div');
    scoreBar.className = 'score-bar';
    
    scoreBar.innerHTML = `
        <div class="score-bar-header">
            <span class="score-bar-title">${title}</span>
            <span class="score-bar-value">${score}/100</span>
        </div>
        <div class="score-bar-progress">
            <div class="score-bar-fill" style="width: ${score}%"></div>
        </div>
        <div style="font-size: 0.8rem; color: #718096; margin-top: 0.3rem;">
            Weight: ${weight}%
        </div>
    `;
    
    return scoreBar;
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#fed7d7' : '#bee3f8'};
        color: ${type === 'error' ? '#9b2c2c' : '#2a69ac'};
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);