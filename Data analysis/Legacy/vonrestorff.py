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

# Print results
print("Word counts for maptype 's':")
for word, count in counts_s.items():
    print(f"{word}: {count}")

print("\nWord counts for maptype 'b':")
for word, count in counts_b.items():
    print(f"{word}: {count}")

# Perform chi-square test for each word
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

# Calculate overall statistics
total_s = sum(counts_s.values())
total_b = sum(counts_b.values())
avg_s = total_s / len(group_s)
avg_b = total_b / len(group_b)

print(f"\nOverall statistics:")
print(f"Total words remembered in group 's': {total_s}")
print(f"Total words remembered in group 'b': {total_b}")
print(f"Average words remembered per participant in group 's': {avg_s:.2f}")
print(f"Average words remembered per participant in group 'b': {avg_b:.2f}")

# Perform t-test for overall difference
t_statistic, p_value = stats.ttest_ind(
    [len(row) for row in group_s['remembered_words']],
    [len(row) for row in group_b['remembered_words']]
)

print(f"\nt-test for overall difference:")
print(f"t-statistic: {t_statistic:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("The overall difference between groups 's' and 'b' is statistically significant (p < 0.05).")
else:
    print("The overall difference between groups 's' and 'b' is not statistically significant (p >= 0.05).")

# Perform pairwise comparisons for 'hotel superior' vs other words
target_word = "hotel superior"
other_words = [word for word in words_to_check if word != target_word]

# Perform chi-square test for 'hotel superior' vs each other word
for word in other_words:
    hotel_superior_count = [counts_s[target_word] + counts_b[target_word]]
    other_word_count = [counts_s[word] + counts_b[word]]
    observed = np.array([hotel_superior_count, other_word_count])
    chi2, p_value, _, _ = stats.chi2_contingency(observed)
    
    print(f"\nChi-square test for 'hotel superior' vs '{word}':")
    print(f"Chi-square statistic: {chi2:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("'Hotel superior' is remembered significantly more than '{word}' (p < 0.05).")
    else:
        print("'Hotel superior' is not remembered significantly more than '{word}' (p >= 0.05).")



#================================================================================================

# Data for word counts (make sure these are the exact keys and values used)
s_word_counts = {
    'roscovina bank': 10,
    'roscovina art museum': 3,
    'midtown medical center': 4,
    'xavier hotel': 4,
    'lucy statue': 15,
    'hotel randalia': 3,
    'st. victor\'s cathedral': 10,
    'bank of randalia': 10,
    'dolby park': 16,
    'st. michael\'s cathedral': 12,
    'embers': 1,
    'civic center theatre': 1,
    'roscovina city library': 5,
    'randalia monument': 5,
    'hotel superior': 7,
    'the mill': 5,
    'randalia tower': 5,
    'harbor green': 5,
    'agnes theatre': 4
}

b_word_counts = {
    'roscovina bank': 10,
    'roscovina art museum': 7,
    'midtown medical center': 2,
    'xavier hotel': 3,
    'lucy statue': 8,
    'hotel randalia': 4,
    'st. victor\'s cathedral': 7,
    'bank of randalia': 10,
    'dolby park': 11,
    'st. michael\'s cathedral': 16,
    'embers': 7,
    'civic center theatre': 1,
    'roscovina city library': 4,
    'randalia monument': 21,
    'hotel superior': 15,
    'the mill': 9,
    'randalia tower': 7,
    'harbor green': 5,
    'agnes theatre': 4
}

# Prepare the DataFrame for plotting
data = {
    'Map Type': ['s'] * len(s_word_counts) + ['b'] * len(b_word_counts),
    'Location': list(s_word_counts.keys()) + list(b_word_counts.keys()),
    'Word Count': list(s_word_counts.values()) + list(b_word_counts.values())
}

df = pd.DataFrame(data)

# Bar plot
plt.figure(figsize=(12, 8))
sns.barplot(x='Location', y='Word Count', hue='Map Type', data=df, palette='coolwarm')
plt.xticks(rotation=90)
plt.title('Average Word Count by Map Type')
plt.xlabel('Location')
plt.ylabel('Word Count')
plt.legend(title='Map Type')
plt.tight_layout()
plt.show()

# Box plot
plt.figure(figsize=(12, 8))
sns.boxplot(x='Map Type', y='Word Count', data=df, palette='coolwarm')
plt.title('Distribution of Word Counts by Map Type')
plt.xlabel('Map Type')
plt.ylabel('Word Count')
plt.tight_layout()
plt.show()

# Data for Von Restorff effect including 'hotel superior'
von_restorff_data = {
    'Map Type': ['s', 'b'] + ['s', 'b'],
    'Location': ['hotel superior', 'hotel superior', 'other', 'other'],
    'Word Count': [7, 15, 118, 136]  # Adjust these values if needed
}

df_von_restorff = pd.DataFrame(von_restorff_data)

plt.figure(figsize=(12, 8))
sns.barplot(x='Location', y='Word Count', hue='Map Type', data=df_von_restorff, palette='coolwarm')
plt.xticks(rotation=0)
plt.title('Von Restorff Effect: Recall of Hotel Superior')
plt.xlabel('Location')
plt.ylabel('Word Count')
plt.legend(title='Map Type')
plt.tight_layout()
plt.show()

# Data for recall of 'hotel superior'
recall_data = {
    'Map Type': ['s', 'b'],
    'Recall Count': [8, 18],
    'Total Count': [88, 85]
}

df_recall = pd.DataFrame(recall_data)
df_recall['Recall Percentage'] = (df_recall['Recall Count'] / df_recall['Total Count']) * 100

plt.figure(figsize=(8, 6))
sns.barplot(x='Map Type', y='Recall Percentage', data=df_recall, palette='coolwarm')
plt.title('Recall Percentage of Hotel Superior by Map Type')
plt.xlabel('Map Type')
plt.ylabel('Recall Percentage')
plt.tight_layout()
plt.show()
