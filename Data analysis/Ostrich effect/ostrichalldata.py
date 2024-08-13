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
#-------------------------------------------------------------------------------------------------------------

# Separate data for maptype 's' and 'b'
s_times = df[df['maptype'] == 's']['time']
b_times = df[df['maptype'] == 'b']['time']

# Calculate basic statistics
s_stats = s_times.describe()
b_stats = b_times.describe()

# Count the number of happiness sadness fear disgust anger surprise and none per maptype
s_happiness = df[(df['maptype'] == 's') & (df['happiness'] == 'Yes')].shape[0]
s_sadness = df[(df['maptype'] == 's') & (df['sadness'] == 'Yes')].shape[0]
s_fear = df[(df['maptype'] == 's') & (df['fear'] == 'Yes')].shape[0]
s_disgust = df[(df['maptype'] == 's') & (df['disgust'] == 'Yes')].shape[0]
s_anger = df[(df['maptype'] == 's') & (df['anger'] == 'Yes')].shape[0]
s_surprise = df[(df['maptype'] == 's') & (df['surprise'] == 'Yes')].shape[0]
s_neutral = df[(df['maptype'] == 's') & (df['none'] == 'Yes')].shape[0]
b_happiness = df[(df['maptype'] == 'b') & (df['happiness'] == 'Yes')].shape[0]
b_sadness = df[(df['maptype'] == 'b') & (df['sadness'] == 'Yes')].shape[0]
b_fear = df[(df['maptype'] == 'b') & (df['fear'] == 'Yes')].shape[0]
b_disgust = df[(df['maptype'] == 'b') & (df['disgust'] == 'Yes')].shape[0]
b_anger = df[(df['maptype'] == 'b') & (df['anger'] == 'Yes')].shape[0]
b_surprise = df[(df['maptype'] == 'b') & (df['surprise'] == 'Yes')].shape[0]
b_neutral = df[(df['maptype'] == 'b') & (df['none'] == 'Yes')].shape[0]

# Count the number of answers per maptype
s_answers = df[df['maptype'] == 's'].shape[0]
b_answers = df[df['maptype'] == 'b'].shape[0]

# Count the number of correct answers (as one increases, so does the other in column relation) per maptype
s_correct = df[(df['maptype'] == 's') & (df['relation'] == 'As one increases, so does the other')].shape[0]
b_correct = df[(df['maptype'] == 'b') & (df['relation'] == 'As one increases, so does the other')].shape[0]

#-------------------------------------------------------------------------------------------------------------

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

# Create two histograms one for each maptype with counts of the emotions
plt.figure(figsize=(10, 6))
plt.bar(['Happiness', 'Sadness', 'Fear', 'Disgust', 'Anger', 'Surprise', 'Neutral'], [s_happiness, s_sadness, s_fear,
                                                                                       s_disgust, s_anger, s_surprise, s_neutral], alpha=0.7, color='blue', label='Standard')
plt.xlabel('Emotion')
plt.ylabel('Frequency')
plt.title('Emotion Distribution - Standard Maps')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(['Happiness', 'Sadness', 'Fear', 'Disgust', 'Anger', 'Surprise', 'Neutral'], [b_happiness, b_sadness, b_fear,
                                                                                        b_disgust, b_anger, b_surprise, b_neutral], alpha=0.7, color='red', label='Biased')
plt.xlabel('Emotion')
plt.ylabel('Frequency')
plt.title('Emotion Distribution - Biased Maps')
plt.legend()
plt.show()

# Plot the number of correct answers per maptype
plt.figure(figsize=(10, 6))
plt.bar(['Standard', 'Biased'], [s_correct, b_correct], alpha=0.7, color=['blue', 'red'])
plt.xlabel('Maptype')
plt.ylabel('Number of Correct Answers')
plt.title('Number of Correct Answers per Maptype')
plt.show()
#-------------------------------------------------------------------------------------------------------------

# Run statistical tests
# Run a t-test to compare the performance of participants on standard and biased maps
t_stat, p_value = stats.ttest_ind(s_times, b_times)

#Run statistical test by deleting the outliers
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

# Run a fisher to compare the number of correct answers for standard and biased maps
fisher_stat, fisher_p_value = stats.fisher_exact([[s_correct, s_answers - s_correct], [b_correct, b_answers - b_correct]])

# Run a chi-square test to compare the number of correct answers for standard and biased maps
contingency_table = np.array([[s_correct, b_correct], [s_answers - s_correct, b_answers - b_correct]])

# Perform the chi-square test
chi2_stat, chi2_p_value, _, _ = stats.chi2_contingency(contingency_table)
#-------------------------------------------------------------------------------------------------------------

# Print the results
print('Basic Statistics for Standard Maps:')
print(s_stats)
print('\nBasic Statistics for Biased Maps:')
print(b_stats)

print('\nNumber of correct answers for standard maps:')
print(s_correct)
print('\nNumber of correct answers for biased maps:')
print(b_correct)

print('\nT-Test Results:')
print(f'T-Statistic: {t_stat}')
print(f'P-Value: {p_value}')
print(f'{"The difference is statistically significant" if p_value < 0.05 else "The difference is not statistically significant"}')

print(f"\nAfter removing outliers:")
print(f"t-statistic: {t_stat_no_outliers}")
print(f"p-value: {p_value_no_outliers}")
print(f"{'The difference is statistically significant (without outliers)' if p_value_no_outliers < 0.05 else 'The difference is not statistically significant (without outliers)'}")

print(f'\nFisher Test Results (Right answers):')
print(f'Fisher Statistic: {fisher_stat}')
print(f'P-Value: {fisher_p_value}')
print(f'{"The difference is statistically significant" if fisher_p_value < 0.05 else "The difference is not statistically significant"}')

print(f'\nChi-Square Test Results (Right answers):')
print(f'Chi-Square Statistic: {chi2_stat}')
print(f'P-Value: {chi2_p_value}')
print(f'{"The difference is statistically significant" if chi2_p_value < 0.05 else "The difference is not statistically significant"}')



