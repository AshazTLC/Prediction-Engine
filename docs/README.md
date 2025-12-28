# Prediction Engine Frontend

A simple, clean web interface for the Offer Prediction Engine.

## 🚀 Quick Start

### Option 1: Open Directly in Browser (Simplest)

1. **Double-click** `index.html` to open it in your default browser

That's it! The frontend will connect to the API at `https://thelewadsconenterprises.com`

### Option 2: Run with a Local Server (Recommended)

For best results, use a local web server:

#### Using Python:

```bash
# Python 3
cd frontend
python3 -m http.server 8000

# Then open: http://localhost:8000
```

#### Using Node.js (http-server):

```bash
# Install http-server globally (one time)
npm install -g http-server

# Run server
cd frontend
http-server -p 8000

# Then open: http://localhost:8000
```

#### Using VS Code Live Server:

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## 📁 Files

- `index.html` - Main HTML structure
- `styles.css` - All styling
- `script.js` - JavaScript functionality
- `README.md` - This file

## 🎯 Features

- ✅ Clean, modern design
- ✅ Loading states with spinner
- ✅ Error handling with user-friendly messages
- ✅ Animated results display
- ✅ Responsive design (works on mobile)
- ✅ No dependencies (pure HTML/CSS/JS)

## 🔧 Configuration

If you need to change the API endpoint, edit `script.js`:

```javascript
const API_BASE_URL = 'https://thelewadsconenterprises.com';
```

## 📱 How It Works

1. Click the "Predict Offers" button
2. The frontend sends a POST request to `/api/offers/predict`
3. Results are displayed in cards:
   - Predicted Clicks
   - Predicted Conversions
   - Predicted Revenue (formatted as currency)
   - Confidence (as percentage)
   - Based on Records

## 🎨 Customization

### Change Colors

Edit `styles.css` and modify the gradient:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change API Endpoint

Edit `script.js`:

```javascript
const API_BASE_URL = 'https://your-api-url.com';
```

## 🐛 Troubleshooting

### CORS Errors

If you see CORS errors, make sure your backend has CORS enabled. The Flask backend should include:

```python
from flask_cors import CORS
CORS(app)
```

### API Not Responding

1. Check that the API URL is correct in `script.js`
2. Verify the backend is running and accessible
3. Check browser console for detailed error messages

### Results Not Showing

1. Check browser console (F12) for errors
2. Verify the API response format matches expected format
3. Ensure all required fields are present in API response

## 📊 API Response Format

The API should return JSON like:

```json
{
  "predicted_clicks": 530,
  "predicted_conversions": 47,
  "predicted_revenue": 1155,
  "confidence": 0.7,
  "based_on_records": 2
}
```

## 🚀 Deployment

### Deploy to GitHub Pages

1. Push the `frontend` folder to GitHub
2. Go to repository Settings → Pages
3. Select branch and folder
4. Your site will be live at `https://username.github.io/repo-name`

### Deploy to Netlify

1. Drag and drop the `frontend` folder to Netlify
2. Your site will be live instantly

### Deploy to Vercel

```bash
cd frontend
vercel
```

## 📝 Notes

- This is a client-side only application (no backend needed for frontend)
- All API calls are made directly from the browser
- No authentication or API keys required
- Works with any static file hosting

## 🎉 That's It!

Open `index.html` and start making predictions!

