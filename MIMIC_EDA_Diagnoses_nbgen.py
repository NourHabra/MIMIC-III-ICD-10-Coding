import nbformat as nbf

notebook = nbf.v4.new_notebook()
cells = []

# Cell 1: Title and intro
cells.append(nbf.v4.new_markdown_cell(
    """# MIMIC-III EDA: Diagnoses and ICD Codes

This notebook explores the diagnoses and ICD code tables in the MIMIC-III dataset, and demonstrates how to join them with patient and ICU stay information.
"""
))

# Cell 2: Imports and setup
cells.append(nbf.v4.new_code_cell(
    """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set display options
pd.set_option('display.max_columns', 100)
sns.set(style='whitegrid')
"""
))

# Cell 3: Load Data
cells.append(nbf.v4.new_markdown_cell("## 1. Load Data"))
cells.append(nbf.v4.new_code_cell(
    """# File paths
DATA_DIR = './mimic-iii-clinical-database-1.4/'
patients = pd.read_csv(DATA_DIR + 'PATIENTS.csv')
admissions = pd.read_csv(DATA_DIR + 'ADMISSIONS.csv')
icustays = pd.read_csv(DATA_DIR + 'ICUSTAYS.csv')
diagnoses_icd = pd.read_csv(DATA_DIR + 'DIAGNOSES_ICD.csv')
d_icd_diagnoses = pd.read_csv(DATA_DIR + 'D_ICD_DIAGNOSES.csv')

print('Loaded tables:')
for name, df in [('patients', patients), ('admissions', admissions), ('icustays', icustays), ('diagnoses_icd', diagnoses_icd), ('d_icd_diagnoses', d_icd_diagnoses)]:
    print(f'{name}: {df.shape}')
"""
))

# Cell 4: Preview Table Structures
cells.append(nbf.v4.new_markdown_cell("## 2. Preview Table Structures"))
cells.append(nbf.v4.new_code_cell(
    """from IPython.display import display

display(patients.head())
display(admissions.head())
display(icustays.head())
display(diagnoses_icd.head())
display(d_icd_diagnoses.head())
"""
))

# Cell 5: Join Tables
cells.append(nbf.v4.new_markdown_cell("## 3. Join Tables: Link Patients, Admissions, ICU Stays, and Diagnoses"))
cells.append(nbf.v4.new_code_cell(
    """# Merge diagnoses with ICD descriptions
diagnoses_full = diagnoses_icd.merge(d_icd_diagnoses, how='left', left_on='ICD9_CODE', right_on='ICD9_CODE')
# Merge with admissions to get patient and admission info
diagnoses_full = diagnoses_full.merge(admissions, how='left', on='HADM_ID')
# Merge with patients to get demographic info
diagnoses_full = diagnoses_full.merge(patients, how='left', on='SUBJECT_ID')
# Merge with icustays to get ICU stay info (optional, not all admissions have ICU stays)
diagnoses_full = diagnoses_full.merge(icustays, how='left', on=['SUBJECT_ID', 'HADM_ID'])

print('Diagnoses full shape:', diagnoses_full.shape)
from IPython.display import display
display(diagnoses_full.head())
"""
))

# Cell 6: EDA - Most Common Diagnoses
cells.append(nbf.v4.new_markdown_cell("## 4. EDA: Diagnoses and ICD Codes"))
cells.append(nbf.v4.new_code_cell(
    """# Most common diagnoses
top_diagnoses = diagnoses_full['LONG_TITLE'].value_counts().head(20)
plt.figure(figsize=(8,8))
sns.barplot(y=top_diagnoses.index, x=top_diagnoses.values, orient='h')
plt.title('Top 20 Most Common Diagnoses')
plt.xlabel('Count')
plt.ylabel('Diagnosis')
plt.tight_layout()
plt.show()
"""
))

# Cell 7: EDA - Diagnoses per Patient
cells.append(nbf.v4.new_code_cell(
    """# Number of unique diagnoses per patient
diagnoses_per_patient = diagnoses_full.groupby('SUBJECT_ID')['ICD9_CODE'].nunique()
plt.figure(figsize=(8,4))
sns.histplot(diagnoses_per_patient, bins=30, kde=True)
plt.title('Distribution of Unique Diagnoses per Patient')
plt.xlabel('Number of Unique Diagnoses')
plt.ylabel('Number of Patients')
plt.show()
"""
))

# Cell 8: EDA - Diagnoses per ICU Stay
cells.append(nbf.v4.new_code_cell(
    """# Number of diagnoses per ICU stay
diagnoses_per_stay = diagnoses_full.groupby('ICUSTAY_ID')['ICD9_CODE'].nunique().dropna()
plt.figure(figsize=(8,4))
sns.histplot(diagnoses_per_stay, bins=30, kde=True)
plt.title('Distribution of Unique Diagnoses per ICU Stay')
plt.xlabel('Number of Unique Diagnoses')
plt.ylabel('Number of ICU Stays')
plt.show()
"""
))

# Cell 9: EDA - Top ICD9 Codes
cells.append(nbf.v4.new_code_cell(
    """# Top ICD9 codes (not just descriptions)
top_icd9 = diagnoses_full['ICD9_CODE'].value_counts().head(20)
plt.figure(figsize=(8,8))
sns.barplot(y=top_icd9.index, x=top_icd9.values, orient='h')
plt.title('Top 20 Most Common ICD9 Codes')
plt.xlabel('Count')
plt.ylabel('ICD9 Code')
plt.tight_layout()
plt.show()
"""
))

# Cell 10: EDA - Admissions per Patient
cells.append(nbf.v4.new_code_cell(
    """# Number of admissions per patient
admissions_per_patient = admissions.groupby('SUBJECT_ID')['HADM_ID'].nunique()
plt.figure(figsize=(8,4))
sns.histplot(admissions_per_patient, bins=30, kde=True)
plt.title('Distribution of Admissions per Patient')
plt.xlabel('Number of Admissions')
plt.ylabel('Number of Patients')
plt.show()
"""
))

# Cell 11: EDA - Most Common Primary Diagnoses
cells.append(nbf.v4.new_code_cell(
    """# Most common primary diagnoses (SEQ_NUM == 1)
primary_diag = diagnoses_full[diagnoses_full['SEQ_NUM'] == 1]
top_primary = primary_diag['LONG_TITLE'].value_counts().head(20)
plt.figure(figsize=(8,8))
sns.barplot(y=top_primary.index, x=top_primary.values, orient='h')
plt.title('Top 20 Most Common Primary Diagnoses')
plt.xlabel('Count')
plt.ylabel('Primary Diagnosis')
plt.tight_layout()
plt.show()
"""
))

# Cell 12: EDA - Distribution of Diagnosis Sequence Numbers
cells.append(nbf.v4.new_code_cell(
    """# Distribution of diagnosis sequence numbers
plt.figure(figsize=(8,4))
sns.histplot(diagnoses_full['SEQ_NUM'], bins=30, kde=True)
plt.title('Distribution of Diagnosis Sequence Numbers (SEQ_NUM)')
plt.xlabel('Diagnosis Sequence Number')
plt.ylabel('Count')
plt.show()
"""
))

# Cell 13: EDA - Age Distribution for Top Diagnoses
cells.append(nbf.v4.new_code_cell(
    """# Age distribution for top 5 diagnoses
from datetime import datetime

def calculate_age(row):
    try:
        dob = pd.to_datetime(row['DOB'])
        adm = pd.to_datetime(row['ADMITTIME'])
        age = (adm - dob).days / 365.25
        return age
    except:
        return None

diagnoses_full['AGE'] = diagnoses_full.apply(calculate_age, axis=1)
top5_diag = top_diagnoses.index[:5]
plt.figure(figsize=(10,6))
for diag in top5_diag:
    sns.kdeplot(diagnoses_full[diagnoses_full['LONG_TITLE'] == diag]['AGE'].dropna(), label=diag)
plt.title('Age Distribution for Top 5 Diagnoses')
plt.xlabel('Age at Admission')
plt.ylabel('Density')
plt.legend()
plt.show()
"""
))

# Cell 14: EDA - Gender Distribution for Top Diagnoses
cells.append(nbf.v4.new_code_cell(
    """# Gender distribution for top 5 diagnoses
gender_counts = diagnoses_full[diagnoses_full['LONG_TITLE'].isin(top5_diag)].groupby(['LONG_TITLE', 'GENDER']).size().unstack().fillna(0)
gender_counts.plot(kind='bar', stacked=True, figsize=(10,6))
plt.title('Gender Distribution for Top 5 Diagnoses')
plt.xlabel('Diagnosis')
plt.ylabel('Count')
plt.legend(title='Gender')
plt.tight_layout()
plt.show()
"""
))

# Cell 15: EDA - Temporal Trends in Diagnoses
cells.append(nbf.v4.new_code_cell(
    """# Diagnoses per year
diagnoses_full['ADMIT_YEAR'] = pd.to_datetime(diagnoses_full['ADMITTIME']).dt.year
trend = diagnoses_full.groupby('ADMIT_YEAR')['ICD9_CODE'].count()
plt.figure(figsize=(10,4))
trend.plot(marker='o')
plt.title('Number of Diagnoses per Year')
plt.xlabel('Year')
plt.ylabel('Number of Diagnoses')
plt.tight_layout()
plt.show()
"""
))

# Cell 16: EDA - Most Common Comorbidity Pairs
cells.append(nbf.v4.new_code_cell(
    """# Most common pairs of diagnoses (comorbidities)
from itertools import combinations
from collections import Counter

# For speed, use a sample if the dataset is very large
sample = diagnoses_full[['HADM_ID', 'ICD9_CODE']].drop_duplicates()
grouped = sample.groupby('HADM_ID')['ICD9_CODE'].apply(list)
pairs = Counter()
for codes in grouped:
    for pair in combinations(sorted(set(codes)), 2):
        pairs[pair] += 1
common_pairs = pairs.most_common(10)
print('Top 10 most common comorbidity pairs (ICD9 codes):')
for (code1, code2), count in common_pairs:
    print(f'{code1} & {code2}: {count}')
"""
))

# Cell 17: Further Exploration
cells.append(nbf.v4.new_markdown_cell(
    """## 5. Further Exploration\nYou can extend this notebook to explore comorbidities, trends over time, or link to other tables (e.g., procedures, outcomes)."""
))

notebook['cells'] = cells
notebook['metadata'] = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "name": "python",
        "version": "3.8"
    }
}

with open('MIMIC_EDA_Diagnoses.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(notebook, f)
print('Notebook MIMIC_EDA_Diagnoses.ipynb created!') 