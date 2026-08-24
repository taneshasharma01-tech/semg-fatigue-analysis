import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# SUBJECT-LEVEL sEMG FATIGUE VISUALIZATION
# ============================================================

INPUT_FILE = "subject_level_fatigue_summary.csv"

df = pd.read_csv(INPUT_FILE)

# Sort by fatigue score
df = df.sort_values("Fatigue_Score", ascending=False).reset_index(drop=True)

subjects = df["Subject"].astype(str)

# ------------------------------------------------------------
# FIGURE 1: Fatigue Score by Subject
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.bar(subjects, df["Fatigue_Score"])

plt.xlabel("Subject")
plt.ylabel("Fatigue Score")
plt.title("Subject-Level sEMG Fatigue Score")

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "figure6_subject_fatigue_scores.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# FIGURE 2: RMS vs MDF Fatigue Slopes
# ------------------------------------------------------------

plt.figure(figsize=(10, 7))

plt.scatter(
    df["Mean_RMS_Slope"],
    df["Mean_MDF_Slope"],
    s=80
)

for _, row in df.iterrows():
    plt.annotate(
        f"S{int(row['Subject'])}",
        (row["Mean_RMS_Slope"], row["Mean_MDF_Slope"]),
        xytext=(5, 5),
        textcoords="offset points"
    )

plt.axhline(0, linewidth=1)
plt.axvline(0, linewidth=1)

plt.xlabel("Mean RMS Slope")
plt.ylabel("Mean MDF Slope")
plt.title("Subject-Level RMS vs MDF Fatigue Slopes")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "figure7_subject_RMS_MDF_relationship.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# FIGURE 3: Expected Fatigue Direction
# ------------------------------------------------------------

x = np.arange(len(df))
width = 0.35

plt.figure(figsize=(13, 6))

plt.bar(
    x - width / 2,
    df["RMS_Positive_%"],
    width,
    label="RMS Positive (%)"
)

plt.bar(
    x + width / 2,
    df["MDF_Negative_%"],
    width,
    label="MDF Negative (%)"
)

plt.xticks(x, subjects)

plt.xlabel("Subject")
plt.ylabel("Subjects/Channels Showing Expected Direction (%)")
plt.title("Consistency of Expected Fatigue Direction")

plt.ylim(0, 110)
plt.legend()

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "figure8_subject_fatigue_direction.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# TOP 5 SUBJECTS
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("TOP 5 FATIGUE-SENSITIVE SUBJECTS")
print("=" * 80)

top5 = df.head(5)

for _, row in top5.iterrows():

    print(
        f"Subject {int(row['Subject'])} | "
        f"Fatigue Score = {row['Fatigue_Score']:.4f} | "
        f"RMS slope = {row['Mean_RMS_Slope']:.5f} | "
        f"MDF slope = {row['Mean_MDF_Slope']:.5f}"
    )


print("\n" + "=" * 80)
print("SUBJECT-LEVEL VISUALIZATION COMPLETE")
print("=" * 80)

print("\nFigures saved:")
print("1. figure6_subject_fatigue_scores.png")
print("2. figure7_subject_RMS_MDF_relationship.png")
print("3. figure8_subject_fatigue_direction.png")