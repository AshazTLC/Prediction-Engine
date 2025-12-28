# ⚡ Quick Start Guide

## Run the Frontend (Choose One Method)

### Method 1: Double-Click (Easiest)
1. Navigate to the `frontend` folder
2. Double-click `index.html`
3. Done! The page opens in your browser

### Method 2: Python Server (Recommended)
```bash
cd frontend
python3 -m http.server 8000
# Open: http://localhost:8000
```

### Method 3: VS Code Live Server
1. Install "Live Server" extension
2. Right-click `index.html` → "Open with Live Server"

## 🎯 How to Use

1. **Click "Predict Offers" button**
2. **Wait for results** (loading spinner shows)
3. **View predictions** displayed in cards:
   - Predicted Clicks
   - Predicted Conversions  
   - Predicted Revenue ($)
   - Confidence (%)
   - Based on Records

## 🔧 If You Need to Change API URL

Edit `script.js`, line 2:
```javascript
const API_BASE_URL = 'https://your-new-url.com';
```

## ✅ That's It!

The frontend connects to: `https://thelewadsconenterprises.com/api/offers/predict`

No setup needed - just open and use!

