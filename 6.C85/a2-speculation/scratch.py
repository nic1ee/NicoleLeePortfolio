import pandas as pd
import matplotlib.pyplot as plt

 
df = pd.read_csv("data/Census_and_Corp_Ownership_and_Occupancy_Over_Time.csv")

df_2024 = df[df["Year"] == 2024].copy()
DATA = "data/Census_and_Corp_Ownership_and_Occupancy_Over_Time.csv"

df_2024 = df[df["Year"] == 2024].copy()

top10_corp = (
    df_2024.sort_values("corp_own_rate", ascending=False)
    .head(10)
    .set_index("Neighborhood")["corp_own_rate"]
)

plt.figure()
top10_corp.sort_values().plot(kind="barh")
plt.title("Top 10 Neighborhoods by Corporate Ownership Rate (2024)")
plt.xlabel("corp_own_rate")
plt.tight_layout()
plt.show()

# next one
import os
import pandas as pd
import matplotlib.pyplot as plt

print("Running analysis...")

# Make sure img folder exists
os.makedirs("img", exist_ok=True)

# Load data
df = pd.read_csv("data/Census_and_Corp_Ownership_and_Occupancy_Over_Time.csv")

# Ensure Year is numeric
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

print("Years in dataset:", sorted(df["Year"].dropna().unique())[:5], "...", sorted(df["Year"].dropna().unique())[-5:])
print("Does 2004 exist?", (df["Year"] == 2004).any())
print("Does 2024 exist?", (df["Year"] == 2024).any())

# Filter
df_2004 = df[df["Year"] == 2004][["Neighborhood", "corp_own_rate"]].rename(
    columns={"corp_own_rate": "corp_2004"}
)
df_2024 = df[df["Year"] == 2024][["Neighborhood", "corp_own_rate"]].rename(
    columns={"corp_own_rate": "corp_2024"}
)

print("Rows in 2004:", len(df_2004))
print("Rows in 2024:", len(df_2024))

chg = df_2004.merge(df_2024, on="Neighborhood", how="inner")
print("Rows after merge:", len(chg))

if len(chg) == 0:
    print("⚠️ Merge is empty. Cannot generate Fig 2.")
else:
    chg["corp_change"] = chg["corp_2024"] - chg["corp_2004"]

    plt.figure()
    chg.sort_values("corp_change").set_index("Neighborhood")["corp_change"].plot(kind="barh")
    plt.title("Change in Corporate Ownership Rate (2004–2024)")
    plt.xlabel("Δ corp_own_rate")
    plt.tight_layout()

    outpath = "img/02_change_corp_own_2004_2024.png"
    plt.savefig(outpath, dpi=300)
    plt.close()

    print("checl Saved:", outpath)

#next
import os
import pandas as pd
import matplotlib.pyplot as plt

print("Running demographic + vacancy analysis...")

# Ensure img folder exists
os.makedirs("img", exist_ok=True)

# Load data
df = pd.read_csv("data/Census_and_Corp_Ownership_and_Occupancy_Over_Time.csv")

# Ensure numeric year
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# Filter to 2024
df_2024 = df[df["Year"] == 2024].copy()

print("Rows in 2024:", len(df_2024))

# -----------------------------
# Create derived fields
# -----------------------------

# Non-white share
df_2024["nonwhite_share"] = 1 - (
    df_2024["white_all"] / df_2024["tot_pop_all"]
)

# Vacancy rate
df_2024["vacancy_rate"] = (
    df_2024["vacant_unit"] / df_2024["tot_unit"]
)

# -----------------------------
# Plot 1: Corporate Ownership vs Nonwhite Share
# -----------------------------

plt.figure()
plt.scatter(df_2024["corp_own_rate"], df_2024["nonwhite_share"])
plt.title("Corporate Ownership vs Non-White Population Share (2024)")
plt.xlabel("corp_own_rate")
plt.ylabel("nonwhite_share")
plt.tight_layout()

plt.savefig("img/05_corp_vs_nonwhite_2024.png", dpi=300)
plt.close()

print("check Saved: 05_corp_vs_nonwhite_2024.png")

# -----------------------------
# Plot 2: Corporate Ownership vs Vacancy Rate
# -----------------------------

plt.figure()
plt.scatter(df_2024["corp_own_rate"], df_2024["vacancy_rate"])
plt.title("Corporate Ownership vs Vacancy Rate (2024)")
plt.xlabel("corp_own_rate")
plt.ylabel("vacancy_rate")
plt.tight_layout()

plt.savefig("img/06_corp_vs_vacancy_2024.png", dpi=300)
plt.close()

print("checl Saved: 06_corp_vs_vacancy_2024.png")