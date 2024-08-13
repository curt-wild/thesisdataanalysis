import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, chi2_contingency


# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Clustering illusion\clustering.csv'
data = pd.read_csv(file_path, sep=';')


# Step 2: Perform the Specified Calculations

# 1. Count the total number of people with each maptype and experience
total_maptype_s = data[data['maptype'] == 's'].shape[0]
total_maptype_b = data[data['maptype'] == 'b'].shape[0]
total_experience_yes = data[data['experience'] == 'Yes'].shape[0]
total_experience_no = data[data['experience'] == 'No'].shape[0]

# 2. Count the total number of people who answered 'Yes' to 'idk'
total_idk_yes = data[data['idk'] == 'Yes'].shape[0]


# 3. Count the number of people who answered 'Yes' to 'nostate' for each maptype
maptype_s_nostate_yes = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes')].shape[0]
maptype_b_nostate_yes = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes')].shape[0]


# 4. Count the number of people with and without experience who answered correctly by maptype
correctanswer_experienceyes_maptype_s = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')].shape[0]
correctanswer_experienceno_maptype_s = data[(data['maptype'] == 's') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')].shape[0]
correctanswer_experienceyes_maptype_b = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'Yes')].shape[0]
correctanswer_experienceno_maptype_b = data[(data['maptype'] == 'b') & (data['nostate'] == 'Yes') & (data['experience'] == 'No')].shape[0]

# 5. Check answers for each state column
columns_to_check = [
    'taraxa', 'phrengal', 'kovaire', 'cameron', 'ajaxa', 'centralia', 
    'laurenia', 'gelesia', 'ravinia', 'midian'
]

yes_counts_maptype_s = data[data['maptype'] == 's'][columns_to_check].apply(lambda x: (x == 'Yes').sum())
yes_counts_maptype_b = data[data['maptype'] == 'b'][columns_to_check].apply(lambda x: (x == 'Yes').sum())

# 6. Calculate the average confidence for people who answered yes to nostate by maptype
average_confidence = data[data['nostate'] == 'Yes'].groupby('maptype')['confidence'].mean().reset_index()

# 7. Calculate the average confidence for people who answered yes to nostate by maptype and experience
average_confidence_yesno = data[data['nostate'] == 'Yes'].groupby(['maptype', 'experience'])['confidence'].mean().reset_index()

# Counts
counts = {
    'Total number of people with maptype standard': total_maptype_s,
    'Total number of people with maptype bias': total_maptype_b,
    'Total number of people with experience': total_experience_yes,
    'Total number of people without experience': total_experience_no,
    'Total number of people who answered no clue': total_idk_yes,
    'Number of people who answered correctly for maptype standard': maptype_s_nostate_yes,
    'Number of people who answered correctly for maptype bias': maptype_b_nostate_yes,
    'Number of people with experience who answered correctly for maptype standard': correctanswer_experienceyes_maptype_s,
    'Number of people without experience who answered correctly for maptype standard': correctanswer_experienceno_maptype_s,
    'Number of people with experience who answered correctly for maptype bias': correctanswer_experienceyes_maptype_b,
    'Number of people without experience who answered correctly for maptype bias': correctanswer_experienceno_maptype_b,
    'Yes counts for maptype standard': yes_counts_maptype_s.to_dict(),
    'Yes counts for maptype bias': yes_counts_maptype_b.to_dict(),
    'Average confidence by maptype': average_confidence.to_dict('records'),
    'Average confidence by maptype and experience': average_confidence_yesno.to_dict('records')
}




# Plotting the percentage of 'Yes' in nostate for each maptype
labels = ['Standard design', 'Bias inducing design']
total_counts = [total_maptype_s, total_maptype_b]
yes_percentages = [maptype_s_nostate_yes / total_maptype_s * 100, maptype_b_nostate_yes / total_maptype_b * 100]

plt.figure(figsize=(8, 6))
plt.bar(labels, yes_percentages, color='skyblue')
plt.xlabel('Map version')
plt.ylabel('Percentage of correct answers')
plt.title('Percentage of people who correctly characterized the points distribution')
plt.show()

# Plotting the counts for each column
plt.figure(figsize=(10, 6))
x = range(len(columns_to_check))
width = 0.35

plt.bar(x, yes_counts_maptype_s, width, label='Standard design', color='skyblue')
plt.bar([i + width for i in x], yes_counts_maptype_b, width, label='Bias inducing design', color='salmon')
plt.xlabel('Columns')
plt.ylabel('Number of correct answers')
plt.title('Number of answers for each column')

plt.xticks([i + width / 2 for i in x], columns_to_check, rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Plot correct answers by experience and maptype as percentages of experience totals
plt.figure(figsize=(10, 6))
x = range(4)
width = 0.35

plt.bar(x, [
    correctanswer_experienceyes_maptype_s / total_experience_yes * 100,
    correctanswer_experienceno_maptype_s / total_experience_no * 100,
    correctanswer_experienceyes_maptype_b / total_experience_yes * 100,
    correctanswer_experienceno_maptype_b / total_experience_no * 100
], width, color='skyblue')
plt.xlabel('Experience and map type')
plt.ylabel('Percentage of correct answers')
plt.title('Percentage of correct answers by experience and map type')
plt.xticks(x, ['Experience standard', 'No experience standard', 'Experience bias inducing', 'No experience bias'])
plt.tight_layout()
plt.show()

# Create a bar plot for the average confidence of contestants who gave correct answer by maptype
plt.figure(figsize=(8, 5))
sns.barplot(x='maptype', y='confidence', data=average_confidence, color='skyblue')
plt.title('Average Confidence Levels by Maptype')
plt.xlabel('Maptype')
plt.ylabel('Average Confidence Level')
plt.show()

# Create a bar plot for the average confidence of contestants who gave correct answer by maptype and experience
plt.figure(figsize=(10, 6))
sns.barplot(x='maptype', y='confidence', hue='experience', data=average_confidence_yesno)
plt.title('Average Confidence Levels by Maptype and Experience')
plt.xlabel('Maptype')
plt.ylabel('Average Confidence Level')
plt.legend(title='Experience')
plt.show()



# Fisher exact test
# Create a contingency table for Fisher's exact test
contingency_table_fisher = [
    [maptype_s_nostate_yes, total_maptype_s - maptype_s_nostate_yes],
    [maptype_b_nostate_yes, total_maptype_b - maptype_b_nostate_yes]
]

# Run Fisher exact test
oddsratio, pvalue_fisher = fisher_exact(contingency_table_fisher)

# Chi-square test
# Create a contingency table for Chi-square test
contingency_table_chi2 = pd.crosstab(data['maptype'], data['nostate'])

# Run Chi-square test
chi2, p_chi2, dof, expected = chi2_contingency(contingency_table_chi2)

# Print the results
test_results = {
    'Fisher exact test': {
        'Odds ratio': oddsratio,
        'p-value': pvalue_fisher
    },
    'Chi-square test': {
        'Chi-square': chi2,
        'p-value': p_chi2,
        'Degrees of freedom': dof,
        'Expected frequencies': expected
    }
}

for key, value in counts.items():
    print(f"{key}: {value}")

for key, value in test_results.items():
    print(f"{key}:")
    for k, v in value.items():
        print(f"{k}: {v}")

if pvalue_fisher < 0.05:
    print("The difference in the proportion of correct answers between the two map types is statistically significant (Fisher).")
else:
    print("The difference in the proportion of correct answers between the two map types is not statistically significant (Fisher).")

if p_chi2 < 0.05:
    print("The difference in the proportion of correct answers between the two map types is statistically significant (Chi).")
else:
    print("The difference in the proportion of correct answers between the two map types is not statistically significant (Chi).")


