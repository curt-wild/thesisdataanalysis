import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Illusory correlation\illusory.csv'
data = pd.read_csv(file_path, sep=';')

# Count the total number of people with each maptype and experience
total_maptype_s = data[data['maptype'] == 's'].shape[0]
total_maptype_b = data[data['maptype'] == 'b'].shape[0]
total_experience_yes = data[data['experience'] == 'Yes'].shape[0]
total_experience_no = data[data['experience'] == 'No'].shape[0]


# Count the total number of people who answered I have no clue to relation
total_idk_yes = data[data['relation'] == 'I have no clue'].shape[0]

# 3. Count the number of people who answered no relationship to relation for each maptype
maptype_s_right = data[(data['maptype'] == 's') & (data['relation'] == 'No relationship')].shape[0]
maptype_b_right = data[(data['maptype'] == 'b') & (data['relation'] == 'No relationship')].shape[0]


# 4. Count the number of people with and without experience who answered correctly by maptype
correctanswer_experienceyes_maptype_s = data[(data['experience'] == 'Yes') & (data['maptype'] == 's') & (data['relation'] == 'No relationship')].shape[0]
correctanswer_experienceno_maptype_s = data[(data['experience'] == 'No') & (data['maptype'] == 's') & (data['relation'] == 'No relationship')].shape[0]
correctanswer_experienceyes_maptype_b = data[(data['experience'] == 'Yes') & (data['maptype'] == 'b') & (data['relation'] == 'No relationship')].shape[0]
correctanswer_experienceno_maptype_b = data[(data['experience'] == 'No') & (data['maptype'] == 'b') & (data['relation'] == 'No relationship')].shape[0]

# Calculate the average confidence for people who answered no relationship to relation by maptype
average_confidence = data[data['relation'] == 'No relationship'].groupby('maptype')['confidence'].mean().reset_index()


# 7. Calculate the average confidence for people who answered no relation to relation by maptype and experience
average_confidence_yesno = data[data['relation'] == 'No relationship'].groupby(['maptype', 'experience'])['confidence'].mean().reset_index()



# Plotting the percentage of right answers by maptype
percentage_s_right = (maptype_s_right / total_maptype_s) * 100
percentage_b_right = (maptype_b_right / total_maptype_b) * 100


plt.figure(figsize=(8, 6))
sns.barplot(x=['maptype_s', 'maptype_b'], y=[percentage_s_right, percentage_b_right])
plt.title('Percentage of Right Answers by Maptype')
plt.xlabel('Maptype')
plt.ylabel('Percentage')
plt.show()

# Plotting the percentage of right answers by experience
percentage_experience_yes = (correctanswer_experienceyes_maptype_s / total_experience_yes) * 100
percentage_experience_no = (correctanswer_experienceno_maptype_s / total_experience_no) * 100

plt.figure(figsize=(8, 6))
sns.barplot(x=['Experience Yes', 'Experience No'], y=[percentage_experience_yes, percentage_experience_no])
plt.title('Percentage of Right Answers by Experience')
plt.xlabel('Experience')
plt.ylabel('Percentage')
plt.show()

# Plotting the percentage of right answers by maptype and experience
percentage_experience_yes_maptype_s = (correctanswer_experienceyes_maptype_s / total_experience_yes) * 100
percentage_experience_no_maptype_s = (correctanswer_experienceno_maptype_s / total_experience_no) * 100
percentage_experience_yes_maptype_b = (correctanswer_experienceyes_maptype_b / total_experience_yes) * 100
percentage_experience_no_maptype_b = (correctanswer_experienceno_maptype_b / total_experience_no) * 100

plt.figure(figsize=(8, 6))
sns.barplot(x=['Experience Yes Maptype S', 'Experience No Maptype S', 'Experience Yes Maptype B', 'Experience No Maptype B'], y=[percentage_experience_yes_maptype_s, percentage_experience_no_maptype_s, percentage_experience_yes_maptype_b, percentage_experience_no_maptype_b])
plt.title('Percentage of Right Answers by Experience and Maptype')
plt.xlabel('Experience and Maptype')
plt.ylabel('Percentage')
plt.show()


# Counts
counts = {
    'Total number of people with maptype standard': total_maptype_s,
    'Total number of people with maptype bias': total_maptype_b,
    'Total number of people with experience': total_experience_yes,
    'Total number of people without experience': total_experience_no,
    'Total number of people who answered no clue': total_idk_yes,
    'Number of people who answered correctly for maptype standard': maptype_s_right,
    'Number of people who answered correctly for maptype bias': maptype_b_right,
    'Percentage of people who answered correctly for maptype standard': percentage_s_right,
    'Percentage of people who answered correctly for maptype bias': percentage_b_right,
    'Number of people with experience who answered correctly for maptype standard': correctanswer_experienceyes_maptype_s,
    'Number of people without experience who answered correctly for maptype standard': correctanswer_experienceno_maptype_s,
    'Number of people with experience who answered correctly for maptype bias': correctanswer_experienceyes_maptype_b,
    'Number of people without experience who answered correctly for maptype bias': correctanswer_experienceno_maptype_b,
}

for key, value in counts.items():
    print(f'{key}: {value}')

# Run statistical tests
# Create a contingency table
contingency_table = [
    [maptype_s_right, maptype_b_right],
    [total_maptype_s - maptype_s_right, total_maptype_b - maptype_b_right]
]


# Perform the Fisher's exact test
oddsratio, pvalue = fisher_exact(contingency_table)

# Perform the Chi-square test
chi2, p_chi2, dof, expected = chi2_contingency(contingency_table)

# Print the results
test_results = {
    'Fisher exact test': {
        'Odds ratio': oddsratio,
        'p-value': pvalue
    },
    'Chi-square test': {
        'Chi-square': chi2,
        'p-value': p_chi2,
        'Degrees of freedom': dof,
        'Expected frequencies': expected
    }
}

for key, value in test_results.items():
    print(f'{key}: {value}')

if pvalue < 0.05:
    print('There is a significant difference between the two maptypes')
else:
    print('There is no significant difference between the two maptypes')
    


