import pandas as pd
import numpy as np

# -------------------------------
# 1. Load the CSV
# -------------------------------

df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")

# -------------------------------
# 2. Explore data
# -------------------------------

print("\nFirst 5 rows:")
print(df.head())

print(f"\nAverage score: {df['score'].mean():,.0f}")
print(f"Average comments: {df['num_comments'].mean():,.0f}")

# -------------------------------
# 3. NumPy Analysis
# -------------------------------

scores = df["score"].values

print("\n--- NumPy Stats ---")
print(f"Mean score: {np.mean(scores):,.0f}")
print(f"Median score: {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score: {np.max(scores):,}")
print(f"Min score: {np.min(scores)}")

# Most stories category

top_category = df["category"].value_counts().idxmax()
top_count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Most commented story

top_story = df.loc[df["num_comments"].idxmax()]
print(f"\nMost commented story: \"{top_story['title']}\" - {top_story['num_comments']} comments")

# -------------------------------
# 4. Add new columns
# -------------------------------

# Engagement
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular (based on average score)
avg_score = df["score"].mean()
df["is_popular"] = df["score"] > avg_score

# -------------------------------
# 5. Save final CSV
# -------------------------------
df.to_csv("data/trends_analysed.csv", index=False)

print("\nSaved to data/trends_analysed.csv")