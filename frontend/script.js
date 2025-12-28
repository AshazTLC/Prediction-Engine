// API Configuration
const API_BASE_URL = 'https://thelewadsconenterprises.com';
const PREDICT_ENDPOINT = `${API_BASE_URL}/api/offers/predict`;

// DOM Elements
const predictBtn = document.getElementById('predictBtn');
const buttonText = document.getElementById('buttonText');
const buttonLoader = document.getElementById('buttonLoader');
const errorMessage = document.getElementById('errorMessage');
const results = document.getElementById('results');

// Result elements
const predictedClicks = document.getElementById('predictedClicks');
const predictedConversions = document.getElementById('predictedConversions');
const predictedRevenue = document.getElementById('predictedRevenue');
const confidence = document.getElementById('confidence');
const basedOnRecords = document.getElementById('basedOnRecords');

/**
 * Format number with commas
 */
function formatNumber(num) {
    if (typeof num !== 'number') return num;
    return num.toLocaleString('en-US');
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    if (typeof amount !== 'number') return amount;
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(amount);
}

/**
 * Format percentage
 */
function formatPercentage(value) {
    if (typeof value !== 'number') return value;
    return `${(value * 100).toFixed(0)}%`;
}

/**
 * Show loading state
 */
function setLoading(loading) {
    predictBtn.disabled = loading;
    buttonText.style.display = loading ? 'none' : 'inline';
    buttonLoader.style.display = loading ? 'inline-block' : 'none';
    errorMessage.style.display = 'none';
    
    if (!loading) {
        results.style.display = 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    results.style.display = 'none';
}

/**
 * Display prediction results
 */
function displayResults(data) {
    // Update result values
    predictedClicks.textContent = formatNumber(data.predicted_clicks || 0);
    predictedConversions.textContent = formatNumber(data.predicted_conversions || 0);
    predictedRevenue.textContent = formatCurrency(data.predicted_revenue || 0);
    confidence.textContent = formatPercentage(data.confidence || 0);
    basedOnRecords.textContent = formatNumber(data.based_on_records || 0);
    
    // Show results with animation
    results.style.display = 'block';
    
    // Add success animation to result cards
    const resultCards = document.querySelectorAll('.result-card');
    resultCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('success');
            setTimeout(() => card.classList.remove('success'), 600);
        }, index * 100);
    });
}

/**
 * Make prediction API call
 */
async function predictOffers() {
    setLoading(true);
    
    try {
        const response = await fetch(PREDICT_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // Note: The API might not require a body, but we'll send an empty object
            // If your API requires specific data, add it here
            body: JSON.stringify({}),
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
                errorData.error || errorData.message || 
                `HTTP error! status: ${response.status}`
            );
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Prediction error:', error);
        
        // User-friendly error messages
        let errorMsg = 'Failed to get predictions. ';
        
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMsg += 'Please check your internet connection and try again.';
        } else if (error.message.includes('404')) {
            errorMsg += 'The prediction endpoint was not found.';
        } else if (error.message.includes('500')) {
            errorMsg += 'The server encountered an error. Please try again later.';
        } else {
            errorMsg += error.message;
        }
        
        showError(errorMsg);
    } finally {
        setLoading(false);
    }
}

// Optional: Add keyboard shortcut (Enter key)
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !predictBtn.disabled) {
        predictOffers();
    }
});

// Check API connection on load
window.addEventListener('load', () => {
    console.log('Prediction Engine Frontend loaded');
    console.log('API Endpoint:', PREDICT_ENDPOINT);
});

