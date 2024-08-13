import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from scipy import stats
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Levels of processing\processing.csv'
data = pd.read_csv(file_path)
df = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------

# List of correct city names
correct_names = ['cheyenna', 'ajax', 'roscovina', 'brevia', 'kara', 'lakhoma', 'havare', 'athenia', 'centralis', 'arcadia', 'mustang']

# Function to check if a name is similar enough to any correct name
def is_similar(name, threshold=60):
    return any(fuzz.ratio(name.lower(), correct.lower()) >= threshold for correct in correct_names)

# Function to count recalled names for a participant
def count_recalled_names(row):
    recalled = 0
    for col in [f'city{i}' for i in range(1, 12)]:
        if pd.notna(row[col]) and is_similar(row[col]):
            recalled += 1
    return recalled

# Apply the function to each row
df['recalled_count'] = df.apply(count_recalled_names, axis=1)

# Separate data for 's' and 'b' groups
group_s = df[df['maptype'] == 's']['recalled_count']
group_b = df[df['maptype'] == 'b']['recalled_count']

# Calculate statistics for each group 
s_stats = group_s.describe()
b_stats = group_b.describe()
#-------------------------------------------------------------------------------------------------------------

# Plot results for Maptype S
plt.figure(figsize=(10, 6))
plt.hist(group_s, bins=range(12), alpha=0.7, color='blue')
plt.xlabel('Number of Correctly Recalled Cities')
plt.ylabel('Frequency')
plt.title('Recalled Cities Distribution - Maptype S')
plt.show()

# Plot results for Maptype B
plt.figure(figsize=(10, 6))
plt.hist(group_b, bins=range(12), alpha=0.7, color='red')
plt.xlabel('Number of Correctly Recalled Cities')
plt.ylabel('Frequency')
plt.title('Recalled Cities Distribution - Maptype B')

plt.show()

# Plot words remembered by maptype
plt.figure(figsize=(10, 6))
plt.bar(['Maptype S', 'Maptype B'], [s_stats['mean'], b_stats['mean']], yerr=[s_stats['std'], b_stats['std']], capsize=5)
plt.ylabel('Mean Number of Correctly Recalled Cities')
plt.title('Mean Number of Correctly Recalled Cities by Maptype')
plt.show()
#-------------------------------------------------------------------------------------------------------------

# Perform t-test to check if the difference is statistically significant
t_stat, p_value = stats.ttest_ind(group_s, group_b)
#-------------------------------------------------------------------------------------------------------------

# Print results
print("Statistics for maptype 's':")
print(s_stats)
print("\nStatistics for maptype 'b':")
print(b_stats)
print(f"\nT-statistic: {t_stat}")
print(f"P-value: {p_value}")
print(f"{'The difference is statistically significant' if p_value < 0.05 else 'The difference is not statistically significant'}")



