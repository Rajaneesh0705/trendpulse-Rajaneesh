import pandas as pd
import numpy as np
import os

csv_file = "data/trends_clean.csv"
if not os.path.exists(csv_file): #If clean CSV missing, stop early
    print("trends_clean.csv not found. Please run task2 first.")
    exit()

df = pd.read_csv(csv_file) #Load the cleaned CSV into a DataFrame
print(f"Loaded data: {df.shape}") #Print (rows, columns)
print("\nFirst 5 rows:")
print(df.head()) #Quick peek at the data

avg_score    = df["score"].mean() #Average score across all stories
avg_comments = df["num_comments"].mean() #Average comments across all stories
print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

scores = df["score"].to_numpy() #Convert score column to NumPy array for stats

mean_score   = np.mean(scores)   #Mean of all scores
median_score = np.median(scores) #Middle value when sorted
std_score    = np.std(scores)    #How spread out the scores are
max_score    = np.max(scores)    #Highest score
min_score    = np.min(scores)    #Lowest score

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:,.0f}")
print(f"Median score : {median_score:,.0f}")
print(f"Std deviation: {std_score:,.0f}")
print(f"Max score    : {max_score:,.0f}")
print(f"Min score    : {min_score:,.0f}")

top_category       = df["category"].value_counts().idxmax() #Category with most stories
top_category_count = df["category"].value_counts().max()
print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

most_commented_idx   = df["num_comments"].idxmax() #Row index of the most commented story
most_commented_story = df.loc[most_commented_idx]  #Pull out that row
print(f'\nMost commented story: "{most_commented_story["title"]}"  — {most_commented_story["num_comments"]} comments')

df["engagement"] = df["num_comments"] / (df["score"] + 1) #Discussion per upvote (+1 avoids division by zero)
df["is_popular"] = df["score"] > avg_score                #True if above average score

os.makedirs("data", exist_ok=True) #Create data/ folder if it doesn't exist
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False) #Save with new columns, no row numbers
print(f"\nSaved to {output_file}")