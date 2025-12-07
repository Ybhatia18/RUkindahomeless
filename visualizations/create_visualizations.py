"""
RUKindaHomeless - Data Visualizations
Creates 5 comprehensive charts for analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

print("=" * 70)
print("RUKINDAHOMELESS - DATA VISUALIZATIONS")
print("=" * 70)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Load data
print("\n📂 Loading data...")
df = pd.read_csv('../data/listings.csv')
df['rent'] = df['rent'].astype(str).str.replace(',', '').astype(float)
df['price_per_sqft'] = df['rent'] / df['sqft']

print(f"✅ Loaded {len(df)} listings")

# Create figure directory
import os
if not os.path.exists('charts'):
    os.makedirs('charts')
    print("📁 Created 'charts' folder")

# ============================================================================
# CHART 1: Bar Chart - Average Rent by Bedrooms
# ============================================================================
print("\n📊 Creating Chart 1: Average Rent by Bedrooms...")

plt.figure(figsize=(10, 6))
avg_rent_by_br = df.groupby('BR')['rent'].agg(['mean', 'count']).reset_index()

bars = plt.bar(avg_rent_by_br['BR'], avg_rent_by_br['mean'], 
               color='steelblue', edgecolor='black', alpha=0.7)

# Add value labels on bars
for i, (br, rent, count) in enumerate(zip(avg_rent_by_br['BR'], 
                                           avg_rent_by_br['mean'], 
                                           avg_rent_by_br['count'])):
    plt.text(br, rent + 50, f'${rent:.0f}\n(n={count})', 
             ha='center', va='bottom', fontweight='bold')

plt.xlabel('Number of Bedrooms', fontsize=12, fontweight='bold')
plt.ylabel('Average Monthly Rent ($)', fontsize=12, fontweight='bold')
plt.title('Average Rent by Number of Bedrooms', fontsize=14, fontweight='bold', pad=20)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/1_avg_rent_by_bedrooms.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: charts/1_avg_rent_by_bedrooms.png")
plt.close()

# ============================================================================
# CHART 2: Scatter Plot - Rent vs Square Feet
# ============================================================================
print("📊 Creating Chart 2: Rent vs Square Feet...")

plt.figure(figsize=(10, 6))

# Color by bedrooms
colors = {0: '#e74c3c', 1: '#3498db', 2: '#2ecc71', 3: '#f39c12', 5: '#9b59b6'}
for br in sorted(df['BR'].unique()):
    subset = df[df['BR'] == br]
    plt.scatter(subset['sqft'], subset['rent'], 
                c=colors.get(br, '#95a5a6'), 
                label=f'{br} BR', s=100, alpha=0.6, edgecolors='black')

# Add trend line
z = np.polyfit(df['sqft'], df['rent'], 1)
p = np.poly1d(z)
plt.plot(df['sqft'].sort_values(), p(df['sqft'].sort_values()), 
         "r--", alpha=0.8, linewidth=2, label=f'Trend: y={z[0]:.2f}x+{z[1]:.0f}')

plt.xlabel('Square Feet', fontsize=12, fontweight='bold')
plt.ylabel('Monthly Rent ($)', fontsize=12, fontweight='bold')
plt.title('Rent vs Square Footage with Trend Line', fontsize=14, fontweight='bold', pad=20)
plt.legend(loc='upper left', framealpha=0.9)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/2_rent_vs_sqft.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: charts/2_rent_vs_sqft.png")
plt.close()

# ============================================================================
# CHART 3: Box Plot - Rent Distribution by Source
# ============================================================================
print("📊 Creating Chart 3: Rent Distribution by Source...")

plt.figure(figsize=(12, 6))

# Prepare data
sources = df['source'].value_counts().index.tolist()
data_by_source = [df[df['source'] == source]['rent'].values for source in sources]

bp = plt.boxplot(data_by_source, labels=sources, patch_artist=True,
                  notch=True, showmeans=True,
                  boxprops=dict(facecolor='lightblue', edgecolor='black'),
                  whiskerprops=dict(color='black'),
                  capprops=dict(color='black'),
                  medianprops=dict(color='red', linewidth=2),
                  meanprops=dict(marker='D', markerfacecolor='green', markersize=8))

plt.xlabel('Data Source', fontsize=12, fontweight='bold')
plt.ylabel('Monthly Rent ($)', fontsize=12, fontweight='bold')
plt.title('Rent Distribution by Data Source', fontsize=14, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/3_rent_by_source.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: charts/3_rent_by_source.png")
plt.close()

# ============================================================================
# CHART 4: Pie Chart - Listings by Source
# ============================================================================
print("📊 Creating Chart 4: Listings by Source...")

plt.figure(figsize=(10, 8))

source_counts = df['source'].value_counts()
colors_pie = plt.cm.Set3(range(len(source_counts)))

wedges, texts, autotexts = plt.pie(source_counts.values, 
                                     labels=source_counts.index,
                                     autopct='%1.1f%%',
                                     colors=colors_pie,
                                     startangle=90,
                                     explode=[0.05] * len(source_counts),
                                     shadow=True)

# Make percentage text bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

# Add count in legend
legend_labels = [f'{source}: {count} listings' 
                 for source, count in source_counts.items()]
plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))

plt.title('Distribution of Listings by Data Source', 
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('charts/4_listings_by_source.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: charts/4_listings_by_source.png")
plt.close()

# ============================================================================
# CHART 5: Heatmap - Feature Correlation Matrix
# ============================================================================
print("📊 Creating Chart 5: Feature Correlation Heatmap...")

plt.figure(figsize=(10, 8))

# Select numeric columns for correlation
corr_data = df[['BR', 'Ba', 'sqft', 'rent', 'price_per_sqft']].corr()

# Create heatmap
sns.heatmap(corr_data, annot=True, fmt='.3f', cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            vmin=-1, vmax=1)

plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('charts/5_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: charts/5_correlation_heatmap.png")
plt.close()

# ============================================================================
# BONUS: Summary Statistics Table as Image
# ============================================================================
print("📊 Creating Bonus: Summary Statistics Table...")

fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('tight')
ax.axis('off')

# Create summary stats
summary_stats = df[['rent', 'BR', 'Ba', 'sqft', 'price_per_sqft']].describe()
summary_stats = summary_stats.round(2)

table = ax.table(cellText=summary_stats.values,
                 rowLabels=summary_stats.index,
                 colLabels=summary_stats.columns,
                 cellLoc='center',
                 loc='center',
                 colWidths=[0.15] * len(summary_stats.columns))

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style header
for i in range(len(summary_stats.columns)):
    table[(0, i)].set_facecolor('#4472C4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style row labels
for i in range(len(summary_stats.index)):
    table[(i+1, -1)].set_facecolor('#D9E1F2')
    table[(i+1, -1)].set_text_props(weight='bold')

plt.title('Summary Statistics for All Listings', 
          fontsize=14, fontweight='bold', pad=20)
plt.savefig('charts/6_summary_statistics.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: charts/6_summary_statistics.png")
plt.close()

# ============================================================================
# Print Summary
# ============================================================================
print("\n" + "=" * 70)
print("VISUALIZATION SUMMARY")
print("=" * 70)

print("\n📊 Charts Created:")
print("   1. Average Rent by Bedrooms (Bar Chart)")
print("   2. Rent vs Square Feet (Scatter Plot with Trend)")
print("   3. Rent Distribution by Source (Box Plot)")
print("   4. Listings by Source (Pie Chart)")
print("   5. Feature Correlation Matrix (Heatmap)")
print("   6. Summary Statistics Table (Bonus)")

print("\n📁 All charts saved in: charts/ folder")
print("\n✅ VISUALIZATION GENERATION COMPLETE!")
print("=" * 70 + "\n")

# Print key insights
print("\n💡 KEY INSIGHTS FROM DATA:")
print("-" * 70)
print(f"   • Total Listings: {len(df)}")
print(f"   • Average Rent: ${df['rent'].mean():.2f}")
print(f"   • Median Rent: ${df['rent'].median():.2f}")
print(f"   • Rent Range: ${df['rent'].min():.2f} - ${df['rent'].max():.2f}")
print(f"   • Average Price/Sqft: ${df['price_per_sqft'].mean():.2f}")
print(f"   • Most Common Source: {df['source'].mode()[0]} ({df['source'].value_counts().iloc[0]} listings)")
print(f"   • Most Common Bedroom Count: {df['BR'].mode()[0]} BR ({df['BR'].value_counts().iloc[0]} listings)")
print()