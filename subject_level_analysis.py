import os
import glob
import numpy as np
import pandas as pd
from scipy import signal
from scipy.stats import linregress

# ============================================================
# SUBJECT-LEVEL sEMG FATIGUE ANALYSIS
# ============================================================

DATA_DIR = "Dataset EMG Fatigue"

FS = 200                 # Sampling frequency
EPOCH_SECONDS = 1        # 1-second epochs
EPOCH_SAMPLES = FS * EPOCH_SECONDS

N_CHANNELS = 8
EXPECTED_DURATION = 120  # seconds


# ============================================================
# RMS
# ============================================================

def calculate_rms(x):
    return np.sqrt(np.mean(x ** 2))


# ============================================================
# MDF
# ============================================================

def calculate_mdf(x, fs):
    """
    Calculate Median Frequency from the power spectrum.
    """

    freqs, psd = signal.welch(
        x,
        fs=fs,
        nperseg=min(len(x), fs),
        noverlap=0
    )

    cumulative_power = np.cumsum(psd)
    total_power = cumulative_power[-1]

    if total_power == 0:
        return np.nan

    median_index = np.where(
        cumulative_power >= total_power / 2
    )[0]

    if len(median_index) == 0:
        return np.nan

    return freqs[median_index[0]]


# ============================================================
# READ NUMERIC DATA FROM TXT
# ============================================================

def load_subject_file(filepath):

    numeric_rows = []

    with open(filepath, "r", errors="ignore") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            # Try whitespace-separated values
            parts = line.replace(",", " ").split()

            try:
                values = [float(v) for v in parts]
            except ValueError:
                continue

            # We need at least 8 numeric values
            if len(values) >= N_CHANNELS:
                numeric_rows.append(values[:N_CHANNELS])

    if len(numeric_rows) == 0:
        raise ValueError(f"No numeric data found in {filepath}")

    data = np.array(numeric_rows, dtype=float)

    return data


# ============================================================
# FIND SUBJECT FILES
# ============================================================

files = glob.glob(
    os.path.join(DATA_DIR, "**", "*.txt"),
    recursive=True
)

# Remove README files
files = [
    f for f in files
    if "read" not in os.path.basename(f).lower()
]

if len(files) == 0:

    raise FileNotFoundError(
        "No subject TXT files found inside Dataset EMG Fatigue."
    )


print("=" * 100)
print("SUBJECT-LEVEL sEMG FATIGUE ANALYSIS")
print("=" * 100)

print(f"\nFound {len(files)} TXT files.")


# ============================================================
# ANALYSIS
# ============================================================

all_results = []

subject_summary = []


for subject_number, filepath in enumerate(sorted(files), start=1):

    filename = os.path.basename(filepath)

    print("\n" + "-" * 80)
    print(f"Subject {subject_number}: {filename}")

    try:
        data = load_subject_file(filepath)

    except Exception as e:

        print(f"ERROR reading file: {e}")
        continue


    # --------------------------------------------------------
    # Make sure we have 8 channels
    # --------------------------------------------------------

    if data.shape[1] < N_CHANNELS:

        print(
            f"WARNING: only {data.shape[1]} channels detected."
        )

        continue


    # Use first 8 channels
    data = data[:, :N_CHANNELS]


    # --------------------------------------------------------
    # Determine number of complete 1-second epochs
    # --------------------------------------------------------

    n_epochs = len(data) // EPOCH_SAMPLES

    if n_epochs == 0:

        print("ERROR: insufficient data.")
        continue


    # Limit to 120 seconds if more data exists
    n_epochs = min(n_epochs, EXPECTED_DURATION)


    print(f"Samples: {len(data)}")
    print(f"1-second epochs used: {n_epochs}")


    subject_channel_results = []


    # ========================================================
    # CHANNEL LOOP
    # ========================================================

    for ch in range(N_CHANNELS):

        signal_data = data[:, ch]

        rms_values = []
        mdf_values = []
        time_values = []


        # ----------------------------------------------------
        # Epoch analysis
        # ----------------------------------------------------

        for epoch in range(n_epochs):

            start = epoch * EPOCH_SAMPLES
            end = start + EPOCH_SAMPLES

            segment = signal_data[start:end]

            if len(segment) < EPOCH_SAMPLES:
                continue


            rms = calculate_rms(segment)

            mdf = calculate_mdf(
                segment,
                FS
            )


            rms_values.append(rms)
            mdf_values.append(mdf)
            time_values.append(epoch + 0.5)


        rms_values = np.array(rms_values)
        mdf_values = np.array(mdf_values)
        time_values = np.array(time_values)


        # ----------------------------------------------------
        # RMS slope
        # ----------------------------------------------------

        valid_rms = np.isfinite(rms_values)

        if np.sum(valid_rms) >= 3:

            rms_reg = linregress(
                time_values[valid_rms],
                rms_values[valid_rms]
            )

            rms_slope = rms_reg.slope
            rms_r2 = rms_reg.rvalue ** 2

        else:

            rms_slope = np.nan
            rms_r2 = np.nan


        # ----------------------------------------------------
        # MDF slope
        # ----------------------------------------------------

        valid_mdf = np.isfinite(mdf_values)

        if np.sum(valid_mdf) >= 3:

            mdf_reg = linregress(
                time_values[valid_mdf],
                mdf_values[valid_mdf]
            )

            mdf_slope = mdf_reg.slope
            mdf_r2 = mdf_reg.rvalue ** 2

        else:

            mdf_slope = np.nan
            mdf_r2 = np.nan


        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        result = {

            "Subject": subject_number,
            "Filename": filename,
            "Channel": ch + 1,

            "RMS_Slope": rms_slope,
            "RMS_R2": rms_r2,

            "MDF_Slope": mdf_slope,
            "MDF_R2": mdf_r2,

            "RMS_Expected": rms_slope > 0,
            "MDF_Expected": mdf_slope < 0,

            "RMS_Abs_Slope": abs(rms_slope)
            if np.isfinite(rms_slope) else np.nan,

            "MDF_Abs_Slope": abs(mdf_slope)
            if np.isfinite(mdf_slope) else np.nan
        }

        all_results.append(result)

        subject_channel_results.append(result)


    # ========================================================
    # SUBJECT SUMMARY
    # ========================================================

    subject_df = pd.DataFrame(subject_channel_results)

    if len(subject_df) > 0:

        rms_mean = subject_df["RMS_Slope"].mean()
        mdf_mean = subject_df["MDF_Slope"].mean()

        rms_positive_pct = (
            subject_df["RMS_Expected"].mean() * 100
        )

        mdf_negative_pct = (
            subject_df["MDF_Expected"].mean() * 100
        )


        # Expected fatigue direction score
        rms_score = np.mean(
            subject_df["RMS_Expected"]
        )

        mdf_score = np.mean(
            subject_df["MDF_Expected"]
        )

        direction_score = (
            rms_score + mdf_score
        ) / 2


        # Combined magnitude
        combined_effect = (
            subject_df["RMS_Abs_Slope"].mean()
            + subject_df["MDF_Abs_Slope"].mean()
        )


        subject_summary.append({

            "Subject": subject_number,
            "Filename": filename,

            "Mean_RMS_Slope": rms_mean,
            "Mean_MDF_Slope": mdf_mean,

            "RMS_Positive_%": rms_positive_pct,
            "MDF_Negative_%": mdf_negative_pct,

            "Direction_Score": direction_score,

            "Combined_Fatigue_Magnitude":
                combined_effect
        })


# ============================================================
# SAVE CHANNEL-LEVEL SUBJECT RESULTS
# ============================================================

results_df = pd.DataFrame(all_results)

results_df.to_csv(
    "subject_channel_fatigue_analysis.csv",
    index=False
)


# ============================================================
# SUBJECT SUMMARY
# ============================================================

summary_df = pd.DataFrame(subject_summary)


# ============================================================
# SUBJECT FATIGUE SCORE
# ============================================================

summary_df["Fatigue_Score"] = (
    summary_df["Direction_Score"]
    * summary_df["Combined_Fatigue_Magnitude"]
)


# Rank subjects
summary_df = summary_df.sort_values(
    by=[
        "Fatigue_Score",
        "Direction_Score",
        "Combined_Fatigue_Magnitude"
    ],
    ascending=[
        False,
        False,
        False
    ]
).reset_index(drop=True)


summary_df["Final_Rank"] = (
    np.arange(len(summary_df)) + 1
)


# ============================================================
# SAVE
# ============================================================

summary_df.to_csv(
    "subject_level_fatigue_summary.csv",
    index=False
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n")
print("=" * 100)
print("SUBJECT-LEVEL FATIGUE RANKING")
print("=" * 100)

print(
    summary_df[
        [
            "Final_Rank",
            "Subject",
            "Mean_RMS_Slope",
            "Mean_MDF_Slope",
            "RMS_Positive_%",
            "MDF_Negative_%",
            "Direction_Score",
            "Combined_Fatigue_Magnitude",
            "Fatigue_Score"
        ]
    ].to_string(index=False)
)


# ============================================================
# STRONGEST SUBJECTS
# ============================================================

print("\n")
print("=" * 100)
print("MOST FATIGUE-SENSITIVE SUBJECTS")
print("=" * 100)

top_n = min(5, len(summary_df))

for _, row in summary_df.head(top_n).iterrows():

    print(
        f"Rank {int(row['Final_Rank'])}: "
        f"Subject {int(row['Subject'])} | "
        f"RMS slope={row['Mean_RMS_Slope']:.5f} | "
        f"MDF slope={row['Mean_MDF_Slope']:.5f} | "
        f"Fatigue Score={row['Fatigue_Score']:.5f}"
    )


# ============================================================
# SUBJECTS WITH EXPECTED FATIGUE IN BOTH METRICS
# ============================================================

both_expected = summary_df[
    (summary_df["Mean_RMS_Slope"] > 0) &
    (summary_df["Mean_MDF_Slope"] < 0)
]

print("\n")
print("=" * 100)
print("SUBJECTS SHOWING EXPECTED RMS ↑ AND MDF ↓")
print("=" * 100)

if len(both_expected) > 0:

    for _, row in both_expected.iterrows():

        print(
            f"Subject {int(row['Subject'])} | "
            f"RMS={row['Mean_RMS_Slope']:.5f} | "
            f"MDF={row['Mean_MDF_Slope']:.5f}"
        )

else:

    print("No subjects showed both expected directions.")


# ============================================================
# COMPLETE
# ============================================================

print("\n")
print("=" * 100)
print("SUBJECT-LEVEL ANALYSIS COMPLETE")
print("=" * 100)

print("\nFiles saved:")
print("1. subject_channel_fatigue_analysis.csv")
print("2. subject_level_fatigue_summary.csv")

print("=" * 100)