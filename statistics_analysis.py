import pandas as pd
import numpy as np
from scipy import stats

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("fatigue_summary_all_subjects.csv")

# Convert channel name: "Ch 1" -> 1
df["Channel_Num"] = df["Channel"].str.extract(r"(\d+)").astype(int)

# ==========================================
# STATISTICAL ANALYSIS
# ==========================================

results = []

for ch in sorted(df["Channel_Num"].unique()):

    data = df[df["Channel_Num"] == ch]

    rms = data["RMS_Slope"].dropna()
    mdf = data["MDF_Slope"].dropna()

    n = len(rms)

    # --------------------------------------
    # RMS
    # --------------------------------------

    rms_mean = rms.mean()
    rms_sd = rms.std(ddof=1)

    rms_t, rms_p = stats.ttest_1samp(rms, 0)

    rms_ci_low, rms_ci_high = stats.t.interval(
        0.95,
        df=n-1,
        loc=rms_mean,
        scale=stats.sem(rms)
    )

    rms_cohens_d = rms_mean / rms_sd

    rms_positive = (rms > 0).sum()
    rms_positive_percent = rms_positive / n * 100

    # --------------------------------------
    # MDF
    # --------------------------------------

    mdf_mean = mdf.mean()
    mdf_sd = mdf.std(ddof=1)

    mdf_t, mdf_p = stats.ttest_1samp(mdf, 0)

    mdf_ci_low, mdf_ci_high = stats.t.interval(
        0.95,
        df=n-1,
        loc=mdf_mean,
        scale=stats.sem(mdf)
    )

    mdf_cohens_d = mdf_mean / mdf_sd

    mdf_negative = (mdf < 0).sum()
    mdf_negative_percent = mdf_negative / n * 100

    # --------------------------------------
    # Store results
    # --------------------------------------

    results.append({
        "Channel": ch,
        "N": n,

        "RMS_Mean": rms_mean,
        "RMS_SD": rms_sd,
        "RMS_CI_Low": rms_ci_low,
        "RMS_CI_High": rms_ci_high,
        "RMS_p_value": rms_p,
        "RMS_Cohens_d": rms_cohens_d,
        "RMS_Positive_%": rms_positive_percent,

        "MDF_Mean": mdf_mean,
        "MDF_SD": mdf_sd,
        "MDF_CI_Low": mdf_ci_low,
        "MDF_CI_High": mdf_ci_high,
        "MDF_p_value": mdf_p,
        "MDF_Cohens_d": mdf_cohens_d,
        "MDF_Negative_%": mdf_negative_percent
    })


# ==========================================
# CREATE RESULTS TABLE
# ==========================================

results_df = pd.DataFrame(results)

# Round for display
display_df = results_df.copy()

numeric_cols = display_df.select_dtypes(
    include=[np.number]
).columns

display_df[numeric_cols] = display_df[numeric_cols].round(4)


# ==========================================
# DISPLAY
# ==========================================

print()
print("=" * 110)
print("STATISTICAL FATIGUE ANALYSIS")
print("=" * 110)

print(display_df.to_string(index=False))


# ==========================================
# SIGNIFICANT CHANNELS
# ==========================================

print()
print("=" * 110)
print("SIGNIFICANT CHANNELS")
print("=" * 110)

for _, row in results_df.iterrows():

    rms_sig = row["RMS_p_value"] < 0.05
    mdf_sig = row["MDF_p_value"] < 0.05

    if rms_sig or mdf_sig:

        print(
            f"Ch {int(row['Channel'])}: "
            f"RMS p={row['RMS_p_value']:.4f}, "
            f"MDF p={row['MDF_p_value']:.4f}"
        )


# ==========================================
# SAVE RESULTS
# ==========================================

results_df.to_csv(
    "statistical_fatigue_analysis.csv",
    index=False
)

print()
print("=" * 110)
print("Results saved to: statistical_fatigue_analysis.csv")
print("=" * 110)