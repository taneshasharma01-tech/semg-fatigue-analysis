import pandas as pd
import numpy as np

# ==========================================
# LOAD STATISTICAL RESULTS
# ==========================================

df = pd.read_csv("statistical_fatigue_analysis.csv")


# ==========================================
# BENJAMINI-HOCHBERG FDR CORRECTION
# ==========================================

def benjamini_hochberg(p_values):

    p_values = np.array(p_values, dtype=float)

    n = len(p_values)

    order = np.argsort(p_values)

    ranked_p = p_values[order]

    adjusted = ranked_p * n / np.arange(1, n + 1)

    # Ensure monotonicity
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]

    adjusted = np.minimum(adjusted, 1.0)

    result = np.empty(n)

    result[order] = adjusted

    return result


# ==========================================
# APPLY FDR TO ALL 16 TESTS
# ==========================================

all_p_values = np.concatenate([
    df["RMS_p_value"].values,
    df["MDF_p_value"].values
])

all_fdr = benjamini_hochberg(all_p_values)

n_channels = len(df)

df["RMS_FDR_p"] = all_fdr[:n_channels]
df["MDF_FDR_p"] = all_fdr[n_channels:]


# ==========================================
# SIGNIFICANCE AFTER FDR
# ==========================================

df["RMS_Significant_FDR"] = df["RMS_FDR_p"] < 0.05
df["MDF_Significant_FDR"] = df["MDF_FDR_p"] < 0.05

df["Both_Significant_FDR"] = (
    df["RMS_Significant_FDR"] &
    df["MDF_Significant_FDR"]
)


# ==========================================
# CREATE SIMPLE CHANNEL SCORE
# ==========================================

df["Fatigue_Biomarker_Score"] = (
    df["RMS_Significant_FDR"].astype(int)
    + df["MDF_Significant_FDR"].astype(int)
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print()
print("=" * 110)
print("FINAL CHANNEL ANALYSIS AFTER FDR CORRECTION")
print("=" * 110)

columns_to_show = [
    "Channel",
    "RMS_Mean",
    "RMS_Cohens_d",
    "RMS_p_value",
    "RMS_FDR_p",
    "MDF_Mean",
    "MDF_Cohens_d",
    "MDF_p_value",
    "MDF_FDR_p",
    "RMS_Positive_%",
    "MDF_Negative_%",
    "Fatigue_Biomarker_Score"
]

display_df = df[columns_to_show].copy()

numeric_columns = display_df.select_dtypes(
    include=[np.number]
).columns

display_df[numeric_columns] = display_df[numeric_columns].round(4)

print(display_df.to_string(index=False))


# ==========================================
# FINAL CHANNEL RANKING
# ==========================================

print()
print("=" * 110)
print("FINAL CHANNEL RANKING")
print("=" * 110)

ranking = df.sort_values(
    by=[
        "Fatigue_Biomarker_Score",
        "RMS_Cohens_d",
        "MDF_Cohens_d"
    ],
    ascending=[
        False,
        False,
        True
    ]
)

for i, (_, row) in enumerate(ranking.iterrows(), start=1):

    print(
        f"{i}. Ch {int(row['Channel'])} | "
        f"Score={row['Fatigue_Biomarker_Score']}/2 | "
        f"RMS FDR p={row['RMS_FDR_p']:.4f} | "
        f"MDF FDR p={row['MDF_FDR_p']:.4f}"
    )


# ==========================================
# FINAL INTERPRETATION
# ==========================================

print()
print("=" * 110)
print("CHANNELS SIGNIFICANT FOR BOTH RMS AND MDF")
print("=" * 110)

both = df[df["Both_Significant_FDR"]]

for _, row in both.iterrows():

    print(
        f"Ch {int(row['Channel'])}: "
        f"RMS FDR p={row['RMS_FDR_p']:.4f}, "
        f"MDF FDR p={row['MDF_FDR_p']:.4f}"
    )


# ==========================================
# SAVE FINAL RESULTS
# ==========================================

df.to_csv(
    "final_channel_analysis.csv",
    index=False
)

print()
print("=" * 110)
print("Final results saved to: final_channel_analysis.csv")
print("=" * 110)