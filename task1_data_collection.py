# Import required libraries
import requests
import time
import json
import os
from datetime import datetime

# Function to fetch stories ID From HackerNews API

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
def get_top_story_ids():
    try:
        headers={"User-Agent":"TrendPulse/1.0"}
        response=requests.get(TOP_STORIES_URL,headers=headers)
        response.raise_for_status()
        return response.json()[:1500]
    except Exception as e:
        print("Error fetching top stories:",e)
        return[]
#ids=get_top_story_ids()
#print(len(ids))

#Fetch to get the details of the story

def get_story_details(story_id):
    url=f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        headers={"User-Agent":"TrendPulse/1.0"}
        response=requests.get(url,headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story{story_id}",e)
        return None
    
#Function to categorize story based on title    
def assign_category(title):
    title = title.lower()
    if any(word in title for word in ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"]):
        return "technology"

    elif any(word in title for word in ["war", "government", "country", "president", "election", "climate", "attack", "global"]):
        return "worldnews"

    elif any(word in title for word in ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"]):
        return "sports"

    elif any(word in title for word in ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"]):
        return "science"

    elif any(word in title for word in ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming","tv"]):
        return "entertainment"

    else:
        return "others"   
    
# extracting the required fields from story data    
    
def extract_fields(story):
    if not story:
        return None

    return {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": assign_category(story.get("title", "")),
        "score": story.get("score"),
        "num_comments": story.get("descendants"),
        "author": story.get("by"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
#Store data category wise
data = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}
ids = get_top_story_ids()

# loop through story IDs and collect data

for story_id in ids:
    print("Processing",story_id)
    story = get_story_details(story_id)

    if not story:
        continue

    clean_data = extract_fields(story)
    category = clean_data["category"]
# add story to corresponding category 

    if category in data and len(data[category]) < 125:
        data[category].append(clean_data)

    #if all(len(v) >= 25 for v in data.values()):
     #   break
    total_collected=sum(len(v)for v in data.values())
    if total_collected >= 125:
            break

    
time.sleep(2)

#create data folder if it doesn't exist

if not os.path.exists("data"):
    os.makedirs("data")

#Generate file name with current date

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

# Save collected data into JSON file
with open(filename, "w") as f:
    json.dump(data, f, indent=4)

#Print summary
print(f"Collected {sum(len(v) for v in data.values())} stories. Saved to {filename}")
print("Data collected:", {k: len(v) for k, v in data.items()})

print("DONE")
