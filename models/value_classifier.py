"""
RUKindaHomeless - Value Classifier Model
Classifies apartments as: Great Deal, Fair Price, or Overpriced
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle

print("=" * 70)
print("VALUE CLASSIFIER MODEL")
print("=" * 70)

# Load data
print("\n📂 Loading data...")
df = pd.read_csv('../data/listings.csv')

# Clean rent column
df['rent'] = df['rent'].astype(str).str.replace(',', '').astype(float)

print(f"✅ Loaded {len(df)} listings")

# Calculate price per square foot
df['price_per_sqft'] = df['rent'] / df['sqft']

# Calculate average rent for each bedroom count
avg_rent_by_br = df.groupby('BR')['rent'].mean().to_dict()
df['avg_rent_for_br'] = df['BR'].map(avg_rent_by_br)

# Create value categories based on comparison to average
print("\n🏷️  Creating value categories...")

def classify_value(row):
    """
    Great Deal: 15% or more below average for that bedroom count
    Fair Price: Within 15% of average
    Overpriced: 15% or more above average
    """
    ratio = row['rent'] / row['avg_rent_for_br']
    
    if ratio <= 0.85:
        return 'Great Deal'
    elif ratio >= 1.15:
        return 'Overpriced'
    else:
        return 'Fair Price'

df['value_category'] = df.apply(classify_value, axis=1)

# Show distribution
print("\n📊 Value Category Distribution:")
value_counts = df['value_category'].value_counts()
for category, count in value_counts.items():
    pct = (count / len(df)) * 100
    print(f"   {category}: {count} listings ({pct:.1f}%)")

# Prepare features
print("\n🔧 Preparing features...")
X = df[['BR', 'Ba', 'sqft', 'price_per_sqft']].copy()
y = df['value_category'].copy()

# Handle any missing values
X = X.fillna(X.mean())

print(f"   Features (X): {X.shape}")
print(f"   Target (y): {y.shape}")

# Split data
print("\n✂️  Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Training set: {X_train.shape[0]} samples")
print(f"   Test set: {X_test.shape[0]} samples")

# Train classifier
print("\n🌲 Training Random Forest Classifier...")
classifier = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=3,
    random_state=42,
    n_jobs=-1
)

classifier.fit(X_train, y_train)
print("✅ Classifier trained successfully!")

# Make predictions
print("\n🔮 Making predictions...")
y_pred_train = classifier.predict(X_train)
y_pred_test = classifier.predict(X_test)

# Calculate accuracy
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print("\n" + "=" * 70)
print("CLASSIFIER PERFORMANCE")
print("=" * 70)

print(f"\n📊 Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"📊 Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# Detailed classification report
print("\n📋 Detailed Classification Report (Test Set):")
print(classification_report(y_test, y_pred_test))

# Confusion matrix
print("\n🔢 Confusion Matrix (Test Set):")
cm = confusion_matrix(y_test, y_pred_test, labels=['Great Deal', 'Fair Price', 'Overpriced'])
print(f"\n{'':>15} {'Predicted Great':<18} {'Predicted Fair':<18} {'Predicted Overpriced':<18}")
print("-" * 70)
labels = ['Great Deal', 'Fair Price', 'Overpriced']
for i, label in enumerate(labels):
    print(f"{'Actual ' + label:>15} {cm[i][0]:<18} {cm[i][1]:<18} {cm[i][2]:<18}")

# Feature importance
print("\n🎯 Feature Importance:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': classifier.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.iterrows():
    print(f"   {row['feature']}: {row['importance']:.4f}")

# Example predictions
print("\n" + "=" * 70)
print("EXAMPLE CLASSIFICATIONS")
print("=" * 70)

examples = [
    {'BR': 1, 'Ba': 1, 'sqft': 700, 'rent': 1500},
    {'BR': 2, 'Ba': 1, 'sqft': 900, 'rent': 1800},
    {'BR': 2, 'Ba': 2, 'sqft': 1100, 'rent': 2500},
    {'BR': 2, 'Ba': 2, 'sqft': 1100, 'rent': 3500},
]

print(f"\n{'BR':<4} {'Ba':<4} {'Sqft':<8} {'Rent':<10} {'$/sqft':<10} {'Classification':<15}")
print("-" * 70)

for ex in examples:
    price_per_sqft = ex['rent'] / ex['sqft']
    pred = classifier.predict([[ex['BR'], ex['Ba'], ex['sqft'], price_per_sqft]])[0]
    print(f"{ex['BR']:<4} {ex['Ba']:<4} {ex['sqft']:<8} ${ex['rent']:<9} ${price_per_sqft:<9.2f} {pred:<15}")

# Save classifier
print("\n💾 Saving classifier...")
with open('value_classifier.pkl', 'wb') as f:
    pickle.dump(classifier, f)
print("✅ Classifier saved as 'value_classifier.pkl'")

# Save category mapping
category_info = {
    'categories': ['Great Deal', 'Fair Price', 'Overpriced'],
    'distribution': value_counts.to_dict(),
    'train_accuracy': train_accuracy,
    'test_accuracy': test_accuracy,
    'feature_importance': feature_importance.to_dict('records')
}

with open('classifier_info.pkl', 'wb') as f:
    pickle.dump(category_info, f)

print("\n" + "=" * 70)
print("✅ CLASSIFIER TRAINING COMPLETE!")
print("=" * 70)
print(f"\nKey Takeaways:")
print(f"   • Classifier achieves {test_accuracy*100:.1f}% accuracy on test data")
print(f"   • {value_counts['Great Deal']} great deals found in dataset")
print(f"   • Most important feature: {feature_importance.iloc[0]['feature']}")
print("\n")