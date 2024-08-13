import pandas as pd
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency

import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Illusory correlation\illusory.csv'
data = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------------------------------

# Count the total number of people with each maptype and experience no
total_maptype_s_experience_no = data[(data['maptype'] == 's') & (data['experience'] == 'No')].shape[0]
total_maptype_b_experience_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No')].shape[0]

# Count the number of people who answered correctly for each maptype and experience no
maptype_s_right_experience_no = data[(data['maptype'] == 's') & (data['experience'] == 'No') & (data['relation'] == 'No relationship')].shape[0]
maptype_b_right_experience_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No') & (data['relation'] == 'No relationship')].shape[0]

# Count the number of people who answered I have no clue, as one increases the other increases, as one increases the other decreases
# for each maptype and experience no
maptype_wrong_answers_experience_no = data[(data['relation'] != 'No relationship') & (data['experience'] == 'No')].groupby(['maptype', 'relation']).size().reset_index(name='counts')

# Calculate the average confidence for people who answered correctly by maptype and experience no
average_confidence_s_experience_no = data[(data['maptype'] == 's') & (data['experience'] == 'No') & (data['relation'] == 'No relationship')]['confidence'].mean()
average_confidence_b_experience_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No') & (data['relation'] == 'No relationship')]['confidence'].mean()

# Counts
counts = {'Total people maptype s experience no': total_maptype_s_experience_no,
            'Total people maptype b experience no': total_maptype_b_experience_no,
            'People who answered correctly maptype s experience no': maptype_s_right_experience_no,
            'People who answered correctly maptype b experience no': maptype_b_right_experience_no,
            'People who answered wrong maptype s experience no': maptype_wrong_answers_experience_no,
            'Average confidence maptype s experience no': average_confidence_s_experience_no,
            'Average confidence maptype b experience no': average_confidence_b_experience_no}
#-------------------------------------------------------------------------------------------------------------------------------------

# Plotting the percentage of right answers by maptype and experience no
percentage_s_right_experience_no = (maptype_s_right_experience_no / total_maptype_s_experience_no) * 100
percentage_b_right_experience_no = (maptype_b_right_experience_no / total_maptype_b_experience_no) * 100

plt.figure(figsize=(8, 6))
sns.barplot(x=['maptype_s experience no', 'maptype_b experience no'], y=[percentage_s_right_experience_no, percentage_b_right_experience_no])
plt.title('Percentage of Right Answers by Maptype and Experience')
plt.xlabel('Maptype and Experience')
plt.ylabel('Percentage')
plt.show()

# Plotting the percentage of wrong answers by maptype and experience no
plt.figure(figsize=(8, 6))
sns.barplot(x='maptype', y='counts', hue='relation', data=maptype_wrong_answers_experience_no)
plt.title('Percentage of Wrong Answers by Maptype and Experience')
plt.xlabel('Maptype')
plt.ylabel('Percentage')
plt.show()

# Plotting the average confidence by maptype and experience no
plt.figure(figsize=(8, 6))
sns.barplot(x=['maptype_s experience no', 'maptype_b experience no'], y=[average_confidence_s_experience_no, average_confidence_b_experience_no])
plt.title('Average Confidence by Maptype and Experience')
plt.xlabel('Maptype and Experience')
plt.ylabel('Average Confidence')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------

# Perform a Fisher's exact test to determine if the percentage of right answers by maptype and experience no is significantly different
# between the two maptypes
contingency_table = [[maptype_s_right_experience_no, total_maptype_s_experience_no - maptype_s_right_experience_no],
                     [maptype_b_right_experience_no, total_maptype_b_experience_no - maptype_b_right_experience_no]]
odds_ratio, p_value = fisher_exact(contingency_table)

# Perform a chi-squared test to determine if the percentage of right answers by maptype and experience no is significantly different
# between the two maptypes
chi2, pchi, dof, expected = chi2_contingency(contingency_table)
#-------------------------------------------------------------------------------------------------------------------------------------

# Print the results
print('Counts:')
for key, value in counts.items():
    print(f'{key}: {value}')

print(f'Fisher exact test: Odds ratio: {odds_ratio}, p-value: {p_value}')
print(f'Chi-square test: Chi2: {chi2}, p-value: {pchi}, dof: {dof}, expected: {expected}')

# If the p-value is less than 0.05, the difference is statistically significant
if p_value < 0.05:
    print('The difference in the proportion of people who answered correctly by maptype and experience is statistically significant')
else:
    print('The difference in the proportion of people who answered correctly by maptype and experience is not statistically significant')

# If the p-value is less than 0.05, the difference is statistically significant
if pchi < 0.05:
    print('The difference in the proportion of people who answered correctly by maptype and experience is statistically significant')
else:
    print('The difference in the proportion of people who answered correctly by maptype and experience is not statistically significant')
