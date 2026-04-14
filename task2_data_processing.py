import pandas as pd
import glob
import os
json_files = glob.glob("data/trends_*.json") #Search for any file matching trends_*.json
if not json_files: #If no file found, stop early
    print("No JSON file found in data/ folder. Please run task1 first.")
    exit()
json_file = sorted(json_files)[-1] #Pick the most recent file if there are multiple
df = pd.read_json(json_file) #Load the JSON into a DataFrame
print(f"Loaded {len(df)} rows from {json_file}")

df = df.drop_duplicates(subset="post_id") #Remove duplicate stories by post_id
print(f"\nAfter removing duplicates: {len(df)}")
df = df.dropna(subset=["post_id", "title", "score"]) #Drop rows missing post_id, title or score
print(f"After removing nulls: {len(df)}")
df["score"]        = df["score"].astype(int) #Convert score to integer
df["num_comments"] = df["num_comments"].astype(int) #Convert num_comments to integer
df = df[df["score"] >= 5] #Remove stories with score below 5 (low quality)
print(f"After removing low scores: {len(df)}")
df["title"] = df["title"].str.strip() #Strip extra whitespace from titles

os.makedirs("data", exist_ok=True) #Create data/ folder if it doesn't exist
csv_file = "data/trends_clean.csv"
df.to_csv(csv_file, index=False) #index=False so row numbers don't get saved
print(f"\nSaved {len(df)} rows to {csv_file}")
print("\nStories per category:") #Quick summary of stories per category
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    print(f"  {category:<20} {count}")