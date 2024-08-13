import pandas as pd
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency

import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Clustering illusion\clustering.csv'
data = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------------------------------

# Count the total number of people for each maptype without experience
total_maptype_s_exp_no = data[(data['maptype'] == 's') & (data['experience'] == 'No')].shape[0]
total_maptype_b_exp_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No')].shape[0]

# Count the amount of correct answers for each maptype without experience
correctanswer_experienceno_maptype_s = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')].shape[0]
correctanswer_experienceno_maptype_b = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')].shape[0]

# Check answers for each state column
columns_to_check = [
    'taraxa', 'phrengal', 'kovaire', 'cameron', 'ajaxa', 'centralia', 
    'laurenia', 'gelesia', 'ravinia', 'midian'
]

statecounts_maptype_s_exp_no = data[(data['maptype'] == 's') & (data['experience'] == 'No')][columns_to_check].apply(lambda x: (x == 'Yes').sum())
statecounts_maptype_b_exp_no = data[(data['maptype'] == 'b') & (data['experience'] == 'No')][columns_to_check].apply(lambda x: (x == 'Yes').sum())

# Calculate the average confidence for people who answered correctly without experience by maptype
average_confidence_maptype_s_exp_no = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')]['confidence'].mean()
average_confidence_maptype_b_exp_no = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')]['confidence'].mean()

# Counts
counts = {
    'Number of people without experience who answered correctly for maptype standard': correctanswer_experienceno_maptype_s,
    'Number of people without experience who answered correctly for maptype bias': correctanswer_experienceno_maptype_b
}
#-------------------------------------------------------------------------------------------------------------------------------------

# Plots
# Plot the percentage of correct answers for maptype without experience
plt.figure(figsize=(10, 6))
sns.barplot(x=['Standard', 'Bias'], y=[correctanswer_experienceno_maptype_s / total_maptype_s_exp_no, correctanswer_experienceno_maptype_b / total_maptype_b_exp_no])
plt.title('Percentage of Correct Answers by Maptype without Experience')
plt.ylabel('Percentage of Correct Answers')
plt.show()

# Plot the percentage of responses for each state by maptype without experience
plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_check, y=statecounts_maptype_s_exp_no / total_maptype_s_exp_no)
plt.title('Percentage of Responses for Each State by Maptype without Experience')

plt.figure(figsize=(10, 6))
sns.barplot(x=columns_to_check, y=statecounts_maptype_b_exp_no / total_maptype_b_exp_no)  
plt.title('Percentage of Responses for Each State by Maptype without Experience')
plt.show()

# Plot the average confidence for correct answers by maptype without experience
plt.figure(figsize=(10, 6))
sns.barplot(x=['Standard', 'Bias'], y=[average_confidence_maptype_s_exp_no, average_confidence_maptype_b_exp_no])
plt.title('Average Confidence for Correct Answers by Maptype without Experience')
plt.ylabel('Average Confidence')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------

# Statistical Tests
# Perform a Fisher's exact test for the number of correct answers by maptype without experience
fisher_test_exp = fisher_exact([[correctanswer_experienceno_maptype_s, correctanswer_experienceno_maptype_b], 
                                [total_maptype_s_exp_no, total_maptype_b_exp_no]])

# Perform a Chi-squared test for the number of correct answers without experience
chi2_test_exp = chi2_contingency([[correctanswer_experienceno_maptype_s, correctanswer_experienceno_maptype_b], 
                                  [total_maptype_s_exp_no, total_maptype_b_exp_no]])
#-------------------------------------------------------------------------------------------------------------------------------------

# Print the results
print('Counts:')

for key, value in counts.items():
    print(f'{key}: {value}')

print('\nFisher\'s Exact Test for the number of correct answers by maptype without experience:')
print(f'p-value: {fisher_test_exp[1]}')

print('\nChi-squared Test for the number of correct answers without experience:')
print(f'p-value: {chi2_test_exp[1]}')

if fisher_test_exp[1] < 0.05:
    print('There is a significant difference between the number of correct answers by maptype without experience.')
else:
    print('There is no significant difference between the number of correct answers by maptype without experience.')

if chi2_test_exp[1] < 0.05:
    print('There is a significant difference between the number of correct answers by maptype without experience.')
else:
    print('There is no significant difference between the number of correct answers by maptype without experience.')
