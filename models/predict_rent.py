"""
RUKindaHomeless - Random Forest Rent Prediction Model
Predicts monthly rent based on bedrooms, bathrooms, and square footage
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import pickle
import matplotlib.pyplot as plt

print("=" * 70)
print("RANDOM FOREST RENT PREDICTION MODEL")
print("=" * 70)

# Load data
print("\n📂 Loading data...")
df = pd.read_csv('../data/listings.csv')

# Clean rent column (remove commas if present)
df['rent'] = df['rent'].astype(str).str.replace(',', '').astype(float)

print(f"✅ Loaded {len(df)} listings")
print(f"📋 Columns: {list(df.columns)}")

# Prepare features and target
print("\n🔧 Preparing features...")
X = df[['BR', 'Ba', 'sqft']].copy()
y = df['rent'].copy()

# Handle any missing values
X = X.fillna(X.mean())
y = y.fillna(y.mean())

print(f"   Features (X): {X.shape}")
print(f"   Target (y): {y.shape}")

# Split data
print("\n✂️  Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"   Training set: {X_train.shape[0]} samples")
print(f"   Test set: {X_test.shape[0]} samples")

# Train Random Forest model
print("\n🌲 Training Random Forest model...")
model = RandomForestRegressor(
    n_estimators=100,      # 100 trees in the forest
    max_depth=10,          # Maximum depth of each tree
    min_samples_split=5,   # Minimum samples to split a node
    random_state=42,
    n_jobs=-1              # Use all CPU cores
)

model.fit(X_train, y_train)
print("✅ Model trained successfully!")

# Make predictions
print("\n🔮 Making predictions...")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Calculate metrics
print("\n" + "=" * 70)
print("MODEL PERFORMANCE METRICS")
print("=" * 70)

# Training metrics
train_mae = mean_absolute_error(y_train, y_pred_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
train_r2 = r2_score(y_train, y_pred_train)

print("\n📊 Training Set Performance:")
print(f"   MAE (Mean Absolute Error): ${train_mae:.2f}")
print(f"   RMSE (Root Mean Squared Error): ${train_rmse:.2f}")
print(f"   R² Score: {train_r2:.4f}")

# Test metrics
test_mae = mean_absolute_error(y_test, y_pred_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
test_r2 = r2_score(y_test, y_pred_test)

print("\n📊 Test Set Performance:")
print(f"   MAE (Mean Absolute Error): ${test_mae:.2f}")
print(f"   RMSE (Root Mean Squared Error): ${test_rmse:.2f}")
print(f"   R² Score: {test_r2:.4f}")

# Feature importance
print("\n🎯 Feature Importance:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.iterrows():
    print(f"   {row['feature']}: {row['importance']:.4f}")

# Example predictions
print("\n" + "=" * 70)
print("EXAMPLE PREDICTIONS")
print("=" * 70)

examples = [
    {'BR': 1, 'Ba': 1, 'sqft': 700},
    {'BR': 2, 'Ba': 1, 'sqft': 900},
    {'BR': 2, 'Ba': 2, 'sqft': 1100},
    {'BR': 3, 'Ba': 2, 'sqft': 1300},
]

print(f"\n{'Bedrooms':<10} {'Bathrooms':<12} {'Sqft':<10} {'Predicted Rent':<15}")
print("-" * 70)
for ex in examples:
    pred = model.predict([[ex['BR'], ex['Ba'], ex['sqft']]])[0]
    print(f"{ex['BR']:<10} {ex['Ba']:<12} {ex['sqft']:<10} ${pred:<14.2f}")

# Save model
print("\n💾 Saving model...")
with open('rent_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✅ Model saved as 'rent_predictor.pkl'")

# Save metrics to file
metrics_summary = {
    'model_type': 'Random Forest Regressor',
    'n_estimators': 100,
    'train_mae': train_mae,
    'train_rmse': train_rmse,
    'train_r2': train_r2,
    'test_mae': test_mae,
    'test_rmse': test_rmse,
    'test_r2': test_r2,
    'feature_importance': feature_importance.to_dict('records')
}

with open('model_metrics.pkl', 'wb') as f:
    pickle.dump(metrics_summary, f)

print("\n" + "=" * 70)
print("✅ MODEL TRAINING COMPLETE!")
print("=" * 70)
print(f"\nKey Takeaways:")
print(f"   • Model can predict rent within ${test_mae:.2f} on average")
print(f"   • R² score of {test_r2:.4f} means the model explains {test_r2*100:.1f}% of rent variance")
print(f"   • Most important feature: {feature_importance.iloc[0]['feature']}")
print("\n")