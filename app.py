"""
Flask web API for Prediction Engine
Deploy to Railway.app or any cloud platform
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import json
from datetime import datetime
from typing import Dict, List, Any
import os

from prediction_engine import PredictionEngine
from prediction_engine.business_predictors import (
    OfferPerformancePredictor,
    EmailCreativePredictor,
    GoogleAdsCampaignPredictor
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global storage for trained models and data
trained_models = {}
historical_data = {
    'offers': [],
    'email_creatives': [],
    'campaigns': []
}

# Global prediction engine
engine = PredictionEngine()


@app.route('/')
def home():
    """Home endpoint with API information."""
    return jsonify({
        'message': 'Prediction Engine API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/offers/train': 'Train offer performance predictor',
            'POST /api/offers/predict': 'Predict offer performance',
            'POST /api/offers/top': 'Get top N offers',
            'POST /api/email/train': 'Train email creative predictor',
            'POST /api/email/predict': 'Predict email creative performance',
            'POST /api/campaigns/train': 'Train ad campaign predictor',
            'POST /api/campaigns/predict': 'Predict campaign performance',
            'GET /api/models/status': 'Get status of trained models',
            'POST /api/offers/upload': 'Upload historical offer data',
            'POST /api/email/upload': 'Upload historical email data',
            'POST /api/campaigns/upload': 'Upload historical campaign data',
        }
    })


@app.route('/api/models/status', methods=['GET'])
def get_model_status():
    """Get status of all trained models."""
    return jsonify({
        'trained_models': list(trained_models.keys()),
        'data_counts': {
            'offers': len(historical_data['offers']),
            'email_creatives': len(historical_data['email_creatives']),
            'campaigns': len(historical_data['campaigns'])
        }
    })


# ============================================================================
# OFFER PREDICTIONS
# ============================================================================

@app.route('/api/offers/upload', methods=['POST'])
def upload_offer_data():
    """Upload historical offer data (CSV or JSON)."""
    try:
        if 'file' in request.files:
            # Handle file upload (CSV expected)
            file = request.files['file']
            if file.filename.endswith('.csv'):
                import pandas as pd
                import io
                df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
                # Convert DataFrame to list of dicts
                data = df.to_dict('records')
                historical_data['offers'].extend(data)
            else:
                return jsonify({'error': 'File must be CSV format'}), 400
        else:
            # Handle JSON data
            data = request.json.get('data', [])
            if not isinstance(data, list):
                return jsonify({'error': 'Data must be a list of offer objects'}), 400
            historical_data['offers'].extend(data)
        
        return jsonify({
            'message': 'Data uploaded successfully',
            'total_records': len(historical_data['offers'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/offers/train', methods=['POST'])
def train_offer_model():
    """Train the offer performance predictor."""
    try:
        # Get data from request or use uploaded data
        data = request.json.get('data', historical_data['offers'])
        performance_scores = request.json.get('performance_scores', [])
        
        if not data or not performance_scores:
            return jsonify({'error': 'Data and performance_scores are required'}), 400
        
        if len(data) != len(performance_scores):
            return jsonify({'error': 'Data and performance_scores must have same length'}), 400
        
        # Extract dates if available
        dates = None
        if 'dates' in request.json:
            dates = [datetime.fromisoformat(d) if isinstance(d, str) else d for d in request.json['dates']]
        elif data and 'date' in data[0]:
            dates = [item.get('date') for item in data]
            dates = [datetime.fromisoformat(d) if isinstance(d, str) else datetime.fromtimestamp(d) if isinstance(d, (int, float)) else d for d in dates]
            dates = np.array(dates)
        
        # Create and train predictor
        model_type = request.json.get('model_type', 'random_forest')
        predictor = OfferPerformancePredictor(model_type=model_type)
        predictor.train(data, np.array(performance_scores), dates=dates)
        
        # Store model
        trained_models['offers'] = predictor
        engine.add_predictor(predictor, name='offers')
        
        # Evaluate on training data
        metrics = predictor.evaluate(data, np.array(performance_scores), dates=dates)
        
        return jsonify({
            'message': 'Model trained successfully',
            'metrics': {k: float(v) for k, v in metrics.items()},
            'training_samples': len(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/offers/predict', methods=['POST'])
def predict_offers():
    """Predict performance for offers."""
    try:
        if 'offers' not in trained_models:
            return jsonify({'error': 'Model not trained. Please train the model first.'}), 400
        
        offers = request.json.get('offers', [])
        if not offers:
            return jsonify({'error': 'Offers data is required'}), 400
        
        # Extract dates if available
        dates = None
        if 'dates' in request.json:
            dates = [datetime.fromisoformat(d) if isinstance(d, str) else d for d in request.json['dates']]
            dates = np.array(dates)
        elif offers and 'date' in offers[0]:
            dates = [item.get('date') for item in offers]
            dates = [datetime.fromisoformat(d) if isinstance(d, str) else datetime.fromtimestamp(d) if isinstance(d, (int, float)) else datetime.now() for d in dates]
            dates = np.array(dates)
        
        predictor = trained_models['offers']
        predictions = predictor.predict(offers, dates=dates)
        
        # Return predictions with offer data
        results = []
        for i, offer in enumerate(offers):
            result = offer.copy()
            result['predicted_score'] = float(predictions[i])
            results.append(result)
        
        return jsonify({
            'predictions': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/offers/top', methods=['POST'])
def get_top_offers():
    """Get top N performing offers."""
    try:
        if 'offers' not in trained_models:
            return jsonify({'error': 'Model not trained. Please train the model first.'}), 400
        
        offers = request.json.get('offers', [])
        top_n = request.json.get('top_n', 10)
        
        if not offers:
            return jsonify({'error': 'Offers data is required'}), 400
        
        # Extract dates if available
        dates = None
        if 'dates' in request.json:
            dates = [datetime.fromisoformat(d) if isinstance(d, str) else d for d in request.json['dates']]
            dates = np.array(dates)
        elif offers and 'date' in offers[0]:
            dates = [item.get('date') for item in offers]
            dates = [datetime.fromisoformat(d) if isinstance(d, str) else datetime.fromtimestamp(d) if isinstance(d, (int, float)) else datetime.now() for d in dates]
            dates = np.array(dates)
        
        predictor = trained_models['offers']
        top_offers = predictor.predict_top_offers(offers, dates=dates, top_n=top_n)
        
        return jsonify({
            'top_offers': top_offers,
            'count': len(top_offers)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# EMAIL CREATIVE PREDICTIONS
# ============================================================================

@app.route('/api/email/upload', methods=['POST'])
def upload_email_data():
    """Upload historical email creative data."""
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.csv'):
                import pandas as pd
                import io
                df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
                data = df.to_dict('records')
                historical_data['email_creatives'].extend(data)
            else:
                return jsonify({'error': 'File must be CSV format'}), 400
        else:
            data = request.json.get('data', [])
            if not isinstance(data, list):
                return jsonify({'error': 'Data must be a list of email creative objects'}), 400
            historical_data['email_creatives'].extend(data)
        
        return jsonify({
            'message': 'Data uploaded successfully',
            'total_records': len(historical_data['email_creatives'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/email/train', methods=['POST'])
def train_email_model():
    """Train the email creative predictor."""
    try:
        data = request.json.get('data', historical_data['email_creatives'])
        performance_scores = request.json.get('performance_scores', [])
        
        if not data or not performance_scores:
            return jsonify({'error': 'Data and performance_scores are required'}), 400
        
        if len(data) != len(performance_scores):
            return jsonify({'error': 'Data and performance_scores must have same length'}), 400
        
        model_type = request.json.get('model_type', 'gradient_boosting')
        predictor = EmailCreativePredictor(model_type=model_type)
        predictor.train(data, np.array(performance_scores))
        
        trained_models['email'] = predictor
        engine.add_predictor(predictor, name='email')
        
        metrics = predictor.evaluate(data, np.array(performance_scores))
        
        return jsonify({
            'message': 'Model trained successfully',
            'metrics': {k: float(v) for k, v in metrics.items()},
            'training_samples': len(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/email/predict', methods=['POST'])
def predict_email():
    """Predict performance for email creatives."""
    try:
        if 'email' not in trained_models:
            return jsonify({'error': 'Model not trained. Please train the model first.'}), 400
        
        creatives = request.json.get('creatives', [])
        if not creatives:
            return jsonify({'error': 'Creatives data is required'}), 400
        
        predictor = trained_models['email']
        predictions = predictor.predict(creatives)
        
        results = []
        for i, creative in enumerate(creatives):
            result = creative.copy()
            result['predicted_score'] = float(predictions[i])
            results.append(result)
        
        return jsonify({
            'predictions': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# CAMPAIGN PREDICTIONS
# ============================================================================

@app.route('/api/campaigns/upload', methods=['POST'])
def upload_campaign_data():
    """Upload historical campaign data."""
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.csv'):
                import pandas as pd
                import io
                df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
                data = df.to_dict('records')
                historical_data['campaigns'].extend(data)
            else:
                return jsonify({'error': 'File must be CSV format'}), 400
        else:
            data = request.json.get('data', [])
            if not isinstance(data, list):
                return jsonify({'error': 'Data must be a list of campaign objects'}), 400
            historical_data['campaigns'].extend(data)
        
        return jsonify({
            'message': 'Data uploaded successfully',
            'total_records': len(historical_data['campaigns'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/campaigns/train', methods=['POST'])
def train_campaign_model():
    """Train the ad campaign predictor."""
    try:
        data = request.json.get('data', historical_data['campaigns'])
        performance_scores = request.json.get('performance_scores', [])
        
        if not data or not performance_scores:
            return jsonify({'error': 'Data and performance_scores are required'}), 400
        
        if len(data) != len(performance_scores):
            return jsonify({'error': 'Data and performance_scores must have same length'}), 400
        
        model_type = request.json.get('model_type', 'random_forest')
        predictor = GoogleAdsCampaignPredictor(model_type=model_type)
        predictor.train(data, np.array(performance_scores))
        
        trained_models['campaigns'] = predictor
        engine.add_predictor(predictor, name='campaigns')
        
        metrics = predictor.evaluate(data, np.array(performance_scores))
        
        return jsonify({
            'message': 'Model trained successfully',
            'metrics': {k: float(v) for k, v in metrics.items()},
            'training_samples': len(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/campaigns/predict', methods=['POST'])
def predict_campaigns():
    """Predict performance for ad campaigns."""
    try:
        if 'campaigns' not in trained_models:
            return jsonify({'error': 'Model not trained. Please train the model first.'}), 400
        
        campaigns = request.json.get('campaigns', [])
        if not campaigns:
            return jsonify({'error': 'Campaigns data is required'}), 400
        
        predictor = trained_models['campaigns']
        predictions = predictor.predict(campaigns)
        
        results = []
        for i, campaign in enumerate(campaigns):
            result = campaign.copy()
            result['predicted_score'] = float(predictions[i])
            results.append(result)
        
        return jsonify({
            'predictions': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

