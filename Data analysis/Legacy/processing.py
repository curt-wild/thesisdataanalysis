import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from scipy import stats

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Levels of processing\processing.csv'
data = pd.read_csv(file_path)
df = pd.read_csv(file_path, sep=';')

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
print("Group 's' statistics:")
print(f"Count: {len(group_s)}")
print(f"Mean recalled: {group_s.mean():.2f}")
print(f"Median recalled: {group_s.median():.2f}")
print(f"Standard deviation: {group_s.std():.2f}")

print("\nGroup 'b' statistics:")
print(f"Count: {len(group_b)}")
print(f"Mean recalled: {group_b.mean():.2f}")
print(f"Median recalled: {group_b.median():.2f}")
print(f"Standard deviation: {group_b.std():.2f}")

# Create a contingency table
contingency_table = pd.crosstab(df['maptype'], df['recalled_count'])

# Perform Chi-square test
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

print(f"\nChi-square statistic: {chi2:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("The difference between groups 's' and 'b' is statistically significant (p < 0.05).")
else:
    print("The difference between groups 's' and 'b' is not statistically significant (p >= 0.05).")

# Calculate Cramer's V for effect size
n = contingency_table.sum().sum()
min_dim = min(contingency_table.shape) - 1
cramer_v = np.sqrt(chi2 / (n * min_dim))

print(f"\nEffect size (Cramer's V): {cramer_v:.4f}")

