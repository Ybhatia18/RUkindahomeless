-- RUKindaHomeless Database Schema
-- Created: December 3, 2024

-- Main listings table
CREATE TABLE listings (
    listing_id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    monthly_rent DECIMAL(10,2) NOT NULL,
    bedrooms INT NOT NULL,
    bathrooms DECIMAL(3,1) NOT NULL,
    square_feet INT NOT NULL,
    source VARCHAR(50),
    listing_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Statistics and calculated metrics
CREATE TABLE listing_stats (
    stat_id SERIAL PRIMARY KEY,
    listing_id INT REFERENCES listings(listing_id) ON DELETE CASCADE,
    price_per_sqft DECIMAL(6,2),
    price_per_bedroom DECIMAL(10,2),
    avg_rent_for_bedrooms DECIMAL(10,2),
    is_above_average BOOLEAN,
    value_score DECIMAL(3,1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_rent ON listings(monthly_rent);
CREATE INDEX idx_bedrooms ON listings(bedrooms);
CREATE INDEX idx_source ON listings(source);
CREATE INDEX idx_sqft ON listings(square_feet);

-- View for summary statistics
CREATE VIEW rent_summary AS
SELECT 
    bedrooms,
    COUNT(*) as num_listings,
    ROUND(AVG(monthly_rent), 2) as avg_rent,
    ROUND(MIN(monthly_rent), 2) as min_rent,
    ROUND(MAX(monthly_rent), 2) as max_rent,
    ROUND(AVG(square_feet), 2) as avg_sqft
FROM listings
GROUP BY bedrooms
ORDER BY bedrooms;