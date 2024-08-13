import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency, ttest_ind, mannwhitneyu


# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Clustering illusion\clustering.csv'
data = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------------------------------

# Perform the Specified Calculations|

# Count the total number of people with each maptype 
total_maptype_s = data[data['maptype'] == 's'].shape[0]
total_maptype_b = data[data['maptype'] == 'b'].shape[0]

# Count the correct answers for each maptype
maptype_s_correct = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes')].shape[0]
maptype_b_correct = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes')].shape[0]

# Count the total number of people who answered 'Yes' to 'idk'
total_idk = data[data['idk'] == 'Yes'].shape[0]

# Count the number of answers for each state column
columns_to_check = [
    'taraxa', 'phrengal', 'kovaire', 'cameron', 'ajaxa', 'centralia', 
    'laurenia', 'gelesia', 'ravinia', 'midian', 'idk'
]

state_counts_maptype_s = data[data['maptype'] == 's'][columns_to_check].apply(lambda x: (x == 'Yes').sum())
state_counts_maptype_b = data[data['maptype'] == 'b'][columns_to_check].apply(lambda x: (x == 'Yes').sum())

# Calculate the average confidence for people who answered yes to nostate by maptype
average_confidence_s = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes')]['confidence'].mean()
average_confidence_b = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes')]['confidence'].mean()

# Calculate the average confidence for people with all other answers by maptype
average_confidence_s_no = data[(data['maptype'] == 's') & (data['nostate'] == 'No') & (data['idk'] != 'Yes')]['confidence'].mean()  
average_confidence_b_no = data[(data['maptype'] == 'b') & (data['nostate'] == 'No') & (data['idk'] != 'Yes')]['confidence'].mean()


# Counts 
counts = {
    'Total number of people with maptype standard': total_maptype_s,
    'Total number of people with maptype bias': total_maptype_b,
    'Total number of people who answered no clue': total_idk,
    'Number of people who answered correctly for maptype standard': maptype_s_correct,
    'Number of people who answered correctly for maptype bias': maptype_b_correct,
    'Confidence for correct answers for maptype standard': average_confidence_s,
    'Confidence for correct answers for maptype bias': average_confidence_b
}
#-------------------------------------------------------------------------------------------------------------------------------------

# Plots
# Plot the percentage of correct answers for each maptype
plt.figure(figsize=(8, 6))
sns.set_theme(font='Lato')
sns.barplot(x=['Standard', 'Bias-inducing'], y=[maptype_s_correct / total_maptype_s * 100, maptype_b_correct / total_maptype_b * 100], edgecolor='none')
plt.ylabel('Percentage of correct answers')
plt.show()

# Plot the counts of responses for each state by maptype do one for each maptype

# Capitalize the first letter of each state name, change idk for I have no clue
columns_to_checkcapit = [column.capitalize() for column in columns_to_check]
columns_to_checkcapit = [column.replace('Idk', 'I have no clue') for column in columns_to_checkcapit]

plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_checkcapit, y=state_counts_maptype_s)
#plt.title('Counts of responses for each state (standard design)')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_checkcapit, y=state_counts_maptype_b)
#plt.title('Counts of responses for each state (bias-inducing design)')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()


# Plot the average confidence for correct answers by maptype
plt.figure(figsize=(8, 6))
sns.barplot(x=['Standard', 'Bias'], y=[average_confidence_s, average_confidence_b])
#plt.title('Average Confidence for Correct Answers by Maptype')
plt.ylabel('Average Confidence')
plt.show()

# Plot the average confidence for incorrect answers by maptype
plt.figure(figsize=(8, 6))
sns.barplot(x=['Standard', 'Bias'], y=[average_confidence_s_no, average_confidence_b_no])
#plt.title('Average Confidence for Incorrect Answers by Maptype')
plt.ylabel('Average Confidence')
plt.show()

# Plot the average confidence for each maptype both correct and incorrect
plt.figure(figsize=(8, 6))
sns.barplot(x=['Correct answers for standard', 'Incorrect answers for standard', 'Correct answers for bias', 'Incorrect answers for bias'], 
            y=[average_confidence_s, average_confidence_s_no, average_confidence_b, average_confidence_b_no])
#plt.title('Average Confidence for Correct and Incorrect Answers by Maptype')
plt.ylabel('Average confidence')
plt.show()

#-------------------------------------------------------------------------------------------------------------------------------------

# Do statistical tests
# Perform a Fisher's exact test for the number of correct answers by maptype
odds_ratio, p_value = fisher_exact([[maptype_s_correct, total_maptype_s - maptype_s_correct], 
                                    [maptype_b_correct, total_maptype_b - maptype_b_correct]])
"""
Fisher's Exact Test 
https://www.langsrud.com/stat/fisher.htm
------------------------------------------
 TABLE = [ 38 , 51 , 61 , 21 ]
Left   : p-value = 0.000022595138665795788
Right  : p-value = 0.9999945810653638
2-Tail : p-value = 0.000028830066610368107
------------------------------------------
"""

# Perform a chi-squared test for the number of correct answers by maptype
chi2, chi2_p, _, _ = chi2_contingency([[maptype_s_correct, total_maptype_s - maptype_s_correct], 
                                       [maptype_b_correct, total_maptype_b - maptype_b_correct]])

# Perform a mann u whitney test for the average confidence by maptype
t_stat, t_p = mannwhitneyu(average_confidence_s_no, average_confidence_b_no)


#-------------------------------------------------------------------------------------------------------------------------------------

# Print counts and test results
print('Counts:')
for key, value in counts.items():
    print(f'{key}: {value}')

print('\nTest Results:')
print(f'Fisher\'s Exact Test: Odds Ratio = {odds_ratio}, p-value = {p_value}')
print(f'Chi-squared Test: Chi^2 = {chi2}, p-value = {chi2_p}')

if p_value < 0.05:
    print('There is a significant difference between the two maptypes (Fisher).')
else:
    print('There is no significant difference between the two maptypes (Fisher).')

if chi2_p < 0.05:
    print('There is a significant difference between the two maptypes (Chi-squared).')
else:
    print('There is no significant difference between the two maptypes (Chi-squared).')

print(f'Mann-Whitney U Test: t-statistic = {t_stat}, p-value = {t_p}')
if t_p < 0.05:
    print('There is a significant difference between the two maptypes (Mann-Whitney).')
else:
    print('There is no significant difference between the two maptypes (Mann-Whitney).')





