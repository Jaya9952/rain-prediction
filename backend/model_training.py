import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv("data/rainfall_data.csv")


df = df[["STATE_UT_NAME", "DISTRICT", "ANNUAL", "Jun-Sep", "Oct-Dec"]]


df.rename(columns={"STATE_UT_NAME": "Location", "ANNUAL": "TotalRainfall"}, inplace=True)


label_encoder = LabelEncoder()
df["Location"] = label_encoder.fit_transform(df["Location"])


threshold = df["TotalRainfall"].median()  
df["RainTomorrow"] = (df["TotalRainfall"] > threshold).astype(int)  


X = df.drop(columns=["TotalRainfall", "DISTRICT", "RainTomorrow"])  
y = df["RainTomorrow"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)


joblib.dump(model, "rain_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("Model trained and saved successfully!")