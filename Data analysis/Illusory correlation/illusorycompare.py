import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Illusory correlation\illusory.csv'
data = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------------------------------

# Count the total number of people with each maptype and experience
total_maptype_s_experience_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes')].shape[0]
total_maptype_s_experience_no = data[(data['maptype'] == 's') & (data['experience'] == 'No')].shape[0]
total_maptype_b_experience_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes')].shape[0]
total_maptype_b_experience_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No')].shape[0]

# Count the number of people who answered correctly for each maptype and experience
maptype_s_right_experience_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes') & (data['relation'] == 'No relationship')].shape[0]
maptype_s_right_experience_no = data[(data['maptype'] == 's') & (data['experience'] == 'No') & (data['relation'] == 'No relationship')].shape[0]
maptype_b_right_experience_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes') & (data['relation'] == 'No relationship')].shape[0]
maptype_b_right_experience_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No') & (data['relation'] == 'No relationship')].shape[0]

# Count the number of people who answered I have no clue, as one increases the other increases, as one increases the other decreases
# for each maptype and experience
maptype_wrong_answers_experience_yes = data[(data['relation'] != 'No relationship') & (data['experience'] == 'Yes')].groupby(['maptype', 'relation']).size().reset_index(name='counts')
maptype_wrong_answers_experience_no = data[(data['relation'] != 'No relationship') & (data['experience'] == 'No')].groupby(['maptype', 'relation']).size().reset_index(name='counts')

# Calculate the average confidence for people who answered correctly by maptype and experience
average_confidence_s_experience_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes') & (data['relation'] == 'No relationship')]['confidence'].mean()
average_confidence_s_experience_no = data[(data['maptype'] == 's') & (data['experience'] == 'No') & (data['relation'] == 'No relationship')]['confidence'].mean()
average_confidence_b_experience_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes') & (data['relation'] == 'No relationship')]['confidence'].mean()
average_confidence_b_experience_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No') & (data['relation'] == 'No relationship')]['confidence'].mean()

# Counts
counts = {'Total people maptype s experience yes': total_maptype_s_experience_yes,
            'Total people maptype s experience no': total_maptype_s_experience_no,
            'Total people maptype b experience yes': total_maptype_b_experience_yes,
            'Total people maptype b experience no': total_maptype_b_experience_no,
            'People who answered correctly maptype s experience yes': maptype_s_right_experience_yes,
            'People who answered correctly maptype s experience no': maptype_s_right_experience_no,
            'People who answered correctly maptype b experience yes': maptype_b_right_experience_yes,
            'People who answered correctly maptype b experience no': maptype_b_right_experience_no,
            'People who answered wrong maptype s experience yes': maptype_wrong_answers_experience_yes,
            'People who answered wrong maptype s experience no': maptype_wrong_answers_experience_no,
            'Average confidence maptype s experience yes': average_confidence_s_experience_yes,
            'Average confidence maptype s experience no': average_confidence_s_experience_no,
            'Average confidence maptype b experience yes': average_confidence_b_experience_yes,
            'Average confidence maptype b experience no': average_confidence_b_experience_no}
#-------------------------------------------------------------------------------------------------------------------------------------

# Plotting the percentage of right answers by maptype and experience
percentage_s_right_experience_yes = (maptype_s_right_experience_yes / total_maptype_s_experience_yes) * 100
percentage_s_right_experience_no = (maptype_s_right_experience_no / total_maptype_s_experience_no) * 100
percentage_b_right_experience_yes = (maptype_b_right_experience_yes / total_maptype_b_experience_yes) * 100
percentage_b_right_experience_no = (maptype_b_right_experience_no / total_maptype_b_experience_no) * 100

plt.figure(figsize=(8, 6))
sns.barplot(x=['maptype_s experience yes', 'maptype_s experience no', 'maptype_b experience yes', 'maptype_b experience no'], y=[percentage_s_right_experience_yes, percentage_s_right_experience_no, percentage_b_right_experience_yes, percentage_b_right_experience_no])
plt.title('Percentage of Right Answers by Maptype and Experience')
plt.xlabel('Maptype and Experience')
plt.ylabel('Percentage')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------

# Run statistics
# Create a contingency table
contingency_table = [[maptype_b_right_experience_yes, maptype_b_right_experience_no],
                     [total_maptype_b_experience_yes - maptype_b_right_experience_yes, total_maptype_b_experience_no - maptype_b_right_experience_no]]
# Perform the Fisher's exact test
odds_ratio, p_value = fisher_exact(contingency_table)
# Perform the Chi-square test
chi2, p_chi, dof, expected = chi2_contingency(contingency_table)
#-------------------------------------------------------------------------------------------------------------------------------------

# Print the counts
for key, value in counts.items():
    print(f'{key}: {value}')
# Print the results
print(f'Fisher exact test: Odds ratio: {odds_ratio}, p-value: {p_value}')
print(f'Chi-square test: Chi2: {chi2}, p-value: {p_value}, dof: {dof}, expected: {expected}')

# If the p-value is less than 0.05, the difference is statistically significant
if p_value < 0.05:
    print('The difference in the proportion of people who answered correctly by maptype and experience is statistically significant')
else:
    print('The difference in the proportion of people who answered correctly by maptype and experience is not statistically significant')
# If the p-value is less than 0.05, the difference is statistically
if p_chi < 0.05:
    print('The difference in the proportion of people who answered correctly by maptype and experience is statistically significant')
else:
    print('The difference in the proportion of people who answered correctly by maptype and experience is not statistically significant')

