import pandas as pd
import matplotlib.pyplot as plt
import os

csv_file = "data/trends_analysed.csv"
if not os.path.exists(csv_file): #If analysed CSV missing, stop early
    print("trends_analysed.csv not found. Please run task3 first.")
    exit()

df = pd.read_csv(csv_file) #Load the analysed data
print(f"Loaded {len(df)} rows from {csv_file}")

os.makedirs("outputs", exist_ok=True) #Create outputs/ folder if it doesn't exist

top10 = df.nlargest(10, "score").copy() #Get the 10 highest-scoring stories
top10["short_title"] = top10["title"].apply(lambda t: t[:50] + "..." if len(t) > 50 else t) #Shorten long titles

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(top10["short_title"], top10["score"], color="steelblue") #Horizontal bar chart
ax1.invert_yaxis() #Highest score at the top
ax1.set_title("Top 10 Stories by Score")
ax1.set_xlabel("Score")
ax1.set_ylabel("Story Title")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png") #Save before show
plt.close()
print("Saved outputs/chart1_top_stories.png")

category_counts = df["category"].value_counts() #Count stories in each category
colors = ["steelblue", "coral", "mediumseagreen", "mediumpurple", "goldenrod"] #Different colour per bar

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
ax2.set_title("Stories per Category")
ax2.set_xlabel("Category")
ax2.set_ylabel("Number of Stories")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png") #Save before show
plt.close()
print("Saved outputs/chart2_categories.png")

popular     = df[df["is_popular"] == True]  #Popular stories (above average score)
not_popular = df[df["is_popular"] == False] #Non-popular stories

fig3, ax3 = plt.subplots(figsize=(8, 6))
ax3.scatter(not_popular["score"], not_popular["num_comments"], color="steelblue", alpha=0.6, label="Not Popular") #Blue dots for non-popular
ax3.scatter(popular["score"],     popular["num_comments"],     color="coral",     alpha=0.6, label="Popular")     #Red dots for popular
ax3.set_title("Score vs Comments")
ax3.set_xlabel("Score")
ax3.set_ylabel("Number of Comments")
ax3.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png") #Save before show
plt.close()
print("Saved outputs/chart3_scatter.png")

fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")
axes[0].barh(top10["short_title"], top10["score"], color="steelblue") #Chart 1 in dashboard
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[1].bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)]) #Chart 2 in dashboard
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], color="steelblue", alpha=0.6, label="Not Popular") #Chart 3 in dashboard
axes[2].scatter(popular["score"],     popular["num_comments"],     color="coral",     alpha=0.6, label="Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()
plt.tight_layout()
plt.savefig("outputs/dashboard.png") #Save before show
plt.close()
print("Saved outputs/dashboard.png")