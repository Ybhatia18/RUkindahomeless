"""
RUKindaHomeless - API Test Script
Tests all API endpoints to ensure they're working
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

print("=" * 70)
print("RUKINDAHOMELESS API TEST SUITE")
print("=" * 70)
print("\nMake sure the Flask server is running first!")
print("Run: python app.py\n")

def test_endpoint(name, method, endpoint, data=None, params=None):
    """Helper function to test an endpoint"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")
    
    try:
        url = BASE_URL + endpoint
        
        if method == 'GET':
            response = requests.get(url, params=params)
        elif method == 'POST':
            response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS")
            print(f"\nResponse Preview:")
            print(json.dumps(result, indent=2)[:500] + "...")
        else:
            print("❌ FAILED")
            print(f"Error: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ ERROR: {e}")

# Run tests
print("\n🧪 Starting API Tests...\n")

# Test 1: Health Check
test_endpoint(
    "Health Check",
    "GET",
    "/health"
)

# Test 2: Get All Listings
test_endpoint(
    "Get All Listings",
    "GET",
    "/listings"
)

# Test 3: Get Listings with Filters
test_endpoint(
    "Get 2BR Listings under $2500",
    "GET",
    "/listings",
    params={'bedrooms': 2, 'max_rent': 2500}
)

# Test 4: Get Statistics
test_endpoint(
    "Get Statistics",
    "GET",
    "/stats"
)

# Test 5: Get Best Deals
test_endpoint(
    "Get Top 5 Best Deals",
    "GET",
    "/best-deals",
    params={'limit': 5}
)

# Test 6: Predict Rent
test_endpoint(
    "Predict Rent for 2BR/1BA/900sqft",
    "POST",
    "/predict",
    data={
        'bedrooms': 2,
        'bathrooms': 1,
        'sqft': 900
    }
)

# Test 7: Predict with Value Classification
test_endpoint(
    "Predict with Value Classification",
    "POST",
    "/predict",
    data={
        'bedrooms': 2,
        'bathrooms': 2,
        'sqft': 1100,
        'rent': 2000
    }
)

# Test 8: Get Sources
test_endpoint(
    "Get Data Sources",
    "GET",
    "/sources"
)

print("\n" + "=" * 70)
print("API TESTING COMPLETE!")
print("=" * 70)
print("\nIf all tests passed, your API is ready for the React frontend!")
print()
