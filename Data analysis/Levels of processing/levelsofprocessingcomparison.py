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

# Separate data for standard and bias groups and experienced and inexperienced groups  
group_standard_experienced = df[(df['maptype'] == 's') & (df['experience'] == 'Yes')]['recalled_count']
group_bias_experienced = df[(df['maptype'] == 'b') & (df['experience'] == 'Yes')]['recalled_count']
group_standard_inexperienced = df[(df['maptype'] == 's') & (df['experience'] == 'No')]['recalled_count']
group_bias_inexperienced = df[(df['maptype'] == 'b') & (df['experience'] == 'No')]['recalled_count']

# Calculate statistics for each group
standard_experienced_stats = group_standard_experienced.describe()
bias_experienced_stats = group_bias_experienced.describe()
standard_inexperienced_stats = group_standard_inexperienced.describe()
bias_inexperienced_stats = group_bias_inexperienced.describe()
#-------------------------------------------------------------------------------------------------------------
# Plot results for standard experienced and non-experienced groups
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.hist(group_standard_experienced, bins=range(12), alpha=0.7, color='blue', label='Standard Experienced')
plt.xlabel('Number of Correctly Recalled Cities')
plt.ylabel('Frequency')
plt.title('Recalled Cities Distribution - Standard Maps (Experienced)')
plt.legend()

plt.subplot(1, 2, 2)
plt.hist(group_standard_inexperienced, bins=range(12), alpha=0.7, color='red', label='Standard Inexperienced')
plt.xlabel('Number of Correctly Recalled Cities')
plt.ylabel('Frequency')
plt.title('Recalled Cities Distribution - Standard Maps (Inexperienced)')
plt.legend()

plt.tight_layout()
plt.show()

# Plot results for bias experienced and non-experienced groups
plt.figure(figsize=(10, 6))

plt.subplot(1, 2, 1)
plt.hist(group_bias_experienced, bins=range(12), alpha=0.7, color='blue', label='Bias Experienced')
plt.xlabel('Number of Correctly Recalled Cities')
plt.ylabel('Frequency')
plt.title('Recalled Cities Distribution - Bias Maps (Experienced)')
plt.legend()

plt.subplot(1, 2, 2)
plt.hist(group_bias_inexperienced, bins=range(12), alpha=0.7, color='red', label='Bias Inexperienced')
plt.xlabel('Number of Correctly Recalled Cities')
plt.ylabel('Frequency')
plt.title('Recalled Cities Distribution - Bias Maps (Inexperienced)')
plt.legend()

plt.tight_layout()
plt.show()
#-------------------------------------------------------------------------------------------------------------

#  Run a t-test to compare the performance of experienced and inexperienced participants on standard maps
t_stat_s, p_value_s = stats.ttest_ind(group_standard_experienced, group_standard_inexperienced)

# Run a t-test to compare the performance of experienced and inexperienced participants on bias maps
t_stat_b, p_value_b = stats.ttest_ind(group_bias_experienced, group_bias_inexperienced)
#-------------------------------------------------------------------------------------------------------------

# Print the results
print('Standard Experienced Stats:')
print(standard_experienced_stats)
print('\nStandard Inexperienced Stats:')
print(standard_inexperienced_stats)
print('\nBias Experienced Stats:')
print(bias_experienced_stats)
print('\nBias Inexperienced Stats:')
print(bias_inexperienced_stats)
print(f'\nT-statistic for Standard Maps: {t_stat_s}')
print(f'P-value for Standard Maps: {p_value_s}')
print(f'{"The difference is statistically significant" if p_value_s < 0.05 else "The difference is not statistically significant"}')
print(f'\nT-statistic for Bias Maps: {t_stat_b}')
print(f'P-value for Bias Maps: {p_value_b}')
print(f'{"The difference is statistically significant" if p_value_b < 0.05 else "The difference is not statistically significant"}')




