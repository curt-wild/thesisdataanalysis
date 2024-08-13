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

# Apply the function to each row and save the result as a new column
df['remembered_words'] = df.apply(count_remembered_words, axis=1)

# Separate data for 's' and 'b' groups
group_s = df[df['maptype'] == 's']
group_b = df[df['maptype'] == 'b']

# Further disaggregate into experience yes and no
group_s_yes = group_s[group_s['experience'] == 'yes']
group_s_no = group_s[group_s['experience'] == 'no']

group_b_yes = group_b[group_b['experience'] == 'yes']
group_b_no = group_b[group_b['experience'] == 'no']

# Count occurrences for each word in the four groups
counts_s_exp_yes = {word: sum(word in row for row in group_s_yes['remembered_words']) for word in words_to_check}
counts_s_exp_no = {word: sum(word in row for row in group_s_no['remembered_words']) for word in words_to_check}

counts_b_exp_yes = {word: sum(word in row for row in group_b_yes['remembered_words']) for word in words_to_check}
counts_b_exp_no = {word: sum(word in row for row in group_b_no['remembered_words']) for word in words_to_check}

"""
# Calculate average words remembered by each group
average_s = sum(group_s['remembered_words'].apply(len)) / len(group_s)
average_b = sum(group_b['remembered_words'].apply(len)) / len(group_b)

average_s_yes = sum(group_s_yes['remembered_words'].apply(len)) / len(group_s_yes)
average_s_no = sum(group_s_no['remembered_words'].apply(len)) / len(group_s_no)



""""""

# Count the average number of words remembered by each maptype and experience
average_s_exp_yes = sum(counts_s_exp_yes.values()) / len(group_s_yes)
average_s_exp_no = sum(counts_s_exp_no.values()) / len(group_s_no)

average_b_exp_yes = sum(counts_b_exp_yes.values()) / len(group_b_yes)
average_b_exp_no = sum(counts_b_exp_no.values()) / len(group_b_no)

# Find the percentage of people remembering hotel superior by maptype and experience
percentage_s_exp_yes = counts_s_exp_yes['hotel superior'] / len(group_s_yes)
percentage_s_exp_no = counts_s_exp_no['hotel superior'] / len(group_s_no)

percentage_b_exp_yes = counts_b_exp_yes['hotel superior'] / len(group_b_yes)
percentage_b_exp_no = counts_b_exp_no['hotel superior'] / len(group_b_no)
#----------------------------------------------------------------
"""
print('counts_s_exp_yes:', counts_s_exp_yes)    
print('counts_s_exp_no:', counts_s_exp_no)
print('counts_b_exp_yes:', counts_b_exp_yes)
print('counts_b_exp_no:', counts_b_exp_no)

