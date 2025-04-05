import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv("data/rainfall_data.csv")


print("Available columns:", df.columns.tolist())


df.rename(columns={"STATE_UT_NAME": "Location", "ANNUAL": "TotalRainfall"}, inplace=True)


df = df[["Location", "TotalRainfall"]].copy()
df.dropna(inplace=True)


monthly_data = pd.DataFrame()

for month in range(1, 13):
    temp = df.copy()
    temp["Month"] = month
    temp["MonthlyRainfall"] = temp["TotalRainfall"] / 12  
    monthly_data = pd.concat([monthly_data, temp])


threshold = monthly_data["MonthlyRainfall"].median()
monthly_data["RainTomorrow"] = (monthly_data["MonthlyRainfall"] > threshold).astype(int)


label_encoder = LabelEncoder()
monthly_data["LocationEncoded"] = label_encoder.fit_transform(monthly_data["Location"])


X = monthly_data[["LocationEncoded", "Month"]]
y = monthly_data["RainTomorrow"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)


joblib.dump(model, "rain_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("Model trained for all months based on Location and Month!")

