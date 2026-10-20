import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("Dataset/student-por.csv")

# Create Risk categories
def classify_risk(g3):
    if g3 < 10:
        return "High Risk"
    elif g3 <= 13:
        return "Medium Risk"
    else:
        return "Low Risk"

df["Risk"] = df["G3"].apply(classify_risk)

# Convert text columns into numbers
encoder = LabelEncoder()

categorical_columns = [
    "sex",
    "schoolsup",
    "famsup",
    "internet"
]

for col in categorical_columns:
    df[col] = encoder.fit_transform(df[col])

# Select features
X = df[
    [
        "age",
        "sex",
        "studytime",
        "failures",
        "absences",
        "schoolsup",
        "famsup",
        "internet",
        "Medu",
        "Fedu",
        "G1",
        "G2"
    ]
]

# Target
y = df["Risk"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

import pickle

pickle.dump(
    model,
    open(
        "models/risk_model.pkl",
        "wb"
    )
)

print("Model saved successfully!")