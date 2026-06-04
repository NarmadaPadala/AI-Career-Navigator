import pandas as pd


df = pd.read_csv("ai_jobs_market_2025_2026.csv")

print("Column names:")
print(df.columns.tolist())

print("\nNumber of rows and columns:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())
