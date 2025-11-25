import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

df = pd.read_csv("startup_cleaned.csv")

df = df.dropna(subset=["amount", "vertical", "city", "date"])

df["year"] = pd.to_datetime(df["date"]).dt.year
df["num_investors"] = df["investors"].fillna("").apply(lambda x: len(str(x).split(",")))

# ✅ New powerful features
df["sector_avg"] = df.groupby("vertical")["amount"].transform("mean")
df["city_avg"] = df.groupby("city")["amount"].transform("mean")
df["startup_total"] = df.groupby("startup")["amount"].transform("sum")

X = df[[
    "vertical",
    "city",
    "year",
    "num_investors",
    "sector_avg",
    "city_avg",
    "startup_total"
]]
y = df["amount"]

preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["vertical", "city"]),
    ("num", "passthrough", ["year","num_investors","sector_avg","city_avg","startup_total"])
])

model = Pipeline([
    ("preprocess", preprocess),
    ("rf", RandomForestRegressor(
        n_estimators=500,
        max_depth=15,
        random_state=42
    ))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model.fit(X_train, y_train)

joblib.dump(model, "funding_model.pkl")
print("✅ Model trained and saved")
