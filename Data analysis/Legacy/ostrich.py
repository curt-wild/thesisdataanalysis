import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Ostrich effect\ostrich.csv'

# Read the CSV data
df = pd.read_csv(file_path, sep=';')


# Convert 'time' column to numeric, replacing comma with dot
df['time'] = df['time'].str.replace(',', '.').astype(float)

# Separate data for maptype 's' and 'b'
s_times = df[df['maptype'] == 's']['time']
b_times = df[df['maptype'] == 'b']['time']

# Calculate basic statistics
s_stats = s_times.describe()
b_stats = b_times.describe()

print("Statistics for maptype 's':")
print(s_stats)
print("\nStatistics for maptype 'b':")
print(b_stats)

# Perform t-test to check if the difference is statistically significant
t_stat, p_value = stats.ttest_ind(s_times, b_times)

print(f"\nt-statistic: {t_stat}")
print(f"p-value: {p_value}")
print(f"{'The difference is statistically significant' if p_value < 0.05 else 'The difference is not statistically significant'}")


#Run statistical test by deleting the outliers
# Assuming s_times and b_times are already defined as pandas Series
# Calculate the z-scores for each value
z_scores_s = stats.zscore(s_times)
z_scores_b = stats.zscore(b_times)

# Find the boolean mask of the outliers
outliers_s_mask = np.abs(z_scores_s) <= 3
outliers_b_mask = np.abs(z_scores_b) <= 3

# Remove the outliers using boolean indexing
s_times_no_outliers = s_times[outliers_s_mask]
b_times_no_outliers = b_times[outliers_b_mask]

# Count outliers
outliers_s = s_times[~outliers_s_mask]
outliers_b = b_times[~outliers_b_mask]

# Perform the t-test again
t_stat_no_outliers, p_value_no_outliers = stats.ttest_ind(s_times_no_outliers, b_times_no_outliers)

print(f"\nAfter removing outliers:")
print(f"Outliers in maptype 's': {outliers_s.tolist()}")
print(f"Outliers in maptype 'b': {outliers_b.tolist()}")
print(f"t-statistic: {t_stat_no_outliers}")
print(f"p-value: {p_value_no_outliers}")
print(f"{'The difference is statistically significant (without outliers)' if p_value_no_outliers < 0.05 else 'The difference is not statistically significant (without outliers)'}")


# Visualize the distribution of times for each maptype
plt.figure(figsize=(10, 6))
plt.boxplot([s_times, b_times], labels=['s', 'b'])
plt.title('Distribution of Times for Maptype s and b')
plt.ylabel('Time')
plt.show()

# Create a histogram
plt.figure(figsize=(10, 6))
plt.hist(s_times, bins=20, alpha=0.5, label='s')
plt.hist(b_times, bins=20, alpha=0.5, label='b')
plt.title('Histogram of Times for Maptype s and b')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.legend()
plt.show()