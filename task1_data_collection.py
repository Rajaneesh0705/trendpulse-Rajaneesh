import requests
import json
import os
import time
from datetime import datetime
categories = { #5 categories with keywords to match in story titles
    "technology":    ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
}
#HackerNews API links
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
story_url       = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HEADERS = {"User-Agent": "TrendPulse/1.0"} #Telling HackerNews which app is calling

response = requests.get(top_stories_url, headers=HEADERS)
all_ids  = response.json()
top_500  = all_ids[:500] #Only need the first 500
print(f"Fetched {len(top_500)} story IDs")

category_counts = { #Tracking how many stories collected per category
    "technology":    0,
    "worldnews":     0,
    "sports":        0,
    "science":       0,
    "entertainment": 0,
}
all_stories  = [] #All collected stories go here
collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Recording time once for all stories
print("\nCollecting stories...\n")
for story_id in top_500:
    if category_counts["technology"] == 25 and category_counts["worldnews"] == 25 and category_counts["sports"] == 25 and category_counts["science"] == 25 and category_counts["entertainment"] == 25: #If all categories hit 25, stop looping
        print("All categories are full. Done!")
        break
    story_response = requests.get(story_url.format(story_id), headers=HEADERS) #Fetching story details
    story = story_response.json()
    if story is None or "title" not in story: #Skip if no title
        continue
    title = story["title"]
    matched_category = None
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title.lower(): #Case-insensitive match
                matched_category = category
                break #Found a keyword match, no continuation
        if matched_category:
            break #Found a category, no continuation
    if matched_category is None: #No keyword matched, skip this story
        continue
    if category_counts[matched_category] >= 25: #Category already full, skip
        continue
    record = { #Building the record with 7 required fields
        "post_id":      story["id"],
        "title":        title,
        "category":     matched_category,
        "score":        story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author":       story.get("by", ""),
        "collected_at": collected_at,
    }
    all_stories.append(record)
    category_counts[matched_category] = category_counts[matched_category] + 1
    print(f"  [{matched_category}] ({category_counts[matched_category]}/25) {title[:60]}")
    if category_counts[matched_category] == 25: #Category just got full, sleep 2 seconds
        print(f"  '{matched_category}' is full..\n")
        time.sleep(2) #Sleep 2 seconds, if the category is full or 25 filled

os.makedirs("data", exist_ok=True) #Create data/ folder if it doesn't exist
today    = datetime.now().strftime("%Y%m%d") #Today's date for the filename
filename = f"data/trends_{today}.json"
with open(filename, "w",) as f:
    json.dump(all_stories, f, indent=2) #Write as formatted JSON
print(f"\nCollected {len(all_stories)} stories. Saved to {filename}")