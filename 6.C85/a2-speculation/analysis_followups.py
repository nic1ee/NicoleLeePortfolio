import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("img", exist_ok=True)

df = pd.read_csv("data/Census_and_Corp_Ownership_and_Occupancy_Over_Time.csv")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

df_2024 = df[df["Year"] == 2024].copy()

# Derived measures
df_2024["nonwhite_share"] = 1 - (df_2024["white_all"] / df_2024["tot_pop_all"])
df_2024["vacancy_rate"] = df_2024["vacant_unit"] / df_2024["tot_unit"]

# Keep relevant columns and drop missing/inf
cols = ["Neighborhood", "corp_own_rate", "nonwhite_share", "vacancy_rate"]
d = df_2024[cols].replace([np.inf, -np.inf], np.nan).dropna()

# Correlations (Pearson r)
r_vac = d["corp_own_rate"].corr(d["vacancy_rate"])
r_nw = d["corp_own_rate"].corr(d["nonwhite_share"])

print("Pearson r (corp vs vacancy):", round(r_vac, 3))
print("Pearson r (corp vs nonwhite):", round(r_nw, 3))

# Scatter + regression + labels for top outliers (vacancy)
x = d["corp_own_rate"].values
y = d["vacancy_rate"].values
m, b = np.polyfit(x, y, 1)

plt.figure()
plt.scatter(d["corp_own_rate"], d["vacancy_rate"])
plt.plot(d["corp_own_rate"], m * d["corp_own_rate"] + b)

plt.title("Corporate Ownership vs Vacancy Rate (2024) with Labeled Outliers")
plt.xlabel("corp_own_rate")
plt.ylabel("vacancy_rate")


top = d.sort_values("vacancy_rate", ascending=False).head(3)
for _, row in top.iterrows():
    plt.annotate(
        row["Neighborhood"],
        (row["corp_own_rate"], row["vacancy_rate"]),
        textcoords="offset points",
        xytext=(6, 6),
        fontsize=9
    )

plt.tight_layout()
plt.savefig("img/08_vacancy_regression_labeled_2024.png", dpi=300)
plt.close()


summary = pd.DataFrame({
    "metric": ["Pearson r: corp vs vacancy", "Pearson r: corp vs nonwhite", "slope: vacancy on corp"],
    "value": [r_vac, r_nw, m]
})
summary.to_csv("img/metrics_2024.csv", index=False)
print("Saved: img/08_vacancy_regression_labeled_2024.png and img/metrics_2024.csv")

# Group comparison: top vs bottom quartile of nonwhite_share
d2 = d.copy()
q1 = d2["nonwhite_share"].quantile(0.25)
q3 = d2["nonwhite_share"].quantile(0.75)

low = d2[d2["nonwhite_share"] <= q1]
high = d2[d2["nonwhite_share"] >= q3]

group_means = pd.DataFrame({
    "group": ["Bottom quartile nonwhite_share", "Top quartile nonwhite_share"],
    "mean_corp_own_rate": [low["corp_own_rate"].mean(), high["corp_own_rate"].mean()],
    "mean_vacancy_rate": [low["vacancy_rate"].mean(), high["vacancy_rate"].mean()]
})

print(group_means)

# Plot mean corporate ownership by group
plt.figure()
plt.bar(group_means["group"], group_means["mean_corp_own_rate"])
plt.title("Mean Corporate Ownership by Non-White Share Group (2024)")
plt.ylabel("mean corp_own_rate")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.savefig("img/09_mean_corp_by_nonwhite_group_2024.png", dpi=300)
plt.close()

print("Saved: img/09_mean_corp_by_nonwhite_group_2024.png")