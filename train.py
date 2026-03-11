import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
import joblib

print("Step 1: Data load ho raha hai...")
# 1. Dataset load kar rahe hain
df = pd.read_csv('heart_failure.csv')

# 2. Features (X) aur Target (y) alag kar rahe hain
X = df.drop('DEATH_EVENT', axis=1)
y = df['DEATH_EVENT']

# 3. Data ko Train (80%) aur Test (20%) mein baant rahe hain
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Step 2: AI Model seekh raha hai (Training)...")
# 4. XGBoost Model bana kar train kar rahe hain
model = xgb.XGBClassifier(
    n_estimators=100, 
    learning_rate=0.1, 
    max_depth=4, 
    random_state=42,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# 5. Model ka test le rahe hain (Accuracy check)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model ki Accuracy: {accuracy * 100:.2f}%")

print("Step 3: Trained Model ko save kar rahe hain...")
# 6. Model ko save kar rahe hain taaki humari website iska use kar sake
joblib.dump(model, 'heart_model.pkl')
print("🎉 Success! 'heart_model.pkl' file ban gayi hai.")