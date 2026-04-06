import json
import pandas as pd

# Load JSON file
with open("data/trends_20260406.json", "r") as f:
    data = json.load(f)

# Convert nested JSON to flat list
rows = []
for category, stories in data.items():
    for story in stories:
        rows.append(story)

# Create DataFrame
df = pd.DataFrame(rows)

# Print loaded rows
print(f"Loaded {len(df)} stories from data/trends_20260406.json")

# Remove duplicates
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low-quality stories
df = df[df["score"] > 5]
print(f"After removing low scores: {len(df)}")

# Clean title whitespace
df["title"] = df["title"].str.strip()

# Save as CSV
df.to_csv("data/trends_clean.csv", index=False)
print(f"\nSaved {len(df)} rows to data/trends_clean.csv")

# Category summary
print("\nStories per category:")
print(df["category"].value_counts())