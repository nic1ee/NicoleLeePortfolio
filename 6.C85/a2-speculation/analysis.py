import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("Running vacancy regression analysis...")

# Ensure img folder exists
os.makedirs("img", exist_ok=True)

# Load data
df = pd.read_csv("data/Census_and_Corp_Ownership_and_Occupancy_Over_Time.csv")

# Ensure Year numeric
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# Filter to 2024
df_2024 = df[df["Year"] == 2024].copy()

# Create vacancy rate
df_2024["vacancy_rate"] = (
    df_2024["vacant_unit"] / df_2024["tot_unit"]
)

# Drop missing values just in case
df_2024 = df_2024.dropna(subset=["corp_own_rate", "vacancy_rate"])

# -----------------------------
# Scatter + Regression Line
# -----------------------------

x = df_2024["corp_own_rate"]
y = df_2024["vacancy_rate"]

# Fit linear regression line
m, b = np.polyfit(x, y, 1)
reg_line = m * x + b

plt.figure()
plt.scatter(x, y)
plt.plot(x, reg_line)  # regression line

plt.title("Corporate Ownership vs Vacancy Rate (2024)")
plt.xlabel("corp_own_rate")
plt.ylabel("vacancy_rate")
plt.tight_layout()

plt.savefig("img/07_corp_vs_vacancy_regression_2024.png", dpi=300)
plt.close()

print("✅ Saved: 07_corp_vs_vacancy_regression_2024.png")
print(f"Slope: {m:.4f}")