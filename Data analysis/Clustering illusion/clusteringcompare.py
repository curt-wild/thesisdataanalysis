import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency


# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Clustering illusion\clustering.csv'
data = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------------------------------

# Calculate the total number of people with each maptype and experience
total_maptype_s_exp_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes')].shape[0]
total_maptype_b_exp_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes')].shape[0]
total_maptype_s_exp_no = data[(data['maptype'] == 's') & (data['experience'] == 'No')].shape[0]
total_maptype_b_exp_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No')].shape[0]

# Count the number of people with and without experience who answered correctly by maptype
correctanswer_experienceyes_maptype_s = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')].shape[0]
correctanswer_experienceno_maptype_s = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')].shape[0]
correctanswer_experienceyes_maptype_b = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')].shape[0]
correctanswer_experienceno_maptype_b = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')].shape[0]

# Check answers for each state column
columns_to_check = [
    'taraxa', 'phrengal', 'kovaire', 'cameron', 'ajaxa', 'centralia', 
    'laurenia', 'gelesia', 'ravinia', 'midian'
]

yes_counts_maptype_s_exp_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes')][columns_to_check].apply(lambda x: (x == 'Yes').sum())
yes_counts_maptype_s_exp_no = data[(data['maptype'] == 's') & (data['experience'] == 'No')][columns_to_check].apply(lambda x: (x == 'Yes').sum())
yes_counts_maptype_b_exp_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes')][columns_to_check].apply(lambda x: (x == 'Yes').sum())
yes_counts_maptype_b_exp_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No')][columns_to_check].apply(lambda x: (x == 'Yes').sum())

# Calculate the average confidence for people who answered yes to nostate by maptype and experience
average_confidence_maptype_s_exp_yes = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')]['confidence'].mean()
average_confidence_maptype_s_exp_no = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')]['confidence'].mean()
average_confidence_maptype_b_exp_yes = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')]['confidence'].mean()
average_confidence_maptype_b_exp_no = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')]['confidence'].mean()

# Counts
counts = {
    'Number of people with experience who answered correctly for maptype standard': correctanswer_experienceyes_maptype_s,
    'Number of people without experience who answered correctly for maptype standard': correctanswer_experienceno_maptype_s,
    'Number of people with experience who answered correctly for maptype bias': correctanswer_experienceyes_maptype_b,
    'Number of people without experience who answered correctly for maptype bias': correctanswer_experienceno_maptype_b
}
#-------------------------------------------------------------------------------------------------------------------------------------

# Plots
# Plot the percentage of correct answers for maptype standard by experience
plt.figure(figsize=(10, 6))
sns.barplot(x=['With Experience', 'Without Experience'], y=[correctanswer_experienceyes_maptype_s / total_maptype_s_exp_yes, correctanswer_experienceno_maptype_s / total_maptype_s_exp_no])
plt.title('Percentage of Correct Answers for Standard Maptype by Experience')
plt.ylabel('Percentage of Correct Answers')
plt.show()

# Plot the percentage of correct answers for maptype bias by experience
plt.figure(figsize=(10, 6))
sns.barplot(x=['With Experience', 'Without Experience'], y=[correctanswer_experienceyes_maptype_b / total_maptype_b_exp_yes, correctanswer_experienceno_maptype_b / total_maptype_b_exp_no])
plt.title('Percentage of Correct Answers for Bias Maptype by Experience')
plt.ylabel('Percentage of Correct Answers')
plt.show()

# Plot the percentage of responses for each state by maptype and experience
plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_check, y=yes_counts_maptype_s_exp_yes / total_maptype_s_exp_yes)
plt.title('Percentage of Responses for Each State (Standard Maptype and Experience)')

plt.ylabel('Percentage of Responses')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_check, y=yes_counts_maptype_s_exp_no / total_maptype_s_exp_no)
plt.title('Percentage of Responses for Each State (Standard Maptype and No Experience)')
plt.ylabel('Percentage of Responses')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_check, y=yes_counts_maptype_b_exp_yes / total_maptype_b_exp_yes)
plt.title('Percentage of Responses for Each State (Bias Maptype and Experience)')
plt.ylabel('Percentage of Responses')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_check, y=yes_counts_maptype_b_exp_no / total_maptype_b_exp_no)
plt.title('Percentage of Responses for Each State (Bias Maptype and No Experience)')
plt.ylabel('Percentage of Responses')
plt.xticks(rotation=45)
plt.show()

# Plot the average confidence for people who answered yes to nostate by maptype and experience
plt.figure(figsize=(10, 6))
sns.barplot(x=['Standard with experience', 'Standard without experience', 'Bias with experience', 'Bias without experience'], 
            y=[average_confidence_maptype_s_exp_yes, average_confidence_maptype_s_exp_no, average_confidence_maptype_b_exp_yes, average_confidence_maptype_b_exp_no])
plt.title('Average Confidence Levels by Maptype and Experience')
plt.ylabel('Average Confidence')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------

# Do statistical tests
# Perform a Fisher's exact test for the number of correct answers for mapype standard by experience
odds_ratio_s, p_value_s = fisher_exact([[correctanswer_experienceyes_maptype_s, total_maptype_s_exp_yes - correctanswer_experienceyes_maptype_s], 
                                       [correctanswer_experienceno_maptype_s, total_maptype_s_exp_no - correctanswer_experienceno_maptype_s]])

# Perform a chi-squared test for the number of correct answers for mapype standard by experience
chi2_s, chi2_p_s, _, _ = chi2_contingency([[correctanswer_experienceyes_maptype_s, total_maptype_s_exp_yes - correctanswer_experienceyes_maptype_s], 
                                          [correctanswer_experienceno_maptype_s, total_maptype_s_exp_no - correctanswer_experienceno_maptype_s]])

# Perform a Fisher's exact test for the number of correct answers for mapype bias by experience
odds_ratio_b, p_value_b = fisher_exact([[correctanswer_experienceyes_maptype_b, total_maptype_b_exp_yes - correctanswer_experienceyes_maptype_b], 
                                       [correctanswer_experienceno_maptype_b, total_maptype_b_exp_no - correctanswer_experienceno_maptype_b]])

# Perform a chi-squared test for the number of correct answers for mapype bias by experience
chi2_b, chi2_p_b, _, _ = chi2_contingency([[correctanswer_experienceyes_maptype_b, total_maptype_b_exp_yes - correctanswer_experienceyes_maptype_b], 
                                          [correctanswer_experienceno_maptype_b, total_maptype_b_exp_no - correctanswer_experienceno_maptype_b]])
#-------------------------------------------------------------------------------------------------------------------------------------

# Print counts and test results
print('Counts:')
for key, value in counts.items():
    print(f'{key}: {value}')

print('\nTest results:')
print('Standard maptype:')
print(f'Fisher exact test: Odds ratio = {odds_ratio_s}, p-value = {p_value_s}')
print(f'Chi-squared test: Chi-squared = {chi2_s}, p-value = {chi2_p_s}')

if p_value_s < 0.05:
    print('There is a significant difference in the number of correct answers for maptype standard by experience')
else:
    print('There is no significant difference in the number of correct answers for maptype standard by experience')

print('\nBias maptype:')
print(f'Fisher exact test: Odds ratio = {odds_ratio_b}, p-value = {p_value_b}')
print(f'Chi-squared test: Chi-squared = {chi2_b}, p-value = {chi2_p_b}')

if p_value_b < 0.05:
    print('There is a significant difference in the number of correct answers for maptype bias by experience')
else:
    print('There is no significant difference in the number of correct answers for maptype bias by experience')



