import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the uploaded CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Von Restorff effect\vonrestorff.csv'
df = pd.read_csv(file_path, sep=';', encoding='latin1')
#---------------------------------------------------------------

# List of words to check
words_to_check = [
    "roscovina bank", "roscovina art museum", "midtown medical center", "xavier hotel",
    "lucy statue", "hotel randalia", "st. victor's cathedral", "bank of randalia",
    "dolby park", "st. michael's cathedral", "embers", "civic center theatre",
    "roscovina city library", "randalia monument", "hotel superior", "the mill",
    "randalia tower", "harbor green", "agnes theatre"
]

# Function to count remembered words for a participant
def count_remembered_words(row):
    remembered = set()
    for col in [f'place{i}' for i in range(1, 20)]:
        if pd.notna(row[col]):
            for word in words_to_check:
                if fuzz.ratio(row[col].lower(), word.lower()) >= 60:
                    remembered.add(word)
    return list(remembered)

# Apply the function to each row
df['remembered_words'] = df.apply(count_remembered_words, axis=1)

# Separate data for 's' and 'b' groups and experience yes and no
group_s_yes = df[(df['maptype'] == 's') & (df['experience'] == 'Yes')]
group_s_no = df[(df['maptype'] == 's') & (df['experience'] == 'No')]

group_b_yes = df[(df['maptype'] == 'b') & (df['experience'] == 'Yes')]
group_b_no = df[(df['maptype'] == 'b') & (df['experience'] == 'No')]

# Count occurrences for each word in the four groups
counts_s_exp_yes = {word: sum(word in row for row in group_s_yes['remembered_words']) for word in words_to_check}
counts_s_exp_no = {word: sum(word in row for row in group_s_no['remembered_words']) for word in words_to_check}

counts_b_exp_yes = {word: sum(word in row for row in group_b_yes['remembered_words']) for word in words_to_check}
counts_b_exp_no = {word: sum(word in row for row in group_b_no['remembered_words']) for word in words_to_check}

# Find the 3 most remembered words by each of the four groups
top_s_yes = sorted(counts_s_exp_yes, key=counts_s_exp_yes.get, reverse=True)[:3]
top_s_no = sorted(counts_s_exp_no, key=counts_s_exp_no.get, reverse=True)[:3]

top_b_yes = sorted(counts_b_exp_yes, key=counts_b_exp_yes.get, reverse=True)[:3]
top_b_no = sorted(counts_b_exp_no, key=counts_b_exp_no.get, reverse=True)[:3]

# Count the average number of words remembered by each group
average_s_yes = sum(counts_s_exp_yes.values()) / len(group_s_yes)
average_s_no = sum(counts_s_exp_no.values()) / len(group_s_no)

average_b_yes = sum(counts_b_exp_yes.values()) / len(group_b_yes)
average_b_no = sum(counts_b_exp_no.values()) / len(group_b_no)

# Find the percentage of people remembering hotel superior by group
percentage_s_yes = counts_s_exp_yes['hotel superior'] / len(group_s_yes)
percentage_s_no = counts_s_exp_no['hotel superior'] / len(group_s_no) 

percentage_b_yes = counts_b_exp_yes['hotel superior'] / len(group_b_yes) 
percentage_b_no = counts_b_exp_no['hotel superior'] / len(group_b_no) 

# Plot words remembered by group
plt.figure(figsize=(10, 6))
plt.barh(words_to_check, [counts_s_exp_yes[word] for word in words_to_check], color='blue', label='Maptype S Experience Yes')
plt.barh(words_to_check, [-counts_s_exp_no[word] for word in words_to_check], color='red', label='Maptype S Experience No')
plt.barh(words_to_check, [counts_b_exp_yes[word] for word in words_to_check], color='green', label='Maptype B Experience Yes')
plt.barh(words_to_check, [-counts_b_exp_no[word] for word in words_to_check], color='yellow', label='Maptype B Experience No')
plt.xlabel('Number of Participants Remembering the Word')
plt.ylabel('Word')
plt.title('Remembered Words Distribution by Group')
plt.legend()
plt.show()

# Plot the percentage of people remembering hotel superior by group
plt.figure(figsize=(10, 6))
plt.bar(['Maptype S Experience Yes', 'Maptype S Experience No', 'Maptype B Experience Yes', 'Maptype B Experience No'], [percentage_s_yes, percentage_s_no, percentage_b_yes, percentage_b_no], color=['blue', 'red', 'green', 'yellow'])
plt.ylabel('Percentage of People Remembering Hotel Superior')
plt.title('Percentage of People Remembering Hotel Superior by Group')
plt.show()

# Do statistical test to compare the word hotel superior between experience yes and no for each maptype
observed_s = np.array([[counts_s_exp_yes['hotel superior'], len(group_s_yes) - counts_s_exp_yes['hotel superior']],
                       [counts_s_exp_no['hotel superior'], len(group_s_no) - counts_s_exp_no['hotel superior']]])

observed_b = np.array([[counts_b_exp_yes['hotel superior'], len(group_b_yes) - counts_b_exp_yes['hotel superior']],
                          [counts_b_exp_no['hotel superior'], len(group_b_no) - counts_b_exp_no['hotel superior']]])

chi2_s, p_value_s, _, _ = stats.chi2_contingency(observed_s)
chi2_b, p_value_b, _, _ = stats.chi2_contingency(observed_b)

print("\nChi-square test for 'hotel superior' in maptype S:")
print(f"Chi-square statistic: {chi2_s:.4f}")
print(f"p-value: {p_value_s:.4f}")

if p_value_s < 0.05:
    print("The difference between experience yes and no in group 's' is statistically significant (p < 0.05).")
else:
    print("The difference between experience yes and no in group 's' is not statistically significant (p >= 0.05).")

print("\nChi-square test for 'hotel superior' in maptype B:")
print(f"Chi-square statistic: {chi2_b:.4f}")
print(f"p-value: {p_value_b:.4f}")

if p_value_b < 0.05:
    print("The difference between experience yes and no in group 'b' is statistically significant (p < 0.05).")
else:
    print("The difference between experience yes and no in group 'b' is not statistically significant (p >= 0.05).")

# Print all results
print('number of people in group s experience yes:', len(group_s_yes))
print('number of people in group s experience no:', len(group_s_no))
print('number of people in group b experience yes:', len(group_b_yes))
print('number of people in group b experience no:', len(group_b_no))

print('number of people remembering hotel superior in group s experience yes:', counts_s_exp_yes['hotel superior'])
print('number of people remembering hotel superior in group s experience no:', counts_s_exp_no['hotel superior'])
print('number of people remembering hotel superior in group b experience yes:', counts_b_exp_yes['hotel superior'])
print('number of people remembering hotel superior in group b experience no:', counts_b_exp_no['hotel superior'])

print('average number of words remembered by group s experience yes:', average_s_yes)
print('average number of words remembered by group s experience no:', average_s_no)
print('average number of words remembered by group b experience yes:', average_b_yes)
print('average number of words remembered by group b experience no:', average_b_no)

print('top 3 words remembered by group s experience yes:', top_s_yes)
print('top 3 words remembered by group s experience no:', top_s_no)
print('top 3 words remembered by group b experience yes:', top_b_yes)
print('top 3 words remembered by group b experience no:', top_b_no)

