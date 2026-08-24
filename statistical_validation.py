import pandas as pd
import numpy as np
from scipy import stats

# ============================================================
# STATISTICAL VALIDATION OF SUBJECT-LEVEL sEMG FATIGUE
# ============================================================

INPUT_FILE = "subject_level_fatigue_summary.csv"

df = pd.read_csv(INPUT_FILE)

rms = df["Mean_RMS_Slope"].dropna().values
mdf = df["Mean_MDF_Slope"].dropna().values

n = len(rms)

print("=" * 100)
print("STATISTICAL VALIDATION OF sEMG FATIGUE")
print("=" * 100)

print(f"\nNumber of subjects = {n}")


# ============================================================
# 1. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "-" * 80)
print("1. DESCRIPTIVE STATISTICS")
print("-" * 80)

print(
    f"RMS slope: Mean = {np.mean(rms):.5f}, "
    f"SD = {np.std(rms, ddof=1):.5f}, "
    f"Median = {np.median(rms):.5f}"
)

print(
    f"MDF slope: Mean = {np.mean(mdf):.5f}, "
    f"SD = {np.std(mdf, ddof=1):.5f}, "
    f"Median = {np.median(mdf):.5f}"
)


# ============================================================
# 2. ONE-SAMPLE T-TEST
#    RMS: expected > 0
#    MDF: expected < 0
# ============================================================

print("\n" + "-" * 80)
print("2. ONE-SAMPLE T-TESTS")
print("-" * 80)

# Two-sided test first
rms_t, rms_p_two = stats.ttest_1samp(rms, 0)
mdf_t, mdf_p_two = stats.ttest_1samp(mdf, 0)

# Convert to one-sided according to expected direction
if rms_t > 0:
    rms_p_one = rms_p_two / 2
else:
    rms_p_one = 1 - rms_p_two / 2

if mdf_t < 0:
    mdf_p_one = mdf_p_two / 2
else:
    mdf_p_one = 1 - mdf_p_two / 2

print(f"RMS: t = {rms_t:.4f}, one-sided p = {rms_p_one:.6f}")
print(f"MDF: t = {mdf_t:.4f}, one-sided p = {mdf_p_one:.6f}")

if rms_p_one < 0.05:
    print("RMS interpretation: Significant positive slope across subjects.")
else:
    print("RMS interpretation: Not statistically significant.")

if mdf_p_one < 0.05:
    print("MDF interpretation: Significant negative slope across subjects.")
else:
    print("MDF interpretation: Not statistically significant.")


# ============================================================
# 3. WILCOXON SIGNED-RANK TEST
#    Non-parametric confirmation
# ============================================================

print("\n" + "-" * 80)
print("3. WILCOXON SIGNED-RANK TESTS")
print("-" * 80)

try:
    rms_w, rms_wp = stats.wilcoxon(
        rms,
        alternative="greater"
    )

    mdf_w, mdf_wp = stats.wilcoxon(
        mdf,
        alternative="less"
    )

    print(f"RMS: W = {rms_w:.4f}, one-sided p = {rms_wp:.6f}")
    print(f"MDF: W = {mdf_w:.4f}, one-sided p = {mdf_wp:.6f}")

except ValueError as e:
    print("Wilcoxon test could not be calculated:", e)


# ============================================================
# 4. EFFECT SIZE: COHEN'S d
# ============================================================

print("\n" + "-" * 80)
print("4. EFFECT SIZE")
print("-" * 80)

rms_sd = np.std(rms, ddof=1)
mdf_sd = np.std(mdf, ddof=1)

rms_d = np.mean(rms) / rms_sd
mdf_d = np.mean(mdf) / mdf_sd

print(f"RMS Cohen's d = {rms_d:.4f}")
print(f"MDF Cohen's d = {mdf_d:.4f}")

def effect_interpretation(d):
    d_abs = abs(d)

    if d_abs < 0.2:
        return "negligible"
    elif d_abs < 0.5:
        return "small"
    elif d_abs < 0.8:
        return "medium"
    else:
        return "large"

print(f"RMS effect: {effect_interpretation(rms_d)}")
print(f"MDF effect: {effect_interpretation(mdf_d)}")


# ============================================================
# 5. 95% CONFIDENCE INTERVALS
# ============================================================

print("\n" + "-" * 80)
print("5. 95% CONFIDENCE INTERVALS")
print("-" * 80)

rms_mean = np.mean(rms)
mdf_mean = np.mean(mdf)

rms_sem = stats.sem(rms)
mdf_sem = stats.sem(mdf)

rms_ci = stats.t.interval(
    0.95,
    df=n - 1,
    loc=rms_mean,
    scale=rms_sem
)

mdf_ci = stats.t.interval(
    0.95,
    df=n - 1,
    loc=mdf_mean,
    scale=mdf_sem
)

print(
    f"RMS mean = {rms_mean:.5f} "
    f"(95% CI: {rms_ci[0]:.5f} to {rms_ci[1]:.5f})"
)

print(
    f"MDF mean = {mdf_mean:.5f} "
    f"(95% CI: {mdf_ci[0]:.5f} to {mdf_ci[1]:.5f})"
)


# ============================================================
# 6. DIRECTIONAL CONSISTENCY
# ============================================================

print("\n" + "-" * 80)
print("6. DIRECTIONAL CONSISTENCY")
print("-" * 80)

rms_positive = np.sum(rms > 0)
mdf_negative = np.sum(mdf < 0)

rms_percentage = rms_positive / n * 100
mdf_percentage = mdf_negative / n * 100

print(
    f"Subjects with RMS slope > 0: "
    f"{rms_positive}/{n} ({rms_percentage:.1f}%)"
)

print(
    f"Subjects with MDF slope < 0: "
    f"{mdf_negative}/{n} ({mdf_percentage:.1f}%)"
)


# ============================================================
# 7. RMS-MDF CORRELATION
# ============================================================

print("\n" + "-" * 80)
print("7. RMS-MDF CORRELATION")
print("-" * 80)

pearson_r, pearson_p = stats.pearsonr(rms, mdf)

spearman_r, spearman_p = stats.spearmanr(rms, mdf)

print(
    f"Pearson r = {pearson_r:.4f}, "
    f"p = {pearson_p:.6f}"
)

print(
    f"Spearman rho = {spearman_r:.4f}, "
    f"p = {spearman_p:.6f}"
)


# ============================================================
# 8. SUBJECTS WITH STRONGEST RESPONSE
# ============================================================

print("\n" + "-" * 80)
print("8. TOP FATIGUE-SENSITIVE SUBJECTS")
print("-" * 80)

top = df.sort_values(
    "Fatigue_Score",
    ascending=False
).head(5)

for _, row in top.iterrows():

    print(
        f"Subject {int(row['Subject'])}: "
        f"Fatigue Score = {row['Fatigue_Score']:.5f}, "
        f"RMS = {row['Mean_RMS_Slope']:.5f}, "
        f"MDF = {row['Mean_MDF_Slope']:.5f}"
    )


# ============================================================
# 9. SAVE STATISTICAL SUMMARY
# ============================================================

summary = pd.DataFrame({
    "Metric": [
        "Number of subjects",
        "Mean RMS slope",
        "Mean MDF slope",
        "RMS one-sided t-test p",
        "MDF one-sided t-test p",
        "RMS Cohen d",
        "MDF Cohen d",
        "RMS positive subjects (%)",
        "MDF negative subjects (%)",
        "Pearson r",
        "Pearson p",
        "Spearman rho",
        "Spearman p"
    ],
    "Value": [
        n,
        rms_mean,
        mdf_mean,
        rms_p_one,
        mdf_p_one,
        rms_d,
        mdf_d,
        rms_percentage,
        mdf_percentage,
        pearson_r,
        pearson_p,
        spearman_r,
        spearman_p
    ]
})

summary.to_csv(
    "statistical_validation_summary.csv",
    index=False
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 100)
print("STATISTICAL VALIDATION COMPLETE")
print("=" * 100)

print("\nSaved:")
print("1. statistical_validation_summary.csv")