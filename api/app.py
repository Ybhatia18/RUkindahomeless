"""
RUKindaHomeless - Flask API Backend
Provides REST endpoints for apartment listings, predictions, and statistics
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Database connection helper
def get_db_connection():
    return psycopg2.connect(
        dbname="rukindahomeless",
        user="yakshbha",
        password="",
        host="localhost"
    )

# Load ML models
print("Loading ML models...")
try:
    with open('../models/rent_predictor.pkl', 'rb') as f:
        rent_predictor = pickle.load(f)
    with open('../models/value_classifier.pkl', 'rb') as f:
        value_classifier = pickle.load(f)
    print("✅ Models loaded successfully")
except FileNotFoundError:
    print("⚠️  Warning: ML models not found. Run the model training scripts first.")
    rent_predictor = None
    value_classifier = None

# ============================================================================
# ENDPOINT 1: Get All Listings
# ============================================================================
@app.route('/api/listings', methods=['GET'])
def get_listings():
    """
    Get all listings with optional filters
    Query params: bedrooms, min_rent, max_rent, source
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Base query
        query = """
            SELECT l.listing_id, l.address, l.monthly_rent, l.bedrooms, 
                   l.bathrooms, l.square_feet, l.source, l.listing_url,
                   s.price_per_sqft, s.value_score
            FROM listings l
            LEFT JOIN listing_stats s ON l.listing_id = s.listing_id
            WHERE 1=1
        """
        params = []
        
        # Apply filters from query parameters
        if request.args.get('bedrooms'):
            query += " AND l.bedrooms = %s"
            params.append(int(request.args.get('bedrooms')))
        
        if request.args.get('min_rent'):
            query += " AND l.monthly_rent >= %s"
            params.append(float(request.args.get('min_rent')))
        
        if request.args.get('max_rent'):
            query += " AND l.monthly_rent <= %s"
            params.append(float(request.args.get('max_rent')))
        
        if request.args.get('source'):
            query += " AND l.source = %s"
            params.append(request.args.get('source'))
        
        query += " ORDER BY l.monthly_rent"
        
        cursor.execute(query, params)
        listings = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for listing in listings:
            result.append({
                'listing_id': listing[0],
                'address': listing[1],
                'monthly_rent': float(listing[2]),
                'bedrooms': listing[3],
                'bathrooms': float(listing[4]),
                'square_feet': listing[5],
                'source': listing[6],
                'listing_url': listing[7],
                'price_per_sqft': float(listing[8]) if listing[8] else None,
                'value_score': float(listing[9]) if listing[9] else None
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(result),
            'listings': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# ENDPOINT 2: Get Statistics
# ============================================================================
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get summary statistics for all listings
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Overall stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_listings,
                ROUND(AVG(monthly_rent), 2) as avg_rent,
                ROUND(MIN(monthly_rent), 2) as min_rent,
                ROUND(MAX(monthly_rent), 2) as max_rent,
                ROUND(AVG(square_feet), 2) as avg_sqft
            FROM listings
        """)
        overall = cursor.fetchone()
        
        # Stats by bedroom count
        cursor.execute("""
            SELECT bedrooms, COUNT(*) as count, 
                   ROUND(AVG(monthly_rent), 2) as avg_rent,
                   ROUND(MIN(monthly_rent), 2) as min_rent,
                   ROUND(MAX(monthly_rent), 2) as max_rent
            FROM listings
            GROUP BY bedrooms
            ORDER BY bedrooms
        """)
        by_bedrooms = cursor.fetchall()
        
        # Stats by source
        cursor.execute("""
            SELECT source, COUNT(*) as count,
                   ROUND(AVG(monthly_rent), 2) as avg_rent
            FROM listings
            GROUP BY source
            ORDER BY count DESC
        """)
        by_source = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'overall': {
                'total_listings': overall[0],
                'avg_rent': float(overall[1]),
                'min_rent': float(overall[2]),
                'max_rent': float(overall[3]),
                'avg_sqft': float(overall[4])
            },
            'by_bedrooms': [
                {
                    'bedrooms': row[0],
                    'count': row[1],
                    'avg_rent': float(row[2]),
                    'min_rent': float(row[3]),
                    'max_rent': float(row[4])
                } for row in by_bedrooms
            ],
            'by_source': [
                {
                    'source': row[0],
                    'count': row[1],
                    'avg_rent': float(row[2])
                } for row in by_source
            ]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# ENDPOINT 3: Get Best Deals
# ============================================================================
@app.route('/api/best-deals', methods=['GET'])
def get_best_deals():
    """
    Get top listings with best value scores
    Query params: limit (default 10)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        limit = int(request.args.get('limit', 10))
        
        cursor.execute("""
            SELECT l.listing_id, l.address, l.monthly_rent, l.bedrooms,
                   l.bathrooms, l.square_feet, l.source, l.listing_url,
                   s.price_per_sqft, s.value_score
            FROM listings l
            JOIN listing_stats s ON l.listing_id = s.listing_id
            WHERE s.value_score >= 7.0
            ORDER BY s.value_score DESC
            LIMIT %s
        """, (limit,))
        
        deals = cursor.fetchall()
        
        result = []
        for deal in deals:
            result.append({
                'listing_id': deal[0],
                'address': deal[1],
                'monthly_rent': float(deal[2]),
                'bedrooms': deal[3],
                'bathrooms': float(deal[4]),
                'square_feet': deal[5],
                'source': deal[6],
                'listing_url': deal[7],
                'price_per_sqft': float(deal[8]),
                'value_score': float(deal[9])
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(result),
            'best_deals': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# ENDPOINT 4: Predict Rent
# ============================================================================
@app.route('/api/predict', methods=['POST'])
def predict_rent():
    """
    Predict rent for given apartment features
    POST body: { "bedrooms": 2, "bathrooms": 1, "sqft": 900 }
    """
    try:
        if rent_predictor is None:
            return jsonify({
                'success': False,
                'error': 'Rent prediction model not loaded'
            }), 500
        
        data = request.get_json()
        
        # Validate input
        required_fields = ['bedrooms', 'bathrooms', 'sqft']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Make prediction
        features = [[
            int(data['bedrooms']),
            float(data['bathrooms']),
            int(data['sqft'])
        ]]
        
        predicted_rent = rent_predictor.predict(features)[0]
        
        # Also classify value if rent is provided
        value_category = None
        if 'rent' in data and value_classifier is not None:
            actual_rent = float(data['rent'])
            price_per_sqft = actual_rent / int(data['sqft'])
            
            features_with_price = [[
                int(data['bedrooms']),
                float(data['bathrooms']),
                int(data['sqft']),
                price_per_sqft
            ]]
            
            value_category = value_classifier.predict(features_with_price)[0]
        
        return jsonify({
            'success': True,
            'predicted_rent': round(float(predicted_rent), 2),
            'value_category': value_category,
            'inputs': {
                'bedrooms': int(data['bedrooms']),
                'bathrooms': float(data['bathrooms']),
                'sqft': int(data['sqft'])
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# ENDPOINT 5: Get Sources
# ============================================================================
@app.route('/api/sources', methods=['GET'])
def get_sources():
    """
    Get list of all data sources
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT source, COUNT(*) as count
            FROM listings
            GROUP BY source
            ORDER BY source
        """)
        
        sources = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'sources': [
                {
                    'name': row[0],
                    'count': row[1]
                } for row in sources
            ]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Health Check
# ============================================================================
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({
        'success': True,
        'message': 'RUKindaHomeless API is running!',
        'models_loaded': {
            'rent_predictor': rent_predictor is not None,
            'value_classifier': value_classifier is not None
        }
    })

# ============================================================================
# Run Server
# ============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🏠 RUKindaHomeless API Server")
    print("=" * 70)
    print("\nAvailable endpoints:")
    print("   GET  /api/health         - Health check")
    print("   GET  /api/listings       - Get all listings (with filters)")
    print("   GET  /api/stats          - Get summary statistics")
    print("   GET  /api/best-deals     - Get best value listings")
    print("   POST /api/predict        - Predict rent for apartment")
    print("   GET  /api/sources        - Get data sources")
    print("\nServer running on http://localhost:5000")
    print("=" * 70 + "\n")
    
    app.run(debug=True, port=5000)
