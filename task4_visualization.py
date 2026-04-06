# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder if not exists
os.makedirs("outputs", exist_ok=True)

# -------------------------------
# Chart 1: Top 10 Stories by Score
# -------------------------------

top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten titles (max 50 chars)
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure()
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# -------------------------------
# Chart 2: Stories per Category
# -------------------------------

category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# -------------------------------
# Chart 3: Score vs Comments
# -------------------------------

plt.figure()

# Split based on popularity
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

print("All charts saved in outputs folder!")

# -------------------------------
# Bonus mark Dashboard - combined chart
# -------------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1: Top Stories
top10 = df.sort_values(by="score", ascending=False).head(10)
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

axes[0].barh(top10["short_title"], top10["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Chart 2: Categories
category_counts = df["category"].value_counts()
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")

# Chart 3: Scatter
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

# Overall title
plt.suptitle("TrendPulse Dashboard")

# Save dashboard
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Dashboard saved as outputs/dashboard.png")