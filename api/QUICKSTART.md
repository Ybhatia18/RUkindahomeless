# 🚀 Flask API Quick Start Guide

## Installation

```bash
cd api/
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## Testing the API

### Option 1: Use the test script
```bash
# In a new terminal (while server is running)
python test_api.py
```

### Option 2: Use curl commands

```bash
# Health check
curl http://localhost:5000/api/health

# Get all listings
curl http://localhost:5000/api/listings

# Get 2BR apartments under $2500
curl "http://localhost:5000/api/listings?bedrooms=2&max_rent=2500"

# Get statistics
curl http://localhost:5000/api/stats

# Get top 5 best deals
curl "http://localhost:5000/api/best-deals?limit=5"

# Predict rent (POST request)
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"bedrooms": 2, "bathrooms": 1, "sqft": 900}'

# Predict with value classification
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"bedrooms": 2, "bathrooms": 2, "sqft": 1100, "rent": 2000}'

# Get data sources
curl http://localhost:5000/api/sources
```

### Option 3: Use browser

Visit these URLs in your browser:
- http://localhost:5000/api/health
- http://localhost:5000/api/listings
- http://localhost:5000/api/stats
- http://localhost:5000/api/best-deals
- http://localhost:5000/api/sources

## Example Responses

### GET /api/stats
```json
{
  "success": true,
  "overall": {
    "total_listings": 60,
    "avg_rent": 2400.50,
    "min_rent": 1059.00,
    "max_rent": 3950.00,
    "avg_sqft": 865.33
  },
  "by_bedrooms": [
    {
      "bedrooms": 1,
      "count": 25,
      "avg_rent": 2100.00,
      "min_rent": 1500.00,
      "max_rent": 3000.00
    }
  ],
  "by_source": [
    {
      "source": "craigslist",
      "count": 35,
      "avg_rent": 2000.00
    }
  ]
}
```

### POST /api/predict
```json
{
  "success": true,
  "predicted_rent": 2150.75,
  "value_category": "Fair Price",
  "inputs": {
    "bedrooms": 2,
    "bathrooms": 1,
    "sqft": 900
  }
}
```

## Troubleshooting

**Port already in use?**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in app.py:
app.run(debug=True, port=5001)
```

**Database connection error?**
- Make sure PostgreSQL is running
- Verify database name: `rukindahomeless`
- Check username/password in app.py

**Models not loading?**
- Run the ML training scripts first:
```bash
cd ../models/
python predict_rent.py
python value_classifier.py
```

## Next Steps

This API is ready to connect to a React frontend!

Example React fetch:
```javascript
// Get all listings
fetch('http://localhost:5000/api/listings')
  .then(res => res.json())
  .then(data => console.log(data.listings));

// Predict rent
fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    bedrooms: 2,
    bathrooms: 1,
    sqft: 900
  })
})
  .then(res => res.json())
  .then(data => console.log('Predicted rent:', data.predicted_rent));
```
