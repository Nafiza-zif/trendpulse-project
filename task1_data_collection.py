
import requests
import time
import json
import os
from datetime import datetime
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
def assign_category(title):
    title = title.lower()
    if any(word in title for word in ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"]):
        return "technology"

    elif any(word in title for word in ["war", "government", "country", "president", "election", "climate", "attack", "global"]):
        return "worldnews"

    elif any(word in title for word in ["nfl", "nba", "fifa", "sport", "game", "football", "tennis", "league", "championship","team","player"]):
        return "sports"

    elif any(word in title for word in ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"]):
        return "science"

    elif any(word in title for word in ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming","tv"]):
        return "entertainment"

    else:
        return "others"   
    
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
data = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}
ids = get_top_story_ids()

for story_id in ids:
    print("Processing",story_id)
    story = get_story_details(story_id)

    if not story:
        continue

    clean_data = extract_fields(story)
    category = clean_data["category"]

    if category in data and len(data[category]) < 25:
        data[category].append(clean_data)

    #if all(len(v) >= 25 for v in data.values()):
     #   break
    total_collected=sum(len(v)for v in data.values())
    if total_collected >= 125:
            break

    
time.sleep(2)

if not os.path.exists("data"):
    os.makedirs("data")

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=4)

print(f"Collected {sum(len(v) for v in data.values())} stories. Saved to {filename}")
print("Data collected:", {k: len(v) for k, v in data.items()})

print("DONE")
