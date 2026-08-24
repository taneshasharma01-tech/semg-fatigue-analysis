import pandas as pd
import numpy as np

# Load results
df = pd.read_csv("fatigue_summary_all_subjects.csv")

# Convert Channel number from "Ch 1" -> 1
df["Channel_Num"] = df["Channel"].str.extract(r"(\d+)").astype(int)

# ==========================================
# CHANNEL-WISE GROUP SUMMARY
# ==========================================

summary = df.groupby("Channel_Num").agg(
    Mean_RMS_Slope=("RMS_Slope", "mean"),
    Mean_RMS_R2=("RMS_R2", "mean"),
    Mean_MDF_Slope=("MDF_Slope", "mean"),
    Mean_MDF_R2=("MDF_R2", "mean"),
    RMS_Positive_Count=("RMS_Slope", lambda x: (x > 0).sum()),
    MDF_Negative_Count=("MDF_Slope", lambda x: (x < 0).sum()),
    Total_Subjects=("Subject", "nunique")
).reset_index()

# ==========================================
# PERCENTAGE
# ==========================================

summary["RMS_Positive_%"] = (
    summary["RMS_Positive_Count"]
    / summary["Total_Subjects"] * 100
)

summary["MDF_Negative_%"] = (
    summary["MDF_Negative_Count"]
    / summary["Total_Subjects"] * 100
)

# ==========================================
# DISPLAY RESULTS
# ==========================================

print()
print("=" * 90)
print("CHANNEL-WISE FATIGUE SUMMARY")
print("=" * 90)

print(summary.round(4).to_string(index=False))

# ==========================================
# SAVE RESULTS
# ==========================================

summary.to_csv(
    "channel_wise_fatigue_summary.csv",
    index=False
)

print()
print("Summary saved to: channel_wise_fatigue_summary.csv")