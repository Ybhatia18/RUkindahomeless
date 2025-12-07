import pandas as pd
import psycopg2
import sys
import os

print("=" * 70)
print("RUKINDAHOMELESS - DATA LOADING SCRIPT")
print("=" * 70)

# Get the CSV file path
csv_path = '../data/listings.csv'

# Check if CSV exists
if not os.path.exists(csv_path):
    print(f"\n❌ ERROR: Could not find {csv_path}")
    print("Make sure your CSV file is in the data/ folder and named 'listings.csv'")
    sys.exit(1)

# Load CSV
print(f"\n📂 Loading data from {csv_path}...")
df = pd.read_csv(csv_path)
print(f"✅ Found {len(df)} listings in CSV")

# Show column names to verify
print(f"\n📋 CSV Columns: {list(df.columns)}")

# Connect to database
try:
    conn = psycopg2.connect(
        dbname="rukindahomeless",
        user="yakshbha",
        password="",  # Leave empty if you didn't set a password
        host="localhost"
    )
    cursor = conn.cursor()
    print("✅ Connected to database")
except Exception as e:
    print(f"\n❌ Could not connect to database: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure PostgreSQL is running")
    print("2. Make sure you created the database: createdb rukindahomeless")
    print("3. If you set a password during install, add it to the script")
    sys.exit(1)

# Insert listings
print(f"\n⏳ Inserting {len(df)} listings into database...")

inserted = 0
errors = 0

for idx, row in df.iterrows():
    try:
        # Adjust these column names to match YOUR CSV
        # Common variations: 'Rent' vs 'rent', 'BR' vs 'Bedrooms', etc.
        cursor.execute("""
            INSERT INTO listings (address, monthly_rent, bedrooms, bathrooms, square_feet, source, listing_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            str(row['address']),                    # adjust if your column is named differently
            float(row['Rent']),                     # adjust: might be 'rent' or 'monthly_rent'
            int(row['BR']),                         # adjust: might be 'bedrooms' or 'Bedrooms'
            float(row['Ba']),                       # adjust: might be 'bathrooms' or 'Bathrooms'
            int(row['sqft']),                       # adjust: might be 'square_feet' or 'Sqft'
            str(row['source']),                     # adjust if needed
            str(row['url']) if 'url' in row and pd.notna(row['url']) else None
        ))
        inserted += 1
        
        if (inserted % 10 == 0):
            print(f"   Inserted {inserted}/{len(df)} listings...", end='\r')
            
    except Exception as e:
        errors += 1
        print(f"\n⚠️  Error on row {idx}: {e}")
        continue

conn.commit()
print(f"\n✅ Successfully inserted {inserted} listings ({errors} errors)")

# Calculate statistics
print("\n⏳ Calculating value scores...")

cursor.execute("""
    INSERT INTO listing_stats (listing_id, price_per_sqft, price_per_bedroom, avg_rent_for_bedrooms, is_above_average, value_score)
    SELECT 
        l.listing_id,
        ROUND(l.monthly_rent::numeric / l.square_feet, 2),
        ROUND(l.monthly_rent::numeric / l.bedrooms, 2),
        avg_prices.avg_rent,
        CASE WHEN l.monthly_rent > avg_prices.avg_rent THEN TRUE ELSE FALSE END,
        CASE 
            WHEN l.monthly_rent <= avg_prices.avg_rent * 0.85 THEN 9.0
            WHEN l.monthly_rent <= avg_prices.avg_rent * 0.95 THEN 7.5
            WHEN l.monthly_rent <= avg_prices.avg_rent * 1.05 THEN 6.0
            WHEN l.monthly_rent <= avg_prices.avg_rent * 1.15 THEN 4.0
            ELSE 2.0
        END
    FROM listings l
    JOIN (
        SELECT bedrooms, AVG(monthly_rent) as avg_rent
        FROM listings GROUP BY bedrooms
    ) avg_prices ON l.bedrooms = avg_prices.bedrooms
""")
conn.commit()
print("✅ Value scores calculated!")

# Show summary
print("\n" + "=" * 70)
print("DATABASE SUMMARY")
print("=" * 70)

cursor.execute("SELECT COUNT(*) FROM listings")
total = cursor.fetchone()[0]
print(f"\nTotal listings in database: {total}")

cursor.execute("SELECT * FROM rent_summary")
print("\nRent Summary by Bedrooms:")
print(f"{'BR':<4} {'Count':<8} {'Avg Rent':<12} {'Min Rent':<12} {'Max Rent':<12} {'Avg Sqft':<10}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:<4} {row[1]:<8} ${row[2]:<11.2f} ${row[3]:<11.2f} ${row[4]:<11.2f} {row[5]:<10.0f}")

cursor.close()
conn.close()

print("\n✅ Data loading complete!")
print("=" * 70 + "\n")