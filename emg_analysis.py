import os
import glob
import numpy as np
import pandas as pd

from scipy.signal import butter, filtfilt, welch
from scipy.stats import linregress


# ============================================================
# SETTINGS
# ============================================================

DATA_FOLDER = "Dataset EMG Fatigue/Dataset EMG Fatigue/Data as txt Files"

FS = 200                  # Sampling frequency
LOWCUT = 20               # Lower cutoff frequency
HIGHCUT = 90              # Upper cutoff frequency
EPOCH_DURATION = 1        # seconds

NUM_CHANNELS = 8


# ============================================================
# FILTER DESIGN
# ============================================================

b, a = butter(
    4,
    [LOWCUT, HIGHCUT],
    btype="bandpass",
    fs=FS
)


# ============================================================
# FIND ALL SUBJECT FILES
# ============================================================

files = glob.glob(os.path.join(DATA_FOLDER, "sub*.txt"))

# Sort numerically: sub1, sub2, ..., sub15
files = sorted(
    files,
    key=lambda x: int(
        os.path.basename(x).replace("sub", "").replace(".txt", "")
    )
)

print("=" * 60)
print("EMG FATIGUE ANALYSIS - ALL SUBJECTS")
print("=" * 60)

print(f"Number of subjects found: {len(files)}")
print()


# ============================================================
# STORE FINAL RESULTS
# ============================================================

all_results = []


# ============================================================
# PROCESS EACH SUBJECT
# ============================================================

for file_path in files:

    subject_name = os.path.basename(file_path).replace(".txt", "")

    print("-" * 60)
    print(f"Processing {subject_name}...")
    print("-" * 60)

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    data = np.loadtxt(file_path)

    print("Original shape:", data.shape)

    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    filtered_data = np.zeros_like(data)

    for ch in range(NUM_CHANNELS):
        filtered_data[:, ch] = filtfilt(
            b,
            a,
            data[:, ch]
        )

    # --------------------------------------------------------
    # 1-SECOND SEGMENTATION
    # --------------------------------------------------------

    epoch_samples = FS * EPOCH_DURATION

    num_epochs = len(filtered_data) // epoch_samples

    print("Number of complete epochs:", num_epochs)

    # --------------------------------------------------------
    # MATRICES
    # --------------------------------------------------------

    rms_values = np.zeros((num_epochs, NUM_CHANNELS))
    mdf_values = np.zeros((num_epochs, NUM_CHANNELS))

    # --------------------------------------------------------
    # RMS + MDF
    # --------------------------------------------------------

    for ch in range(NUM_CHANNELS):

        for epoch in range(num_epochs):

            start = epoch * epoch_samples
            end = start + epoch_samples

            segment = filtered_data[start:end, ch]

            # =========================
            # RMS
            # =========================

            rms = np.sqrt(
                np.mean(segment ** 2)
            )

            rms_values[epoch, ch] = rms

            # =========================
            # PSD using Welch
            # =========================

            frequencies, psd = welch(
                segment,
                fs=FS,
                nperseg=epoch_samples
            )

            # =========================
            # MDF
            # =========================

            cumulative_power = np.cumsum(psd)

            total_power = cumulative_power[-1]

            median_index = np.where(
                cumulative_power >= total_power / 2
            )[0][0]

            mdf_values[epoch, ch] = frequencies[median_index]

    # --------------------------------------------------------
    # TIME VECTOR
    # --------------------------------------------------------

    epoch_time = np.arange(1, num_epochs + 1)

    # --------------------------------------------------------
    # CHANNEL-WISE ANALYSIS
    # --------------------------------------------------------

    for ch in range(NUM_CHANNELS):

        # ================================================
        # RMS LINEAR REGRESSION
        # ================================================

        rms_result = linregress(
            epoch_time,
            rms_values[:, ch]
        )

        rms_slope = rms_result.slope
        rms_r2 = rms_result.rvalue ** 2

        # ================================================
        # MDF LINEAR REGRESSION
        # ================================================

        mdf_result = linregress(
            epoch_time,
            mdf_values[:, ch]
        )

        mdf_slope = mdf_result.slope
        mdf_r2 = mdf_result.rvalue ** 2

        # ================================================
        # FATIGUE DIRECTION
        # ================================================

        if rms_slope > 0 and mdf_slope < 0:

            fatigue_direction = "Consistent"

        elif rms_slope > 0 and mdf_slope > 0:

            fatigue_direction = "Mixed"

        elif rms_slope < 0 and mdf_slope < 0:

            fatigue_direction = "Mixed"

        else:

            fatigue_direction = "Opposite"

        # ================================================
        # SAVE RESULT
        # ================================================

        all_results.append({

            "Subject": subject_name,

            "Channel": f"Ch {ch + 1}",

            "RMS_Slope": rms_slope,

            "RMS_R2": rms_r2,

            "MDF_Slope": mdf_slope,

            "MDF_R2": mdf_r2,

            "Fatigue_Direction": fatigue_direction
        })


# ============================================================
# CREATE DATAFRAME
# ============================================================

results_df = pd.DataFrame(all_results)


# ============================================================
# SAVE CSV
# ============================================================

output_file = "fatigue_summary_all_subjects.csv"

results_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 60)
print("ALL SUBJECTS ANALYSIS COMPLETED")
print("=" * 60)

print()

print(results_df.to_string(index=False))

print()

print("=" * 60)
print(f"Results saved to: {output_file}")
print("=" * 60)