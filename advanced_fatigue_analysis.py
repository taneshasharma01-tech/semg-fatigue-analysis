import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# ============================================================
# ADVANCED sEMG FATIGUE ANALYSIS
# ============================================================

INPUT_FILE = "final_channel_analysis.csv"

df = pd.read_csv(INPUT_FILE)

# ------------------------------------------------------------
# Rename score column for easier use
# ------------------------------------------------------------

df["Score"] = df["Fatigue_Biomarker_Score"]

# ------------------------------------------------------------
# Significance classification
# ------------------------------------------------------------

df["RMS_Significant"] = df["RMS_FDR_p"] < 0.05
df["MDF_Significant"] = df["MDF_FDR_p"] < 0.05

def classify(row):

    if row["RMS_Significant"] and row["MDF_Significant"]:
        return "Strong: RMS + MDF"

    elif row["RMS_Significant"]:
        return "Partial: RMS only"

    elif row["MDF_Significant"]:
        return "Partial: MDF only"

    else:
        return "Not significant"

df["Classification"] = df.apply(classify, axis=1)

# ------------------------------------------------------------
# Absolute effect sizes
# ------------------------------------------------------------

df["Abs_RMS_d"] = df["RMS_Cohens_d"].abs()
df["Abs_MDF_d"] = df["MDF_Cohens_d"].abs()

# Combined effect size
df["Combined_Effect_Size"] = (
    df["Abs_RMS_d"] + df["Abs_MDF_d"]
) / 2

# ------------------------------------------------------------
# Direction consistency
# ------------------------------------------------------------

df["Expected_Direction"] = (
    (df["RMS_Mean"] > 0) &
    (df["MDF_Mean"] < 0)
)

# ------------------------------------------------------------
# RMS-MDF correlation across channels
# ------------------------------------------------------------

r, p = pearsonr(
    df["RMS_Mean"],
    df["MDF_Mean"]
)

# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("ADVANCED sEMG FATIGUE ANALYSIS")
print("=" * 100)

print("\nRMS vs MDF slope correlation")
print("-" * 100)

print(f"Pearson r = {r:.4f}")
print(f"p-value   = {p:.4f}")

if p < 0.05:
    print("Interpretation: significant association between RMS and MDF slopes.")
else:
    print("Interpretation: no statistically significant association detected.")

# ------------------------------------------------------------
# Effect-size ranking
# ------------------------------------------------------------

effect_rank = df.sort_values(
    "Combined_Effect_Size",
    ascending=False
).reset_index(drop=True)

effect_rank["Effect_Rank"] = range(1, len(effect_rank) + 1)

print("\n" + "=" * 100)
print("EFFECT-SIZE RANKING")
print("=" * 100)

for _, row in effect_rank.iterrows():

    print(
        f"{int(row['Effect_Rank'])}. "
        f"Ch {int(row['Channel'])} | "
        f"RMS |d|={row['Abs_RMS_d']:.3f} | "
        f"MDF |d|={row['Abs_MDF_d']:.3f} | "
        f"Combined={row['Combined_Effect_Size']:.3f} | "
        f"{row['Classification']}"
    )

# ------------------------------------------------------------
# Strongest channels
# ------------------------------------------------------------

strong = df[
    (df["RMS_Significant"]) &
    (df["MDF_Significant"]) &
    (df["Expected_Direction"])
].copy()

strong = strong.sort_values(
    "Combined_Effect_Size",
    ascending=False
)

print("\n" + "=" * 100)
print("STRONG FATIGUE-SENSITIVE CHANNELS")
print("=" * 100)

for _, row in strong.iterrows():

    print(
        f"Ch {int(row['Channel'])}: "
        f"RMS slope={row['RMS_Mean']:.4f}, "
        f"MDF slope={row['MDF_Mean']:.4f}, "
        f"RMS d={row['RMS_Cohens_d']:.3f}, "
        f"MDF d={row['MDF_Cohens_d']:.3f}"
    )

# ------------------------------------------------------------
# Scatter plot
# ------------------------------------------------------------

plt.figure(figsize=(8, 6))

plt.scatter(
    df["RMS_Mean"],
    df["MDF_Mean"],
    s=100
)

for _, row in df.iterrows():

    plt.annotate(
        f"Ch {int(row['Channel'])}",
        (
            row["RMS_Mean"],
            row["MDF_Mean"]
        ),
        xytext=(6, 6),
        textcoords="offset points"
    )

plt.axhline(0)
plt.axvline(0)

plt.xlabel("Mean RMS slope")
plt.ylabel("Mean MDF slope")

plt.title(
    f"Relationship Between RMS and MDF Fatigue Slopes\n"
    f"Pearson r = {r:.3f}, p = {p:.4f}"
)

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "figure5_RMS_MDF_relationship.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ------------------------------------------------------------
# Save advanced results
# ------------------------------------------------------------

df.to_csv(
    "advanced_fatigue_analysis.csv",
    index=False
)

effect_rank.to_csv(
    "effect_size_ranking.csv",
    index=False
)

print("\n" + "=" * 100)
print("ANALYSIS COMPLETE")
print("=" * 100)

print("Saved:")
print("1. advanced_fatigue_analysis.csv")
print("2. effect_size_ranking.csv")
print("3. figure5_RMS_MDF_relationship.png")

print("=" * 100)