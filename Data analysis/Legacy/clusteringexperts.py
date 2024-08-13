import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency


# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Clustering illusion\clustering.csv'
data = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------------------------------

# Count the total number of people for each maptype with experience
total_maptype_s_exp_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes')].shape[0]
total_maptype_b_exp_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes')].shape[0]

# Count the amount of correct answers for each maptype with experience
correctanswer_experienceyes_maptype_s = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')].shape[0]
correctanswer_experienceyes_maptype_b = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')].shape[0]

# Check answers for each state column
columns_to_check = [
    'taraxa', 'phrengal', 'kovaire', 'cameron', 'ajaxa', 'centralia', 
    'laurenia', 'gelesia', 'ravinia', 'midian'
]

statecounts_maptype_s_exp_yes = data[(data['maptype'] == 's') & (data['experience'] == 'Yes')][columns_to_check].apply(lambda x: (x == 'Yes').sum())
statecounts_maptype_b_exp_yes = data[(data['maptype'] == 'b') & (data['experience'] == 'Yes')][columns_to_check].apply(lambda x: (x == 'Yes').sum())

# Calculate the average confidence for people who answered answered correctly with experience by maptype
average_confidence_maptype_s_exp_yes = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')]['confidence'].mean()
average_confidence_maptype_b_exp_yes = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')]['confidence'].mean()

# Counts
counts = {
    'Number of people with experience who answered correctly for maptype standard': correctanswer_experienceyes_maptype_s,
    'Number of people with experience who answered correctly for maptype bias': correctanswer_experienceyes_maptype_b
}
#-------------------------------------------------------------------------------------------------------------------------------------

# Plots
# Plot the percentage of correct answers for mapytype with experience
plt.figure(figsize=(10, 6))
sns.barplot(x=['Standard', 'Bias'], y=[correctanswer_experienceyes_maptype_s / total_maptype_s_exp_yes, correctanswer_experienceyes_maptype_b / total_maptype_b_exp_yes])
plt.title('Percentage of Correct Answers by Maptype with Experience')
plt.ylabel('Percentage of Correct Answers')
plt.show()

# Plot the percentage of responses for each state by maptype with experience
plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_check, y=statecounts_maptype_s_exp_yes / total_maptype_s_exp_yes)
plt.title('Percentage of Responses for Each State by Maptype with Experience')

plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_check, y=statecounts_maptype_b_exp_yes / total_maptype_b_exp_yes)  
plt.title('Percentage of Responses for Each State by Maptype with Experience')
plt.show()

# Plot the average confidence for correct answers by maptype with experience
plt.figure(figsize=(10, 6))
sns.barplot(x=['Standard', 'Bias'], y=[average_confidence_maptype_s_exp_yes, average_confidence_maptype_b_exp_yes])
plt.title('Average Confidence for Correct Answers by Maptype with Experience')
plt.ylabel('Average Confidence')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------

# Statistical Tests
# Perform a Fisher's exact test for the number of correct answers by maptype with experience
fisher_test_exp = fisher_exact([[correctanswer_experienceyes_maptype_s, correctanswer_experienceyes_maptype_b], 
                                [total_maptype_s_exp_yes, total_maptype_b_exp_yes]])

# Perform a Chi-squared test for the number of correct answers with experience
chi2_test_exp = chi2_contingency([[correctanswer_experienceyes_maptype_s, correctanswer_experienceyes_maptype_b], 
                                  [total_maptype_s_exp_yes, total_maptype_b_exp_yes]])
#-------------------------------------------------------------------------------------------------------------------------------------

# Print the results
print('Counts:')

for key, value in counts.items():
    print(f'{key}: {value}')

print('\nFisher\'s Exact Test for the number of correct answers by maptype with experience:')
print(f'p-value: {fisher_test_exp[1]}')

print('\nChi-squared Test for the number of correct answers with experience:')
print(f'p-value: {chi2_test_exp[1]}')

if fisher_test_exp[1] < 0.05:
    print('There is a significant difference between the number of correct answers by maptype with experience.')
else:
    print('There is no significant difference between the number of correct answers by maptype with experience.')

if chi2_test_exp[1] < 0.05:
    print('There is a significant difference between the number of correct answers by maptype with experience.')
else:
    print('There is no significant difference between the number of correct answers by maptype with experience.')




