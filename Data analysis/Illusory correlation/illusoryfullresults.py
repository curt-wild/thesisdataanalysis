import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency, mannwhitneyu

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Illusory correlation\illusory.csv'
data = pd.read_csv(file_path, sep=';')
#-------------------------------------------------------------------------------------------------------------------------------------

# Count the total number of people with each maptype
total_maptype_s = data[data['maptype'] == 's'].shape[0]
total_maptype_b = data[data['maptype'] == 'b'].shape[0]

# Count the number of people who answered correctly for each maptype
maptype_s_right = data[(data['maptype'] == 's') & (data['relation'] == 'No relationship')].shape[0]
maptype_b_right = data[(data['maptype'] == 'b') & (data['relation'] == 'No relationship')].shape[0]

# Count amount of people who answered incorrectly by maptype
maptype_wrong_answers = data[(data['relation'] != 'No relationship')].groupby(['maptype', 'relation']).size().reset_index(name='counts')


# Calculate the average confidence for people who answered corectly by maptype
average_confidence_s = data[(data['maptype'] == 's') & (data['relation'] == 'No relationship')]['confidence'].mean()
average_confidence_b = data[(data['maptype'] == 'b') & (data['relation'] == 'No relationship')]['confidence'].mean()

# Counts
counts = {'Total people maptype s': total_maptype_s,
          'Total people maptype b': total_maptype_b,
          'People who answered correctly maptype s': maptype_s_right,
          'People who answered correctly maptype b': maptype_b_right,
          'People who answered wrong': maptype_wrong_answers,}
#-------------------------------------------------------------------------------------------------------------------------------------

# Plotting the percentage of right answers by maptype
percentage_s_right = (maptype_s_right / total_maptype_s) * 100
percentage_b_right = (maptype_b_right / total_maptype_b) * 100

plt.figure(figsize=(8, 6))
sns.set_theme(font='Lato')
sns.barplot(x=['Standard', 'Bias-inducing'], y=[percentage_s_right, percentage_b_right],
            edgecolor='none')
plt.ylabel('Percentage of correct answers')
plt.show()


# Plotting the percentage of wrong answers by maptype
plt.figure(figsize=(8, 6))
sns.barplot(x='maptype', y='counts', hue='relation', data=maptype_wrong_answers)
plt.title('Percentage of Wrong Answers by Maptype')
plt.xlabel('Maptype')
plt.ylabel('Percentage')
plt.show()

# Plotting the average confidence by maptype
plt.figure(figsize=(8, 6))
sns.barplot(x=['Standard', 'Bias-inducing'], y=[average_confidence_s, average_confidence_b])
plt.title('Average Confidence by Maptype')
plt.ylabel('Average confidence')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------------

# Run statistical tests
# Run a Fisher's exact test to determine if the proportion of people who answered correctly is different by maptype
oddsratio, pvalue = fisher_exact([[maptype_s_right, total_maptype_s - maptype_s_right],
                                   [maptype_b_right, total_maptype_b - maptype_b_right]])
# Run a chi-squared test to determine if the proportion of people who answered correctly is different by maptype
chi2, pchi, dof, expected = chi2_contingency([[maptype_s_right, total_maptype_s - maptype_s_right],
                                                [maptype_b_right, total_maptype_b - maptype_b_right]])

# Run a mann-whitney test to determine if the average confidence is different by maptype
t_stat, t_p = mannwhitneyu(data[(data['maptype'] == 's') & (data['relation'] == 'No relationship')]['confidence'],
                            data[(data['maptype'] == 'b') & (data['relation'] == 'No relationship')]['confidence'])
#-------------------------------------------------------------------------------------------------------------------------------------

# Print the results
print('Counts:')
for key, value in counts.items():
    print(f'{key}: {value}')

# Print the statistical results
print('Statistical Results:')
print(f'Fisher\'s exact test p-value: {pvalue}')
print(f'Chi-squared test p-value: {pchi}')
print(f'Mann-Whitney U test p-value: {t_p}')

if pvalue < 0.05:
    print('There is a significant difference in the proportion of people who answered correctly by maptype')
else:
    print('There is no significant difference in the proportion of people who answered correctly by maptype')

if pchi < 0.05:
    print('There is a significant difference in the proportion of people who answered correctly by maptype')
else:
    print('There is no significant difference in the proportion of people who answered correctly by maptype')

if t_p < 0.05:
    print('There is a significant difference in the average confidence by maptype')
else:
    print('There is no significant difference in the average confidence by maptype')




