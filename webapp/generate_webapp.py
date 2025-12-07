"""
RUKindaHomeless - Web App Generator
Generates a complete HTML web application with all listings from CSV
"""

import pandas as pd
import json

print("=" * 70)
print("RUKINDAHOMELESS - WEB APP GENERATOR")
print("=" * 70)

# Load CSV data
print("\n📂 Loading data from CSV...")
df = pd.read_csv('../data/listings.csv')

# Clean rent column
df['rent'] = df['rent'].astype(str).str.replace(',', '').astype(float)

print(f"✅ Loaded {len(df)} listings")

# Convert to list of dictionaries
listings = []
for _, row in df.iterrows():
    listing = {
        'address': str(row['address']),
        'rent': float(row['rent']),
        'bedrooms': int(row['BR']),
        'bathrooms': float(row['Ba']),
        'sqft': int(row['sqft']),
        'url': str(row['url']),
        'source': str(row['source']).strip()
    }
    listings.append(listing)

# Convert to JavaScript array
listings_js = json.dumps(listings, indent=2)

print(f"✅ Converted {len(listings)} listings to JavaScript format")

# HTML template
html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RUKindaHomeless - Apartment Finder</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}

        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .stat-card h3 {{
            color: #667eea;
            font-size: 2em;
            margin-bottom: 5px;
        }}

        .stat-card p {{
            color: #666;
            font-size: 0.9em;
        }}

        .filters {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .filters h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}

        .filter-group {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }}

        .filter-group label {{
            display: block;
            color: #666;
            margin-bottom: 5px;
            font-weight: 600;
        }}

        .filter-group select,
        .filter-group input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
        }}

        .filter-group select:focus,
        .filter-group input:focus {{
            outline: none;
            border-color: #667eea;
        }}

        button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
        }}

        button:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .listings {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}

        .listing-card {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s;
        }}

        .listing-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}

        .listing-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
        }}

        .listing-price {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .listing-address {{
            font-size: 0.9em;
            opacity: 0.9;
        }}

        .listing-details {{
            padding: 20px;
        }}

        .listing-detail-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }}

        .listing-detail-row:last-child {{
            border-bottom: none;
        }}

        .detail-label {{
            color: #666;
            font-weight: 600;
        }}

        .detail-value {{
            color: #333;
        }}

        .value-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-top: 10px;
        }}

        .great-deal {{
            background: #4caf50;
            color: white;
        }}

        .fair-price {{
            background: #2196f3;
            color: white;
        }}

        .overpriced {{
            background: #ff9800;
            color: white;
        }}

        .listing-link {{
            display: block;
            text-align: center;
            padding: 15px;
            background: #f5f5f5;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: background 0.3s;
        }}

        .listing-link:hover {{
            background: #667eea;
            color: white;
        }}

        .no-results {{
            text-align: center;
            padding: 60px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .no-results h2 {{
            color: #667eea;
            margin-bottom: 10px;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8em;
            }}

            .listings {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏠 RUKindaHomeless</h1>
            <p class="subtitle">Find Your Perfect Apartment in New Brunswick, NJ</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <h3 id="totalListings">0</h3>
                <p>Total Listings</p>
            </div>
            <div class="stat-card">
                <h3 id="avgRent">$0</h3>
                <p>Average Rent</p>
            </div>
            <div class="stat-card">
                <h3 id="minRent">$0</h3>
                <p>Starting From</p>
            </div>
            <div class="stat-card">
                <h3 id="greatDeals">0</h3>
                <p>Great Deals</p>
            </div>
        </div>

        <div class="filters">
            <h2>🔍 Filter Apartments</h2>
            <div class="filter-group">
                <div>
                    <label for="bedroomsFilter">Bedrooms</label>
                    <select id="bedroomsFilter">
                        <option value="">All</option>
                        <option value="0">Studio</option>
                        <option value="1">1 BR</option>
                        <option value="2">2 BR</option>
                        <option value="3">3 BR</option>
                        <option value="5">5 BR</option>
                    </select>
                </div>
                <div>
                    <label for="minPrice">Min Price</label>
                    <input type="number" id="minPrice" placeholder="e.g., 1500">
                </div>
                <div>
                    <label for="maxPrice">Max Price</label>
                    <input type="number" id="maxPrice" placeholder="e.g., 3000">
                </div>
                <div>
                    <label for="sourceFilter">Source</label>
                    <select id="sourceFilter">
                        <option value="">All Sources</option>
                    </select>
                </div>
            </div>
            <button onclick="applyFilters()">Apply Filters</button>
            <button onclick="resetFilters()" style="background: #666; margin-left: 10px;">Reset</button>
        </div>

        <div id="listings" class="listings"></div>
    </div>

    <script>
        // All apartment listings data loaded from CSV
        const ALL_LISTINGS = {listings_js};

        // Function to calculate value category
        function getValueCategory(rent, bedrooms, avgRentByBR) {{
            const avgRent = avgRentByBR[bedrooms] || rent;
            const ratio = rent / avgRent;
            
            if (ratio <= 0.85) return 'great-deal';
            if (ratio >= 1.15) return 'overpriced';
            return 'fair-price';
        }}

        function getValueLabel(category) {{
            const labels = {{
                'great-deal': 'Great Deal',
                'fair-price': 'Fair Price',
                'overpriced': 'Overpriced'
            }};
            return labels[category] || 'Fair Price';
        }}

        function calculateStats() {{
            if (ALL_LISTINGS.length === 0) return;
            
            const totalRent = ALL_LISTINGS.reduce((sum, l) => sum + l.rent, 0);
            const avgRent = totalRent / ALL_LISTINGS.length;
            const minRent = Math.min(...ALL_LISTINGS.map(l => l.rent));
            
            // Calculate average rent by bedroom count
            const rentByBR = {{}};
            const countByBR = {{}};
            
            ALL_LISTINGS.forEach(listing => {{
                if (!rentByBR[listing.bedrooms]) {{
                    rentByBR[listing.bedrooms] = 0;
                    countByBR[listing.bedrooms] = 0;
                }}
                rentByBR[listing.bedrooms] += listing.rent;
                countByBR[listing.bedrooms]++;
            }});
            
            const avgRentByBR = {{}};
            Object.keys(rentByBR).forEach(br => {{
                avgRentByBR[br] = rentByBR[br] / countByBR[br];
            }});
            
            // Calculate great deals
            let greatDeals = 0;
            ALL_LISTINGS.forEach(listing => {{
                const category = getValueCategory(listing.rent, listing.bedrooms, avgRentByBR);
                if (category === 'great-deal') greatDeals++;
                listing.valueCategory = category;
                listing.avgRentForBR = avgRentByBR[listing.bedrooms];
            }});
            
            // Update stats display
            document.getElementById('totalListings').textContent = ALL_LISTINGS.length;
            document.getElementById('avgRent').textContent = '$' + Math.round(avgRent).toLocaleString();
            document.getElementById('minRent').textContent = '$' + minRent.toLocaleString();
            document.getElementById('greatDeals').textContent = greatDeals;
            
            // Populate source filter
            const sources = [...new Set(ALL_LISTINGS.map(l => l.source))].sort();
            const sourceFilter = document.getElementById('sourceFilter');
            sourceFilter.innerHTML = '<option value="">All Sources</option>';
            sources.forEach(source => {{
                const option = document.createElement('option');
                option.value = source;
                option.textContent = source;
                sourceFilter.appendChild(option);
            }});
        }}

        function displayListings(listings) {{
            const container = document.getElementById('listings');
            
            if (listings.length === 0) {{
                container.innerHTML = `
                    <div class="no-results">
                        <h2>No apartments found</h2>
                        <p>Try adjusting your filters</p>
                    </div>
                `;
                return;
            }}
            
            container.innerHTML = listings.map(listing => `
                <div class="listing-card">
                    <div class="listing-header">
                        <div class="listing-price">$${{listing.rent.toLocaleString()}}/mo</div>
                        <div class="listing-address">${{listing.address}}</div>
                    </div>
                    <div class="listing-details">
                        <div class="listing-detail-row">
                            <span class="detail-label">Bedrooms</span>
                            <span class="detail-value">${{listing.bedrooms === 0 ? 'Studio' : listing.bedrooms + ' BR'}}</span>
                        </div>
                        <div class="listing-detail-row">
                            <span class="detail-label">Bathrooms</span>
                            <span class="detail-value">${{listing.bathrooms}} BA</span>
                        </div>
                        <div class="listing-detail-row">
                            <span class="detail-label">Square Feet</span>
                            <span class="detail-value">${{listing.sqft.toLocaleString()}} sqft</span>
                        </div>
                        <div class="listing-detail-row">
                            <span class="detail-label">Price/sqft</span>
                            <span class="detail-value">$${{(listing.rent / listing.sqft).toFixed(2)}}</span>
                        </div>
                        <div class="listing-detail-row">
                            <span class="detail-label">Source</span>
                            <span class="detail-value">${{listing.source}}</span>
                        </div>
                        <div style="text-align: center;">
                            <span class="value-badge ${{listing.valueCategory}}">${{getValueLabel(listing.valueCategory)}}</span>
                        </div>
                    </div>
                    <a href="${{listing.url}}" target="_blank" class="listing-link">View Original Listing →</a>
                </div>
            `).join('');
        }}

        function applyFilters() {{
            const bedrooms = document.getElementById('bedroomsFilter').value;
            const minPrice = parseFloat(document.getElementById('minPrice').value) || 0;
            const maxPrice = parseFloat(document.getElementById('maxPrice').value) || Infinity;
            const source = document.getElementById('sourceFilter').value;
            
            const filtered = ALL_LISTINGS.filter(listing => {{
                if (bedrooms && listing.bedrooms !== parseInt(bedrooms)) return false;
                if (listing.rent < minPrice || listing.rent > maxPrice) return false;
                if (source && listing.source !== source) return false;
                return true;
            }});
            
            displayListings(filtered);
        }}

        function resetFilters() {{
            document.getElementById('bedroomsFilter').value = '';
            document.getElementById('minPrice').value = '';
            document.getElementById('maxPrice').value = '';
            document.getElementById('sourceFilter').value = '';
            displayListings(ALL_LISTINGS);
        }}

        // Initialize when page loads
        window.addEventListener('DOMContentLoaded', () => {{
            console.log(`Loaded ${{ALL_LISTINGS.length}} apartment listings`);
            calculateStats();
            displayListings(ALL_LISTINGS);
        }});
    </script>
</body>
</html>'''

# Write to file
output_path = 'index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"\n✅ Generated web app: {output_path}")
print(f"✅ Embedded {len(listings)} listings")
print("\n" + "=" * 70)
print("SUCCESS!")
print("=" * 70)
print(f"\nYour web app is ready!")
print(f"\nTo use it:")
print(f"1. Open '{output_path}' in your web browser")
print(f"2. Double-click the file, or run: open {output_path}")
print(f"\nThe app includes:")
print(f"  • All {len(listings)} apartment listings")
print(f"  • Interactive filtering")
print(f"  • Live statistics")
print(f"  • Value ratings (Great Deal/Fair/Overpriced)")
print("\n" + "=" * 70 + "\n")
