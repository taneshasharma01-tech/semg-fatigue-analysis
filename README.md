# Surface EMG-Based Muscle Fatigue Analysis

Computational analysis of multi-channel surface EMG signals for quantitative assessment of muscle fatigue using RMS and MDF biomarkers.

**Dataset:** 15 subjects × 8 channels  
**Sampling Rate:** 200 Hz  
**Epoch Length:** 1 second  
**Primary Biomarkers:** RMS and MDF  
**Analysis:** Signal Processing + Regression + Statistical Validation

## Overview

This project investigates muscle fatigue using surface electromyography (sEMG) signals.

The analysis focuses on two commonly used sEMG fatigue biomarkers:

- Root Mean Square (RMS)
- Median Frequency (MDF)

During sustained muscle contraction, fatigue is generally associated with an increase in RMS amplitude and a decrease in the frequency-domain characteristics such as MDF.

The objective of this project is to develop a computational pipeline for subject-level and channel-level assessment of muscle fatigue using sEMG signals.

---

## Objectives

The main objectives of this project are:

1. Process multi-channel sEMG signals from multiple subjects.
2. Apply appropriate signal preprocessing and band-pass filtering.
3. Segment the signals into 1-second epochs.
4. Extract RMS and MDF features from each epoch.
5. Quantify fatigue-related temporal trends using linear regression.
6. Evaluate the consistency of expected fatigue directions.
7. Perform statistical validation using p-values, confidence intervals and effect sizes.
8. Apply False Discovery Rate (FDR) correction for multiple comparisons.
9. Develop subject-level fatigue scores.
10. Rank subjects according to fatigue-related sEMG characteristics.

---

## Dataset

The analysis was performed on sEMG recordings from:

- **15 subjects**
- **8 channels per subject**
- Sampling frequency: **200 Hz**

The raw dataset is not included in this repository.

---

## Signal Processing Pipeline

The overall processing pipeline is:

Raw sEMG  
↓  
Band-pass filtering  
↓  
1-second segmentation  
↓  
RMS extraction  
↓  
Welch PSD estimation  
↓  
MDF extraction  
↓  
Linear regression  
↓  
Statistical analysis  
↓  
Subject-level fatigue assessment

### 1. Band-pass Filtering

A 4th-order Butterworth band-pass filter was applied.

- Lower cutoff: **20 Hz**
- Upper cutoff: **90 Hz**
- Sampling frequency: **200 Hz**

### 2. Epoch Segmentation

Each recording was divided into non-overlapping **1-second epochs**.

### 3. RMS

RMS was calculated for each epoch and channel:

RMS = sqrt(mean(x²))

An increasing RMS trend was considered consistent with the expected fatigue response.

### 4. Median Frequency

Power spectral density (PSD) was estimated using Welch's method.

The Median Frequency (MDF) was obtained as the frequency dividing the total spectral power into two equal halves.

A decreasing MDF trend was considered consistent with the expected fatigue response.

### 5. Linear Regression

For each subject and channel, RMS and MDF values across epochs were fitted using linear regression.

The slope was used to quantify the temporal fatigue trend.

Expected directions:

- RMS slope > 0 → expected increase
- MDF slope < 0 → expected decrease

---

## Statistical Analysis

The project includes statistical validation of the extracted fatigue biomarkers.

The analysis includes:

- Mean change
- Standard deviation
- 95% confidence intervals
- p-values
- Cohen's d effect size
- False Discovery Rate (FDR) corrected p-values
- Directional consistency

Both channel-level and subject-level analyses were performed.

---

## Subject-Level Fatigue Analysis

A subject-level fatigue score was developed using:

- RMS fatigue magnitude
- MDF fatigue magnitude
- Directional consistency

The final fatigue score combines fatigue magnitude with consistency of the expected RMS↑ / MDF↓ direction.

Subjects were then ranked according to their fatigue score.

---

## Key Results

The final analysis included **15 subjects**.

### Group-level findings

The mean RMS slope across subjects was:

**0.10353**

The mean MDF slope across subjects was:

**-0.06061**

This indicates that, at the overall subject level, the average RMS trend was positive while the average MDF trend was negative, consistent with the expected direction of sEMG fatigue.

### Directional consistency

- **8/15 subjects** showed a positive RMS slope in all analyzed channels.
- **3/15 subjects** showed a negative MDF slope in all analyzed channels.
- Mean channel-wise RMS directional consistency: **90.0%**
- Mean channel-wise MDF directional consistency: **84.2%**

### Top fatigue-sensitive subjects

According to the final subject-level fatigue ranking:

| Rank | Subject | Fatigue Score |
|------|---------|---------------|
| 1 | Subject 2 | 0.38355 |
| 2 | Subject 10 | 0.23117 |
| 3 | Subject 5 | 0.22305 |
| 4 | Subject 7 | 0.20825 |
| 5 | Subject 4 | 0.17272 |

Subject 2 showed the strongest combined fatigue-related response in the final ranking.

---

## Statistical Findings

Channel-level statistical analysis demonstrated that RMS showed strong evidence of an increasing trend across several channels.

MDF generally demonstrated the expected negative trend, with statistically significant effects observed in multiple channels after FDR correction.

For example:

- Channel 4 showed significant RMS and MDF effects after FDR correction.
- Channel 5 showed significant RMS and MDF effects after FDR correction.
- Channel 6 showed significant RMS and MDF effects after FDR correction.
- Channel 7 showed significant RMS and MDF effects after FDR correction.
- Channel 8 showed significant RMS and MDF effects after FDR correction.

These findings support the presence of fatigue-related changes in the analyzed sEMG signals.

---

## Visualizations

The repository contains the generated figures from the analysis.

### Figure 1 — RMS and MDF Slopes

RMS and MDF fatigue-related slopes across channels.

![RMS and MDF Slopes](figure1_RMS_MDF_slopes.png)

### Figure 2 — Expected Fatigue Direction

Percentage of channels showing the expected fatigue direction.

![Expected Fatigue Direction](figure2_expected_fatigue_percentage.png)

### Figure 3 — Effect Size Analysis

Effect-size analysis of fatigue-related changes.

![Effect Size Analysis](figure3_effect_sizes.png)

### Figure 4 — FDR-Corrected P-values

False Discovery Rate corrected statistical significance.

![FDR Corrected P-values](figure4_FDR_pvalues.png)

### Figure 5 — RMS-MDF Relationship

Relationship between RMS and MDF fatigue-related trends.

![RMS MDF Relationship](figure5_RMS_MDF_relationship.png)

### Figure 6 — Subject-Level Fatigue Scores

Subject-level fatigue scores across the analyzed subjects.

![Subject-Level Fatigue Scores](figure6_subject_fatigue_scores.png)

### Figure 7 — Subject-Level RMS-MDF Relationship

Relationship between subject-level RMS and MDF fatigue-related trends.

![Subject-Level RMS-MDF Relationship](figure7_subject_RMS_MDF_relationship.png)

### Figure 8 — Subject-Level Fatigue Direction

Subject-level consistency of the expected fatigue direction.

![Subject-Level Fatigue Direction](figure8_subject_fatigue_direction.png)

### Figure 9 — Final Subject-Level RMS and MDF Slopes

Final RMS and MDF slopes for each subject.

![Final Subject-Level RMS and MDF Slopes](figure9_final_RMS_MDF_slopes.png)

### Figure 10 — Final Subject-Level Fatigue Ranking

Ranking of subjects according to their final fatigue scores.

![Final Subject-Level Fatigue Ranking](figure10_final_fatigue_ranking.png)

### Figure 11 — Fatigue Direction Consistency

Consistency of the expected RMS↑ / MDF↓ fatigue direction across subjects and channels.

![Fatigue Direction Consistency](figure11_fatigue_direction_consistency.png)

---

## Repository Structure

```text
sEMG/

│
├── emg_analysis.py
├── group_analysis.py
├── statistics_analysis.py
├── statistical_validation.py
├── advanced_fatigue_analysis.py
├── final_channel_analysis.py
├── final_summary.py
├── final_results_table.py
├── final_results_visualization.py
├── subject_level_analysis.py
├── subject_level_plots.py
├── plot_results.py
│
├── fatigue_summary_all_subjects.csv
├── channel_wise_fatigue_summary.csv
├── statistical_fatigue_analysis.csv
├── statistical_validation_summary.csv
├── advanced_fatigue_analysis.csv
├── final_channel_analysis.csv
├── final_fatigue_summary.csv
├── subject_channel_fatigue_analysis.csv
├── subject_level_fatigue_summary.csv
├── FINAL_CONSOLIDATED_RESULTS.csv
│
├── figure1_RMS_MDF_slopes.png
├── figure2_expected_fatigue_percentage.png
├── figure3_effect_sizes.png
├── figure4_FDR_pvalues.png
├── figure5_RMS_MDF_relationship.png
├── figure6_subject_fatigue_scores.png
├── figure7_subject_RMS_MDF_relationship.png
├── figure8_subject_fatigue_direction.png
├── figure9_final_RMS_MDF_slopes.png
├── figure10_final_fatigue_ranking.png
└── figure11_fatigue_direction_consistency.png