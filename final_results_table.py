import pandas as pd
from pathlib import Path

print("=" * 100)
print("FINAL CONSOLIDATED sEMG FATIGUE RESULTS")
print("=" * 100)

# ---------------------------------------------------------
# 1. Load subject-level summary
# ---------------------------------------------------------

subject_file = Path("subject_level_fatigue_summary.csv")

if not subject_file.exists():
    print(f"\nERROR: {subject_file} not found.")
    print("Run subject_level_analysis.py first.")
    raise SystemExit

df = pd.read_csv(subject_file)

print(f"\nLoaded {len(df)} subjects.")

# ---------------------------------------------------------
# 2. Select and standardize important columns
# ---------------------------------------------------------

required_columns = [
    "Subject",
    "Mean_RMS_Slope",
    "Mean_MDF_Slope",
    "RMS_Positive_%",
    "MDF_Negative_%",
    "Direction_Score",
    "Combined_Fatigue_Magnitude",
    "Fatigue_Score"
]

missing = [c for c in required_columns if c not in df.columns]

if missing:
    print("\nERROR: Missing columns:")
    for c in missing:
        print(" -", c)
    print("\nAvailable columns:")
    print(list(df.columns))
    raise SystemExit

final_df = df[required_columns].copy()

# ---------------------------------------------------------
# 3. Add expected-direction labels
# ---------------------------------------------------------

final_df["RMS_Direction"] = final_df["Mean_RMS_Slope"].apply(
    lambda x: "Expected ↑" if x > 0 else "Not expected"
)

final_df["MDF_Direction"] = final_df["Mean_MDF_Slope"].apply(
    lambda x: "Expected ↓" if x < 0 else "Not expected"
)

# ---------------------------------------------------------
# 4. Rank subjects by fatigue score
# ---------------------------------------------------------

final_df = final_df.sort_values(
    by="Fatigue_Score",
    ascending=False
).reset_index(drop=True)

final_df.insert(0, "Final_Rank", range(1, len(final_df) + 1))

# ---------------------------------------------------------
# 5. Print final table
# ---------------------------------------------------------

print("\n" + "=" * 100)
print("FINAL SUBJECT-LEVEL RESULTS")
print("=" * 100)

display_columns = [
    "Final_Rank",
    "Subject",
    "Mean_RMS_Slope",
    "Mean_MDF_Slope",
    "RMS_Direction",
    "MDF_Direction",
    "RMS_Positive_%",
    "MDF_Negative_%",
    "Fatigue_Score"
]

print(
    final_df[display_columns].to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)

# ---------------------------------------------------------
# 6. Save consolidated CSV
# ---------------------------------------------------------

output_file = "FINAL_CONSOLIDATED_RESULTS.csv"

final_df.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# 7. Overall summary
# ---------------------------------------------------------

rms_expected = (final_df["Mean_RMS_Slope"] > 0).sum()
mdf_expected = (final_df["Mean_MDF_Slope"] < 0).sum()

print("\n" + "=" * 100)
print("OVERALL SUMMARY")
print("=" * 100)

print(f"Total subjects analyzed       : {len(final_df)}")
print(f"RMS ↑ expected direction      : {rms_expected}/{len(final_df)}")
print(f"MDF ↓ expected direction      : {mdf_expected}/{len(final_df)}")

print(
    f"Mean RMS slope                : "
    f"{final_df['Mean_RMS_Slope'].mean():.5f}"
)

print(
    f"Mean MDF slope                : "
    f"{final_df['Mean_MDF_Slope'].mean():.5f}"
)

print("\nTop 5 fatigue-sensitive subjects:")

for _, row in final_df.head(5).iterrows():
    print(
        f"Rank {int(row['Final_Rank'])}: "
        f"Subject {int(row['Subject'])} | "
        f"Fatigue Score = {row['Fatigue_Score']:.5f} | "
        f"RMS = {row['Mean_RMS_Slope']:.5f} | "
        f"MDF = {row['Mean_MDF_Slope']:.5f}"
    )

print("\n" + "=" * 100)
print("FINAL RESULTS TABLE CREATED")
print("=" * 100)

print(f"\nSaved file:")
print(f"1. {output_file}")