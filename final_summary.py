import pandas as pd

# ============================================================
# FINAL sEMG FATIGUE SUMMARY
# ============================================================

INPUT_FILE = "final_channel_analysis.csv"
OUTPUT_FILE = "final_fatigue_summary.csv"

# Load final results
df = pd.read_csv(INPUT_FILE)

# ------------------------------------------------------------
# Channel labels
# IMPORTANT:
# Only Channel 4 is explicitly identified as Pronator Teres
# in the original dataset paper.
# ------------------------------------------------------------

channel_labels = {
    1: "Channel 1",
    2: "Channel 2",
    3: "Channel 3",
    4: "Pronator Teres (Ch 4)",
    5: "Channel 5",
    6: "Channel 6",
    7: "Channel 7",
    8: "Channel 8"
}

df["Label"] = df["Channel"].map(channel_labels)

# ------------------------------------------------------------
# Significance after FDR correction
# ------------------------------------------------------------

df["RMS_Significant"] = df["RMS_FDR_p"] < 0.05
df["MDF_Significant"] = df["MDF_FDR_p"] < 0.05

def significance(row):

    rms = row["RMS_Significant"]
    mdf = row["MDF_Significant"]

    if rms and mdf:
        return "Both RMS + MDF"

    elif rms:
        return "RMS only"

    elif mdf:
        return "MDF only"

    else:
        return "Neither"

df["Significance"] = df.apply(significance, axis=1)

# ------------------------------------------------------------
# Fatigue direction
# ------------------------------------------------------------

def fatigue_direction(row):

    rms_positive = row["RMS_Mean"] > 0
    mdf_negative = row["MDF_Mean"] < 0

    if rms_positive and mdf_negative:
        return "Expected: RMS ↑ + MDF ↓"

    elif rms_positive:
        return "RMS ↑ only"

    elif mdf_negative:
        return "MDF ↓ only"

    else:
        return "Unexpected direction"

df["Fatigue_Direction"] = df.apply(fatigue_direction, axis=1)

# ------------------------------------------------------------
# Ranking
# ------------------------------------------------------------

df = df.sort_values(
    by=["Fatigue_Biomarker_Score", "RMS_FDR_p", "MDF_FDR_p"],
    ascending=[False, True, True]
).reset_index(drop=True)

df["Final_Rank"] = range(1, len(df) + 1)

# ------------------------------------------------------------
# Select useful columns
# ------------------------------------------------------------

summary = df[
    [
        "Final_Rank",
        "Channel",
        "Label",
        "RMS_Mean",
        "MDF_Mean",
        "RMS_Cohens_d",
        "MDF_Cohens_d",
        "RMS_FDR_p",
        "MDF_FDR_p",
        "RMS_Positive_%",
        "MDF_Negative_%",
        "Fatigue_Biomarker_Score",
        "Significance",
        "Fatigue_Direction"
    ]
]

# Save
summary.to_csv(OUTPUT_FILE, index=False)

# ------------------------------------------------------------
# Print final report
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("FINAL sEMG FATIGUE SUMMARY")
print("=" * 100)

print(summary.to_string(index=False))

print("\n" + "=" * 100)
print("CHANNELS SIGNIFICANT FOR BOTH RMS AND MDF")
print("=" * 100)

both = summary[
    summary["Significance"] == "Both RMS + MDF"
]

for _, row in both.iterrows():

    print(
        f"Rank {int(row['Final_Rank'])}: "
        f"{row['Label']} | "
        f"RMS FDR p={row['RMS_FDR_p']:.4f} | "
        f"MDF FDR p={row['MDF_FDR_p']:.4f} | "
        f"Score={int(row['Fatigue_Biomarker_Score'])}/2"
    )

print("\n" + "=" * 100)
print("EXPECTED FATIGUE DIRECTION")
print("=" * 100)

expected = summary[
    summary["Fatigue_Direction"] == "Expected: RMS ↑ + MDF ↓"
]

print(
    f"{len(expected)} / {len(summary)} channels "
    f"show RMS increase + MDF decrease."
)

print("\n" + "=" * 100)
print(f"Saved to: {OUTPUT_FILE}")
print("=" * 100)