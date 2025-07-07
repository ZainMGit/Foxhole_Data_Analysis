import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("foxhole_war_data.csv")

# Overall average days per faction
overall_avg = df.groupby("Winner")["Days"].mean()

# Filter for wars after War 100
post_100_df = df[df["War"] > 108]
post_100_avg = post_100_df.groupby("Winner")["Days"].mean()

# Output the results
print("📊 Average Days to Win by Faction (All Wars):")
for faction, days in overall_avg.items():
    print(f"{faction}: {days:.2f} days")

print("\n📊 Average Days to Win by Faction (Wars After #108):")
for faction, days in post_100_avg.items():
    print(f"{faction}: {days:.2f} days")







# === Filter Wars Lasting More Than 20 Days ===
wars_over_20_days = df[df["Days"] > 20]



# === Filter Wars > 20 Days AND War Number > 100 ===
filtered_df = df[(df["Days"] > 25) & (df["War"] > 108)]

# === Count Wins by Faction ===
win_counts = filtered_df["Winner"].value_counts().reset_index()
win_counts.columns = ["Faction", "Wins (War > 108 and Days > 25)"]

# === Display Results ===
print("Number of Wars Won by Faction (War > 100 and Days > 20):\n")
print(win_counts)

# === Count Wins by Faction ===
win_counts_over_20 = wars_over_20_days["Winner"].value_counts().reset_index()
win_counts_over_20.columns = ["Faction", "Wins (Days > 20)"]

# === Display Results ===
print("Number of Wars Won by Faction (Only Wars > 20 Days):\n")
print(win_counts_over_20)



# Create a scatter plot with War on x-axis, Days on y-axis, and color by Winner
plt.figure(figsize=(12, 6))
faction_colors = {
    "Wardens": "blue",
    "Colonials": "green"
}

for faction in df["Winner"].unique():
    faction_data = df[df["Winner"] == faction]
    color = faction_colors.get(faction, "gray")
    plt.scatter(faction_data["War"], faction_data["Days"], label=faction, color=color, alpha=0.7)

plt.xlabel("War Number")
plt.ylabel("War Duration (Days)")
plt.title("War Duration by War Number and Winning Faction")
plt.legend(title="Winner")
plt.grid(True)
plt.tight_layout()
plt.show()
