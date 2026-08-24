import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# FINAL RESULTS VISUALIZATION
# ============================================================

INPUT_FILE = "FINAL_CONSOLIDATED_RESULTS.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 90)
print("FINAL sEMG FATIGUE RESULTS VISUALIZATION")
print("=" * 90)

# Sort by fatigue rank
df = df.sort_values("Final_Rank").reset_index(drop=True)


# ------------------------------------------------------------
# Figure 9: RMS and MDF slopes across subjects
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(df))

ax.plot(
    x,
    df["Mean_RMS_Slope"],
    marker="o",
    linewidth=2,
    label="RMS slope"
)

ax.plot(
    x,
    df["Mean_MDF_Slope"],
    marker="o",
    linewidth=2,
    label="MDF slope"
)

ax.axhline(0, linewidth=1)

ax.set_xticks(x)
ax.set_xticklabels(
    [f"S{int(s)}" for s in df["Subject"]]
)

ax.set_xlabel("Subject")
ax.set_ylabel("Mean Fatigue Slope")
ax.set_title("Subject-Level RMS and MDF Fatigue Slopes")

ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "figure9_final_RMS_MDF_slopes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# Figure 10: Fatigue score ranking
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 7))

subjects = [f"S{int(s)}" for s in df["Subject"]]
scores = df["Fatigue_Score"]

bars = ax.bar(subjects, scores)

# Highlight top 5
for i, bar in enumerate(bars):
    if i < 5:
        bar.set_alpha(1.0)
    else:
        bar.set_alpha(0.5)

ax.set_xlabel("Subject")
ax.set_ylabel("Fatigue Score")
ax.set_title("Subject-Level sEMG Fatigue Score Ranking")

ax.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "figure10_final_fatigue_ranking.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# Figure 11: RMS positive vs MDF negative consistency
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 7))

width = 0.35
x = np.arange(len(df))

ax.bar(
    x - width / 2,
    df["RMS_Positive_%"],
    width,
    label="RMS Positive (%)"
)

ax.bar(
    x + width / 2,
    df["MDF_Negative_%"],
    width,
    label="MDF Negative (%)"
)

ax.set_xticks(x)

ax.set_xticklabels(
    [f"S{int(s)}" for s in df["Subject"]]
)

ax.set_ylim(0, 110)

ax.set_xlabel("Subject")
ax.set_ylabel("Consistency (%)")
ax.set_title("Consistency of Expected Fatigue Direction")

ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "figure11_fatigue_direction_consistency.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# Print final summary
# ------------------------------------------------------------

print("\n" + "=" * 90)
print("FINAL VISUALIZATION SUMMARY")
print("=" * 90)

print(f"\nSubjects analyzed: {len(df)}")

print(
    f"Mean RMS slope: "
    f"{df['Mean_RMS_Slope'].mean():.5f}"
)

print(
    f"Mean MDF slope: "
    f"{df['Mean_MDF_Slope'].mean():.5f}"
)

print(
    f"Subjects with 100% channel-wise RMS increase: "
    f"{(df['RMS_Positive_%'] == 100).sum()}/{len(df)}"
)

print(
    f"Subjects with 100% channel-wise MDF decrease: "
    f"{(df['MDF_Negative_%'] == 100).sum()}/{len(df)}"
)

print(
    f"Mean RMS channel-wise consistency: "
    f"{df['RMS_Positive_%'].mean():.1f}%"
)

print(
    f"Mean MDF channel-wise consistency: "
    f"{df['MDF_Negative_%'].mean():.1f}%"
)


# ------------------------------------------------------------
# Top 5 fatigue-sensitive subjects
# ------------------------------------------------------------

print("\nTop 5 fatigue-sensitive subjects:")

for _, row in df.head(5).iterrows():

    print(
        f"Rank {int(row['Final_Rank'])}: "
        f"Subject {int(row['Subject'])} | "
        f"Fatigue Score = {row['Fatigue_Score']:.5f}"
    )


# ------------------------------------------------------------
# Completion message
# ------------------------------------------------------------

print("\n" + "=" * 90)
print("FINAL VISUALIZATION COMPLETE")
print("=" * 90)

print("\nFigures saved:")
print("1. figure9_final_RMS_MDF_slopes.png")
print("2. figure10_final_fatigue_ranking.png")
print("3. figure11_fatigue_direction_consistency.png")