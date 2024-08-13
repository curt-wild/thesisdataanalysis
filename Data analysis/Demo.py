import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
file_path = r'C:\Users\nicol\OneDrive - Universidad de los andes\CartoMSCThesis\Data analysis\Demo.csv'
data = pd.read_csv(file_path, sep=';') 
#-------------------------------------------------------------

# Data exploration
birthcountry = data['birthcountry'].value_counts()

# Continent distribution
north_america = data[data['birthcountry'].isin(['United States', 'Canada', 'Mexico'])]
south_america = data[data['birthcountry'].isin(['Colombia', 'Brazil', 'Argentina'])]
europe = data[data['birthcountry'].isin(['Germany', 'Russia', 'France', 'Austria', 'Italy', 'Greece', 'Poland', 
                                         'United Kingdom', 'Spain', 'Portugal', 'Finland', 'Netherlands', 'Sweden', 
                                         'Belgium', 'Latvia', 'Estonia'])]
asia = data[data['birthcountry'].isin(['Malaysia', 'China', 'Japan', 'Turkey', 'Nepal', 'Israel'])]
africa = data[data['birthcountry'].isin(['South Africa', 'Nigeria', 'Egypt'])]
other = data[data['birthcountry'].isin(["Other / I'd rather not say"])]


# Age distribution
age = data['age']
agestats = age.describe()

# Age groups
# Young adults 17-30
age_17_30 = data[(data['age'] > 16) & (data['age'] <= 30)]
# Middle age adults 31-45
age_31_45 = data[(data['age'] > 30) & (data['age'] <= 45)]
# Old age adults 46-60
age_46_60 = data[(data['age'] > 45) & (data['age'] <= 60)]
# Elderly 61-75 
age_61_75 = data[(data['age'] > 60) & (data['age'] <= 75)]

# Count empty cells in the age column
notsay_age = data['age'].isnull().sum()

# Colorblind yes or no 
colorblind = data['colorblind'].value_counts()

# Gender distribution
gender = data['gender'].value_counts()

# Experience yes or no  
experience = data['experience'].value_counts()

#-------------------------------------------------------------
# Data visualization
# Age distribution
plt.figure()
sns.set_theme(font='Lato') 
sns.histplot(age, bins=len(age.unique()), kde=True, edgecolor='none')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# Age groups distribution pie chart include not say
labels = ['17-30', '31-45', '46-60', '61-75', 'Not say']
sizes = [len(age_17_30), len(age_31_45), len(age_46_60), len(age_61_75), notsay_age]
plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()

# Age groups distribution bar chart include not say
labels = ['17-30', '31-45', '46-60', '61-75', 'Not say']
sizes = [len(age_17_30), len(age_31_45), len(age_46_60), len(age_61_75), notsay_age]
plt.figure()
plt.bar(labels, sizes)
plt.xlabel('Age group')
plt.ylabel('Frequency')
plt.show()

# Birth country distribution
plt.figure()
birthcountry.plot(kind='bar')
plt.xlabel('Country')
plt.ylabel('Frequency')
plt.show()

# Continent distribution pie chart
labels = ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Other / I\'d rather not say']
sizes = [len(north_america), len(south_america), len(europe), len(asia), len(africa), len(other)]
plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()

# Colorblind distribution pie chart
labels = ['Yes', 'No']
sizes = [colorblind[1], colorblind[0]]
plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()

# Gender distribution pie chart
labels = ['Male', 'Female', 'Diverse', 'Prefer not to say']
sizes = [gender['Male'], gender['Female'], gender['Diverse'], gender['I\'d rather not say']]
plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()

# Experience distribution pie chart
labels = ['Yes', 'No']
sizes = [experience[1], experience[0]]
plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()

# Print the statistics
print(agestats)
print('North America:', len(north_america))
print('South America:', len(south_america))
print('Europe:', len(europe))
print('Asia:', len(asia))
print('Africa:', len(africa))
print('Other:', len(other))
print(agestats)
print('Young adults:', len(age_17_30))
print('Middle age adults:', len(age_31_45))
print('Old age adults:', len(age_46_60))
print('Elderly:', len(age_61_75))

#Print counts for every country
for key, value in birthcountry.items():
    print(f'{key}: {value}')






