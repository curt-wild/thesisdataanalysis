import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Ostrich effect\ostrich.csv'
# Read the CSV data
df = pd.read_csv(file_path, sep=';')

# Convert 'time' column to numeric, replacing comma with dot
df['time'] = df['time'].str.replace(',', '.').astype(float)
#-------------------------------------------------------------------------------------------------------------

# Separate data for maptypes and experience yes or no
s_times_expyes = df[(df['maptype'] == 's') & (df['experience'] == 'Yes')]['time']
b_times_expyes = df[(df['maptype'] == 'b') & (df['experience'] == 'Yes')]['time']
s_times_expno = df[(df['maptype'] == 's') & (df['experience'] == 'No')]['time']
b_times_expno = df[(df['maptype'] == 'b') & (df['experience'] == 'No')]['time']

# Calculate basic statistics
s_stats_expyes = s_times_expyes.describe()
b_stats_expyes = b_times_expyes.describe()
s_stats_expno = s_times_expno.describe()
b_stats_expno = b_times_expno.describe()

# Count the number of answers per maptype and experience
s_answers_expyes = df[(df['maptype'] == 's') & (df['experience'] == 'Yes')].shape[0]
b_answers_expyes = df[(df['maptype'] == 'b') & (df['experience'] == 'Yes')].shape[0]
s_answers_expno = df[(df['maptype'] == 's') & (df['experience'] == 'No')].shape[0]
b_answers_expno = df[(df['maptype'] == 'b') & (df['experience'] == 'No')].shape[0]

# Count the number of correct answers (as one increases, so does the other in column relation) per maptype and experience
s_correct_expyes = df[(df['maptype'] == 's') & (df['experience'] == 'Yes') & (df['relation'] == 'As one increases, so does the other')].shape[0]
b_correct_expyes = df[(df['maptype'] == 'b') & (df['experience'] == 'Yes') & (df['relation'] == 'As one increases, so does the other')].shape[0]
s_correct_expno = df[(df['maptype'] == 's') & (df['experience'] == 'No') & (df['relation'] == 'As one increases, so does the other')].shape[0]
b_correct_expno = df[(df['maptype'] == 'b') & (df['experience'] == 'No') & (df['relation'] == 'As one increases, so does the other')].shape[0]
#-------------------------------------------------------------------------------------------------------------

# Visualize the distribution of times for each maptype and experience
plt.figure(figsize=(10, 6))
plt.boxplot([s_times_expyes, b_times_expyes, s_times_expno, b_times_expno], labels=['s experience yes', 'b experience yes', 's experience no', 'b experience no'])
plt.title('Distribution of Times for Maptype s and b')
plt.ylabel('Time')
plt.show()

#Create a histogram for maptype s
plt.figure(figsize=(10, 6))
plt.hist(s_times_expyes, bins=20, alpha=0.5, label='s experience yes')
plt.hist(s_times_expno, bins=20, alpha=0.5, label='s experience no')
plt.legend(loc='upper right')
plt.title('Distribution of Times for Maptype s')
plt.ylabel('Time')
plt.show()

#Create a histogram for maptype b
plt.figure(figsize=(10, 6))
plt.hist(b_times_expyes, bins=20, alpha=0.5, label='b experience yes')
plt.hist(b_times_expno, bins=20, alpha=0.5, label='b experience no')
plt.legend(loc='upper right')
plt.title('Distribution of Times for Maptype b')
plt.ylabel('Time')
plt.show()

# Plot the percentage of correct answers for maptype s
plt.figure(figsize=(10, 6))
plt.bar(['s experience yes', 's experience no'], [s_correct_expyes/s_answers_expyes, s_correct_expno/s_answers_expno])
plt.title('Percentage of correct answers for maptype s')
plt.ylabel('Percentage of correct answers')
plt.show()

# Plot the percentage of correct answers for maptype b
plt.figure(figsize=(10, 6))
plt.bar(['b experience yes', 'b experience no'], [b_correct_expyes/b_answers_expyes, b_correct_expno/b_answers_expno])
plt.title('Percentage of correct answers for maptype b')
plt.ylabel('Percentage of correct answers')
plt.show()
#-------------------------------------------------------------------------------------------------------------

# Perform a t-test to compare the times for maptype s
t_statistic_s, p_value_s = stats.ttest_ind(s_times_expyes, s_times_expno)

# Perform a t-test to compare the times for maptype b
t_statistic_b, p_value_b = stats.ttest_ind(b_times_expyes, b_times_expno)
# -------------------------------------------------------------------------------------------------------------

# Print the results
print('Results for maptype s:')
print(stats.describe(s_times_expyes))
print(stats.describe(s_times_expno))
print('t test results for maptype s:')
print(t_statistic_s)
print(p_value_s)
if p_value_s < 0.05:
    print('The difference in times for maptype s is statistically significant')
else:
    print('The difference in times for maptype s is not statistically significant')


print('Results for maptype b:')
print(stats.describe(b_times_expyes))
print(stats.describe(b_times_expno))
print('t test results for maptype b:')
print(t_statistic_b)
print(p_value_b)
if p_value_b < 0.05:
    print('The difference in times for maptype b is statistically significant')
else:
    print('The difference in times for maptype b is not statistically significant')






