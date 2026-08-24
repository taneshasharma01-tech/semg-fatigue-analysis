import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# LOAD FINAL RESULTS
# ============================================================

df = pd.read_csv("final_channel_analysis.csv")

# Sort channels
df = df.sort_values("Channel")

channels = df["Channel"].astype(str)

# ============================================================
# FIGURE 1: RMS AND MDF MEAN SLOPES
# ============================================================

x = np.arange(len(channels))
width = 0.35

plt.figure(figsize=(10, 6))

plt.bar(
    x - width/2,
    df["RMS_Mean"],
    width,
    label="RMS Slope"
)

plt.bar(
    x + width/2,
    df["MDF_Mean"],
    width,
    label="MDF Slope"
)

plt.axhline(0, linewidth=1)

plt.xticks(x, channels)
plt.xlabel("Channel")
plt.ylabel("Mean Slope")
plt.title("Mean RMS and MDF Slopes Across Channels")
plt.legend()
plt.tight_layout()

plt.savefig(
    "figure1_RMS_MDF_slopes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# FIGURE 2: PERCENTAGE SHOWING EXPECTED FATIGUE DIRECTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    x - width/2,
    df["RMS_Positive_%"],
    width,
    label="RMS Positive (%)"
)

plt.bar(
    x + width/2,
    df["MDF_Negative_%"],
    width,
    label="MDF Negative (%)"
)

plt.ylim(0, 110)

plt.xticks(x, channels)
plt.xlabel("Channel")
plt.ylabel("Subjects (%)")
plt.title("Percentage of Subjects Showing Expected Fatigue Direction")
plt.legend()
plt.tight_layout()

plt.savefig(
    "figure2_expected_fatigue_percentage.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# FIGURE 3: EFFECT SIZE (COHEN'S d)
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    x - width/2,
    df["RMS_Cohens_d"],
    width,
    label="RMS Cohen's d"
)

plt.bar(
    x + width/2,
    df["MDF_Cohens_d"],
    width,
    label="MDF Cohen's d"
)

plt.axhline(0, linewidth=1)

plt.xticks(x, channels)
plt.xlabel("Channel")
plt.ylabel("Cohen's d")
plt.title("Effect Size of Fatigue-Related Changes")
plt.legend()
plt.tight_layout()

plt.savefig(
    "figure3_effect_sizes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# FIGURE 4: FDR-CORRECTED P-VALUES
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    x - width/2,
    df["RMS_FDR_p"],
    width,
    label="RMS FDR p-value"
)

plt.bar(
    x + width/2,
    df["MDF_FDR_p"],
    width,
    label="MDF FDR p-value"
)

plt.axhline(
    0.05,
    linestyle="--",
    linewidth=1,
    label="FDR significance threshold (0.05)"
)

plt.yscale("log")

plt.xticks(x, channels)
plt.xlabel("Channel")
plt.ylabel("FDR-adjusted p-value")
plt.title("FDR-Corrected Statistical Significance")
plt.legend()
plt.tight_layout()

plt.savefig(
    "figure4_FDR_pvalues.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("VISUALIZATION COMPLETE")
print("=" * 70)

print("\nFigures saved:")

print("1. figure1_RMS_MDF_slopes.png")
print("2. figure2_expected_fatigue_percentage.png")
print("3. figure3_effect_sizes.png")
print("4. figure4_FDR_pvalues.png")

print("\nAll figures saved at 300 DPI.")
print("=" * 70)