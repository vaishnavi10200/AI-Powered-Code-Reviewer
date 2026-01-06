// DOM ELEMENTS

const codeInput = document.getElementById('code-input');
const languageSelect = document.getElementById('language');
const reviewBtn = document.getElementById('review-btn');
const clearBtn = document.getElementById('clear-btn');

const resultContent = document.getElementById('results-content');
const emptyState = document.getElementById('empty-state');
const loading = document.getElementById('loading');
const analysisResults = document.getElementById('analysis-results');

const scoreValue = document.getElementById('score-value');
const scoreMessage = document.getElementById('score-message');
const scoreCircle = document.getElementById('score-circle');

const issuesContainer = document.getElementById('issues-container');
const aiInsightsContainer = document.getElementById('ai-insights-container');
const securityContainer = document.getElementById('security-container');
const performanceContainer = document.getElementById('performance-container');

// BACKEND API CONFIGURATION

const API_URL = 'http://localhost:5000/review';  // Flask backend

// CLEAR BUTTON FUNCTIONALITY

clearBtn.addEventListener('click', () => {
    // Clear the textarea
    codeInput.value = '';
    
    // Show empty state
    emptyState.style.display = 'flex';
    analysisResults.style.display = 'none';
    loading.style.display = 'none';
    
    // Reset score circle
    if (scoreCircle) {
        scoreCircle.style.background = 'conic-gradient(#00c896 0deg, #00c896 0deg, #2d2d2d 0deg)';
    }
});

// REVIEW BUTTON - MAIN FUNCTIONALITY

reviewBtn.addEventListener('click', async () => {
    const code = codeInput.value.trim();
    const language = languageSelect.value;
    
    // Validation: Check if code is empty
    if (!code) {
        alert('⚠️ Please enter some code to analyze!');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        // Send code to backend API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: code,
                language: language
            })
        });
        
        // Check if request was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse JSON response
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        // Handle errors
        console.error('Error:', error);
        hideLoading();
        alert('❌ Error connecting to backend. Make sure your Flask server is running on http://localhost:5000');
    }
});

// SHOW LOADING STATE

function showLoading() {
    emptyState.style.display = 'none';
    analysisResults.style.display = 'none';
    loading.style.display = 'flex';
}

// HIDE LOADING STATE

function hideLoading() {
    loading.style.display = 'none';
    analysisResults.style.display = 'block';
}

// DISPLAY RESULTS FROM BACKEND

function displayResults(data) {
    hideLoading();
    
    // Update score with animation
    const score = data.score || 0;
    animateScore(score);
    
    // Update score message
    scoreMessage.textContent = getScoreMessage(score);
    
    // Display issues
    displayIssues(data.issues || []);
    
    // Display AI insights
    displayAIInsights(data.ai_review || {});
    
    // Display security analysis
    displaySecurity(data.ai_review || {});
    
    // Display performance tips
    displayPerformance(data.ai_review || {});
}

// ANIMATE SCORE COUNTER

function animateScore(targetScore) {
    const duration = 1000; // 1 second
    const startScore = 0;
    const startTime = performance.now();
    
    function updateScore(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuad = progress * (2 - progress);
        const currentScore = Math.floor(startScore + (targetScore - startScore) * easeOutQuad);
        
        // Update score display
        scoreValue.textContent = currentScore;
        
        // Update circular progress
        const degrees = (currentScore / 100) * 360;
        const color = getScoreColor(currentScore);
        scoreCircle.style.background = `conic-gradient(${color} 0deg, ${color} ${degrees}deg, #2d2d2d ${degrees}deg)`;
        scoreValue.style.color = color;
        
        // Continue animation
        if (progress < 1) {
            requestAnimationFrame(updateScore);
        }
    }
    
    requestAnimationFrame(updateScore);
}

// GET SCORE COLOR BASED ON VALUE

function getScoreColor(score) {
    if (score >= 80) return '#00c896';      // Green - Excellent
    if (score >= 60) return '#ffa116';      // Orange - Good
    if (score >= 40) return '#ff9800';      // Light Orange - Fair
    return '#ef4444';                        // Red - Poor
}

// GET SCORE MESSAGE

function getScoreMessage(score) {
    if (score >= 90) return '🎉 Excellent! Your code follows best practices.';
    if (score >= 75) return '✅ Great! Minor improvements suggested.';
    if (score >= 60) return '👍 Good! Some areas need attention.';
    if (score >= 40) return '⚠️ Fair. Several issues found.';
    return '❌ Poor. Significant improvements needed.';
}

// DISPLAY BASIC ISSUES
function displayIssues(issues) {
    issuesContainer.innerHTML = '';
    
    if (!issues || issues.length === 0) {
        issuesContainer.innerHTML = '<p style="color: #999; font-size: 14px;">No basic issues found! ✨</p>';
        return;
    }
    
    issues.forEach(issue => {
        const card = createIssueCard(
            issue.type || 'warning',
            issue.title || issue.message || 'Issue detected',
            issue.description || issue.message || '',
            issue.line ? `Line ${issue.line}` : null
        );
        issuesContainer.appendChild(card);
    });
}

// DISPLAY AI INSIGHTS

function displayAIInsights(aiReview) {
    aiInsightsContainer.innerHTML = '';
    
    const suggestions = aiReview.suggestions || [];
    
    if (suggestions.length === 0) {
        aiInsightsContainer.innerHTML = '<p style="color: #999; font-size: 14px;">No AI suggestions available.</p>';
        return;
    }
    
    suggestions.forEach(suggestion => {
        const card = createIssueCard(
            'info',
            'AI Suggestion',
            suggestion,
            null
        );
        aiInsightsContainer.appendChild(card);
    });
}

// DISPLAY SECURITY ANALYSIS

function displaySecurity(aiReview) {
    securityContainer.innerHTML = '';
    
    const securityIssues = aiReview.security || [];
    
    if (securityIssues.length === 0) {
        securityContainer.innerHTML = '<p style="color: #00c896; font-size: 14px;">✅ No security issues detected!</p>';
        return;
    }
    
    securityIssues.forEach(issue => {
        const card = createIssueCard(
            'error',
            'Security Issue',
            issue,
            null
        );
        securityContainer.appendChild(card);
    });
}

// DISPLAY PERFORMANCE TIPS

function displayPerformance(aiReview) {
    performanceContainer.innerHTML = '';
    
    const performanceTips = aiReview.performance || [];
    
    if (performanceTips.length === 0) {
        performanceContainer.innerHTML = '<p style="color: #999; font-size: 14px;">No performance optimizations suggested.</p>';
        return;
    }
    
    performanceTips.forEach(tip => {
        const card = createIssueCard(
            'warning',
            'Performance Tip',
            tip,
            null
        );
        performanceContainer.appendChild(card);
    });
}

// CREATE ISSUE CARD ELEMENT

function createIssueCard(type, title, description, lineInfo) {
    const card = document.createElement('div');
    card.className = `issue-card ${type}`;
    
    const header = document.createElement('div');
    header.className = 'issue-header';
    
    const badge = document.createElement('span');
    badge.className = `issue-badge ${type}`;
    badge.textContent = type.toUpperCase();
    
    const titleSpan = document.createElement('span');
    titleSpan.className = 'issue-title';
    titleSpan.textContent = lineInfo ? `${title} (${lineInfo})` : title;
    
    header.appendChild(badge);
    header.appendChild(titleSpan);
    
    const desc = document.createElement('div');
    desc.className = 'issue-description';
    desc.textContent = description;
    
    card.appendChild(header);
    card.appendChild(desc);
    
    return card;
}

// KEYBOARD SHORTCUTS

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to run analysis
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        reviewBtn.click();
    }
    
    // Ctrl/Cmd + K to clear
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        clearBtn.click();
    }
});

// INITIALIZE

console.log('✅ AI Code Reviewer loaded successfully!');
console.log('💡 Tip: Use Ctrl+Enter to analyze code quickly');
console.log('🔗 Backend should be running at:', API_URL);
