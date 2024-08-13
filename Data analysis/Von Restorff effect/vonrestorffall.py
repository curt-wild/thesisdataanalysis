import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Von Restorff effect\vonrestorff.csv'
# Read the CSV data
df = pd.read_csv(file_path, sep=';', encoding='latin1')
#-----------------------------------------------------------------


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

# Separate data for 's' and 'b' groups
group_s = df[df['maptype'] == 's']
group_b = df[df['maptype'] == 'b']

# Count occurrences for each word in both groups
counts_s = {word: sum(word in row for row in group_s['remembered_words']) for word in words_to_check}
counts_b = {word: sum(word in row for row in group_b['remembered_words']) for word in words_to_check}

# Find the 3 most remembered words by each group
top_s = sorted(counts_s, key=counts_s.get, reverse=True)[:3]
top_b = sorted(counts_b, key=counts_b.get, reverse=True)[:3]

# Count the average number of words remembered by each maptype
average_s = sum(counts_s.values()) / len(group_s)
average_b = sum(counts_b.values()) / len(group_b)

# Find the percentage of people remembering hotel superior by maptype
percentage_s = counts_s['hotel superior'] / len(group_s)
percentage_b = counts_b['hotel superior'] / len(group_b)
#-----------------------------------------------------------------


# Plot words remembered by maptype
plt.figure(figsize=(10, 6))
plt.barh(words_to_check, [counts_s[word] for word in words_to_check], color='blue', label='Maptype S')
plt.barh(words_to_check, [-counts_b[word] for word in words_to_check], color='red', label='Maptype B')
plt.xlabel('Number of Participants Remembering the Word')
plt.ylabel('Word')
plt.title('Remembered Words Distribution by Maptype')
plt.legend()
plt.show()

# Plot the percentage of people remembering hotel superior by maptype
plt.figure(figsize=(10, 6))
plt.bar(['Maptype S', 'Maptype B'], [percentage_s, percentage_b], color=['blue', 'red'])
plt.ylabel('Percentage of People Remembering Hotel Superior')
plt.title('Percentage of People Remembering Hotel Superior by Maptype')
plt.show()
#-----------------------------------------------------------------
# Do statistical test to compare the counts of each word between groups
for word in words_to_check:
    observed = np.array([[counts_s[word], len(group_s) - counts_s[word]],
                         [counts_b[word], len(group_b) - counts_b[word]]])
    chi2, p_value, _, _ = stats.chi2_contingency(observed)
    
    print(f"\nChi-square test for '{word}':")
    print(f"Chi-square statistic: {chi2:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("The difference between groups 's' and 'b' is statistically significant (p < 0.05).")
    else:
        print("The difference between groups 's' and 'b' is not statistically significant (p >= 0.05).")

#-----------------------------------------------------------------

# Print all results
print('number of people in group s:', len(group_s))
print('number of people in group b:', len(group_b))

print('number of people remembering hotel superior in group s:', counts_s['hotel superior'])
print('number of people remembering hotel superior in group b:', counts_b['hotel superior'])

print('average number of words remembered by group s:', average_s)
print('average number of words remembered by group b:', average_b)

print('top 3 words remembered by group s:', top_s)
print('top 3 words remembered by group b:', top_b)





