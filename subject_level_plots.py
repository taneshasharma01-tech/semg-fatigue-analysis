import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# SUBJECT-LEVEL sEMG FATIGUE VISUALIZATION
# ============================================================

INPUT_FILE = "subject_level_fatigue_summary.csv"

df = pd.read_csv(INPUT_FILE)

# Sort by final rank
df = df.sort_values("Final_Rank").reset_index(drop=True)


# ============================================================
# FIGURE 6
# SUBJECT-LEVEL FATIGUE SCORES
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    df["Subject"].astype(str),
    df["Fatigue_Score"]
)

plt.xlabel("Subject")
plt.ylabel("Fatigue Score")
plt.title("Subject-Level sEMG Fatigue Scores")

plt.tight_layout()

plt.savefig(
    "figure6_subject_fatigue_scores.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# FIGURE 7
# SUBJECT-LEVEL RMS-MDF RELATIONSHIP
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    df["Mean_RMS_Slope"],
    df["Mean_MDF_Slope"],
    s=100
)

for _, row in df.iterrows():

    plt.annotate(
        f"S{int(row['Subject'])}",
        (
            row["Mean_RMS_Slope"],
            row["Mean_MDF_Slope"]
        ),
        xytext=(6, 6),
        textcoords="offset points"
    )

plt.axhline(0)
plt.axvline(0)

plt.xlabel("Mean RMS slope")
plt.ylabel("Mean MDF slope")

plt.title("Subject-Level RMS-MDF Relationship")

plt.tight_layout()

plt.savefig(
    "figure7_subject_RMS_MDF_relationship.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# FIGURE 8
# SUBJECT-LEVEL FATIGUE DIRECTION
# ============================================================

df["Expected_Direction"] = np.where(
    (df["Mean_RMS_Slope"] > 0) &
    (df["Mean_MDF_Slope"] < 0),
    "Expected",
    "Other"
)

direction_counts = df["Expected_Direction"].value_counts()

plt.figure(figsize=(8, 6))

plt.bar(
    direction_counts.index,
    direction_counts.values
)

plt.xlabel("Fatigue Direction")
plt.ylabel("Number of Subjects")
plt.title("Subject-Level Fatigue Direction")

plt.tight_layout()

plt.savefig(
    "figure8_subject_fatigue_direction.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# FIGURE 9
# FINAL SUBJECT-LEVEL RMS AND MDF SLOPES
# ============================================================

x = np.arange(len(df))
width = 0.35

plt.figure(figsize=(12, 6))

plt.bar(
    x - width / 2,
    df["Mean_RMS_Slope"],
    width,
    label="RMS slope"
)

plt.bar(
    x + width / 2,
    df["Mean_MDF_Slope"],
    width,
    label="MDF slope"
)

plt.axhline(0)

plt.xticks(
    x,
    [f"S{int(s)}" for s in df["Subject"]]
)

plt.xlabel("Subject")
plt.ylabel("Slope")
plt.title("Final Subject-Level RMS and MDF Slopes")

plt.legend()

plt.tight_layout()

plt.savefig(
    "figure9_final_RMS_MDF_slopes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# FIGURE 10
# FINAL SUBJECT-LEVEL FATIGUE RANKING
# ============================================================

ranking = df.sort_values(
    "Fatigue_Score",
    ascending=False
).reset_index(drop=True)

plt.figure(figsize=(10, 6))

plt.bar(
    [f"S{int(s)}" for s in ranking["Subject"]],
    ranking["Fatigue_Score"]
)

plt.xlabel("Subject")
plt.ylabel("Fatigue Score")
plt.title("Final Subject-Level Fatigue Ranking")

plt.tight_layout()

plt.savefig(
    "figure10_final_fatigue_ranking.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# FIGURE 11
# CONSISTENCY OF EXPECTED FATIGUE DIRECTION
# ============================================================

plt.figure(figsize=(12, 6))

x = np.arange(len(df))
width = 0.35

plt.bar(
    x - width / 2,
    df["RMS_Positive_%"],
    width,
    label="RMS positive (%)"
)

plt.bar(
    x + width / 2,
    df["MDF_Negative_%"],
    width,
    label="MDF negative (%)"
)

plt.axhline(50)

plt.xticks(
    x,
    [f"S{int(s)}" for s in df["Subject"]]
)

plt.xlabel("Subject")
plt.ylabel("Percentage of channels (%)")

plt.title("Consistency of Expected Fatigue Direction")

plt.ylim(0, 100)

plt.legend()

plt.tight_layout()

plt.savefig(
    "figure11_fatigue_direction_consistency.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# COMPLETE
# ============================================================

print("=" * 100)
print("SUBJECT-LEVEL VISUALIZATION COMPLETE")
print("=" * 100)

print("\nSaved figures:")

print("1. figure6_subject_fatigue_scores.png")
print("2. figure7_subject_RMS_MDF_relationship.png")
print("3. figure8_subject_fatigue_direction.png")
print("4. figure9_final_RMS_MDF_slopes.png")
print("5. figure10_final_fatigue_ranking.png")
print("6. figure11_fatigue_direction_consistency.png")

print("=" * 100)