import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Illusory correlation\illusory.csv'
data = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------------------------------

# Count the total number of people with each maptype and experience yes
total_maptype_s_experience_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes')].shape[0]
total_maptype_b_experience_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes')].shape[0]

# Count the number of people who answered correctly for each maptype and experience yes
maptype_s_right_experience_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes') & (data['relation'] == 'No relationship')].shape[0]
maptype_b_right_experience_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes') & (data['relation'] == 'No relationship')].shape[0]

# Count the number of people who answered I have no clue, as one increases the other increases, as one increases the other decreases
# for each maptype and experience yes
maptype_wrong_answers_experience_yes = data[(data['relation'] != 'No relationship') & (data['experience'] == 'Yes')].groupby(['maptype', 'relation']).size().reset_index(name='counts')

# Calculate the average confidence for people who answered correctly by maptype and experience yes
average_confidence_s_experience_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes') & (data['relation'] == 'No relationship')]['confidence'].mean()
average_confidence_b_experience_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes') & (data['relation'] == 'No relationship')]['confidence'].mean()

# Counts
counts = {'Total people maptype s experience yes': total_maptype_s_experience_yes,
            'Total people maptype b experience yes': total_maptype_b_experience_yes,
            'People who answered correctly maptype s experience yes': maptype_s_right_experience_yes,
            'People who answered correctly maptype b experience yes': maptype_b_right_experience_yes,
            'People who answered wrong maptype s experience yes': maptype_wrong_answers_experience_yes,
            'Average confidence maptype s experience yes': average_confidence_s_experience_yes,
            'Average confidence maptype b experience yes': average_confidence_b_experience_yes}
#-------------------------------------------------------------------------------------------------------------------------------------

# Plotting the percentage of right answers by maptype and experience yes
percentage_s_right_experience_yes = (maptype_s_right_experience_yes / total_maptype_s_experience_yes) * 100
percentage_b_right_experience_yes = (maptype_b_right_experience_yes / total_maptype_b_experience_yes) * 100

plt.figure(figsize=(8, 6))
sns.barplot(x=['maptype_s experience yes', 'maptype_b experience yes'], y=[percentage_s_right_experience_yes, percentage_b_right_experience_yes])
plt.title('Percentage of Right Answers by Maptype and Experience')
plt.xlabel('Maptype and Experience')
plt.ylabel('Percentage')
plt.show()

# Plotting the percentage of wrong answers by maptype and experience yes
plt.figure(figsize=(8, 6))
sns.barplot(x='maptype', y='counts', hue='relation', data=maptype_wrong_answers_experience_yes)
plt.title('Percentage of Wrong Answers by Maptype and Experience')
plt.xlabel('Maptype')
plt.ylabel('Percentage')
plt.show()

# Plotting the average confidence by maptype and experience yes
plt.figure(figsize=(8, 6))
sns.barplot(x=['maptype_s experience yes', 'maptype_b experience yes'], y=[average_confidence_s_experience_yes, average_confidence_b_experience_yes])
plt.title('Average Confidence by Maptype and Experience')
plt.xlabel('Maptype and Experience')
plt.ylabel('Average Confidence')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------

# Perform a Fisher's exact test to determine if the percentage of right answers by maptype and experience yes is significantly different
# between the two maptypes
contingency_table = [[maptype_s_right_experience_yes, total_maptype_s_experience_yes - maptype_s_right_experience_yes],
                     [maptype_b_right_experience_yes, total_maptype_b_experience_yes - maptype_b_right_experience_yes]]
odds_ratio, p_value = fisher_exact(contingency_table)

# Perform a chi-squared test to determine if the percentage of right answers by maptype and experience yes is significantly different
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

    



