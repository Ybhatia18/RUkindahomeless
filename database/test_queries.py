import psycopg2

print("\n" + "="*70)
print("RUKINDAHOMELESS - SQL QUERY DEMONSTRATIONS")
print("="*70 + "\n")

# Connect to database
conn = psycopg2.connect(
    dbname="rukindahomeless",
    user="yakshbha",
    password="",
    host="localhost"
)
cursor = conn.cursor()

# Query 1: Average rent by bedrooms
print("QUERY 1: Average rent by number of bedrooms")
print("-" * 70)
cursor.execute("""
    SELECT bedrooms, COUNT(*) as num_listings, 
           ROUND(AVG(monthly_rent), 2) as avg_rent,
           ROUND(MIN(monthly_rent), 2) as min_rent,
           ROUND(MAX(monthly_rent), 2) as max_rent
    FROM listings
    GROUP BY bedrooms
    ORDER BY bedrooms
""")
print(f"{'BR':<4} {'Count':<8} {'Avg Rent':<12} {'Min Rent':<12} {'Max Rent':<12}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:<4} {row[1]:<8} ${row[2]:<11.2f} ${row[3]:<11.2f} ${row[4]:<11.2f}")

# Query 2: Best deals
print("\n\nQUERY 2: Top 10 Best Value Apartments (Score >= 7)")
print("-" * 70)
cursor.execute("""
    SELECT l.address, l.bedrooms, l.monthly_rent, s.value_score
    FROM listings l
    JOIN listing_stats s ON l.listing_id = s.listing_id
    WHERE s.value_score >= 7.0
    ORDER BY s.value_score DESC
    LIMIT 10
""")
print(f"{'Address':<40} {'BR':<4} {'Rent':<10} {'Score':<6}")
print("-" * 70)
for row in cursor.fetchall():
    address = row[0][:37] + "..." if len(row[0]) > 40 else row[0]
    print(f"{address:<40} {row[1]:<4} ${row[2]:<9.2f} {row[3]:<6.1f}")

# Query 3: Cheapest apartment for each bedroom count
print("\n\nQUERY 3: Cheapest Apartment for Each Bedroom Count")
print("-" * 70)
cursor.execute("""
    SELECT DISTINCT ON (bedrooms) 
           bedrooms, address, monthly_rent, source
    FROM listings
    ORDER BY bedrooms, monthly_rent
""")
print(f"{'BR':<4} {'Address':<40} {'Rent':<10} {'Source':<15}")
print("-" * 70)
for row in cursor.fetchall():
    address = row[1][:37] + "..." if len(row[1]) > 40 else row[1]
    print(f"{row[0]:<4} {address:<40} ${row[2]:<9.2f} {row[3]:<15}")

# Query 4: Source comparison
print("\n\nQUERY 4: Average Rent by Data Source")
print("-" * 70)
cursor.execute("""
    SELECT source, COUNT(*) as count, 
           ROUND(AVG(monthly_rent), 2) as avg_rent,
           ROUND(AVG(square_feet), 2) as avg_sqft
    FROM listings
    GROUP BY source
    ORDER BY avg_rent
""")
print(f"{'Source':<20} {'Count':<8} {'Avg Rent':<12} {'Avg Sqft':<10}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:<20} {row[1]:<8} ${row[2]:<11.2f} {row[3]:<10.0f}")

# Query 5: Above vs below average
print("\n\nQUERY 5: Listings Above Average for Their Bedroom Count")
print("-" * 70)
cursor.execute("""
    SELECT l.bedrooms, 
           COUNT(*) as total,
           SUM(CASE WHEN s.is_above_average THEN 1 ELSE 0 END) as above_avg,
           SUM(CASE WHEN NOT s.is_above_average THEN 1 ELSE 0 END) as below_avg
    FROM listings l
    JOIN listing_stats s ON l.listing_id = s.listing_id
    GROUP BY l.bedrooms
    ORDER BY l.bedrooms
""")
print(f"{'BR':<4} {'Total':<8} {'Above Avg':<12} {'Below Avg':<12}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:<4} {row[1]:<8} {row[2]:<12} {row[3]:<12}")

# Query 6: Price per sqft leaders
print("\n\nQUERY 6: Most Expensive per Square Foot")
print("-" * 70)
cursor.execute("""
    SELECT l.address, l.bedrooms, l.monthly_rent, l.square_feet, s.price_per_sqft
    FROM listings l
    JOIN listing_stats s ON l.listing_id = s.listing_id
    ORDER BY s.price_per_sqft DESC
    LIMIT 5
""")
print(f"{'Address':<40} {'BR':<4} {'Rent':<10} {'Sqft':<8} {'$/sqft':<8}")
print("-" * 70)
for row in cursor.fetchall():
    address = row[0][:37] + "..." if len(row[0]) > 40 else row[0]
    print(f"{address:<40} {row[1]:<4} ${row[2]:<9.2f} {row[3]:<8} ${row[4]:<7.2f}")

# Query 7: Complex multi-table join
print("\n\nQUERY 7: 2BR Apartments with Best Value Scores")
print("-" * 70)
cursor.execute("""
    SELECT l.address, l.monthly_rent, l.square_feet, s.value_score, l.source
    FROM listings l
    JOIN listing_stats s ON l.listing_id = s.listing_id
    WHERE l.bedrooms = 2
    ORDER BY s.value_score DESC
    LIMIT 5
""")
print(f"{'Address':<40} {'Rent':<10} {'Sqft':<8} {'Score':<8} {'Source':<15}")
print("-" * 70)
for row in cursor.fetchall():
    address = row[0][:37] + "..." if len(row[0]) > 40 else row[0]
    print(f"{address:<40} ${row[1]:<9.2f} {row[2]:<8} {row[3]:<7.1f} {row[4]:<15}")

print("\n" + "="*70 + "\n")

cursor.close()
conn.close()