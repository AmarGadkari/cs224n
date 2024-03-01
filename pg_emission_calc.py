# -*- coding: utf-8 -*-
"""pg_emission_calc.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1del_mAOVctyV6WxCz4e4RZx1wkY6iOiw
"""

!pip install pandas==1.5.3
!pip install sentence-transformers accelerate -U
!pip install transformers[torch] -U

import accelerate
import transformers
print("Accelerate version:", accelerate.__version__)
print("Transformers version:", transformers.__version__)

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authenticate and create the PyDrive client
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

import pandas as pd

epa_data = drive.CreateFile({'id': '1nOdK7YrAzx-2ZpKZCd620rbSG9qLLxZp'})
epa_data.GetContentFile('EPA_EmissionsData.csv')
factor_df = pd.read_csv('EPA_EmissionsData.csv')
print(factor_df.head())

activity_data = drive.CreateFile({'id': '1smUkjfTvvHmx2QiCfDImKOOtdCSb4dTk'})
activity_data.GetContentFile('business_activities_training_data.csv')
activity_df = pd.read_csv('business_activities_training_data.csv')
print(activity_df.head())

# Load the test data
activity_test_data = drive.CreateFile({'id': '1Q6Sm-lxT-cpOJpFeLg_Leyj3w28Ff9GY'})
activity_test_data.GetContentFile('business_activities_test_data.csv')
test_df = pd.read_csv('business_activities_test_data.csv')
print(test_df.head())

print(f"\n\nFactor Count: {factor_df.count()}")
print(f"\n\nActivity Count: {activity_df.count()}")

# import torch

# device = torch.device('cpu')

label_dict = {value: idx for idx, value in enumerate(activity_df['2017 NAICS Title'].unique())}
activity_df['label'] = activity_df['2017 NAICS Title'].map(label_dict)

import pandas as pd
import numpy as np
import random

# Helper functions
def introduce_minor_errors(text):
    """Introduce minor spelling mistakes in the text."""
    errors_introduced = 0
    max_errors = random.randint(2, 3)  # Decide to introduce 2 or 3 minor errors

    while errors_introduced < max_errors and len(text) > 4:  # Ensure text is long enough to alter
        error_type = random.choice(['substitute', 'omit', 'swap'])
        error_index = random.randint(1, len(text) - 2)  # Avoid beginning and end of the text for simplicity

        if error_type == 'substitute':
            # Substitute a character with a nearby character (mimicking common typing errors)
            substitutions = {'a': 's', 's': 'a', 'd': 'f', 'i': 'o', 'o': 'p', 'e': 'r', 'r': 't'}
            if text[error_index] in substitutions:
                text = text[:error_index] + substitutions[text[error_index]] + text[error_index + 1:]
                errors_introduced += 1

        elif error_type == 'omit':
            # Omit a character
            text = text[:error_index] + text[error_index + 1:]
            errors_introduced += 1

        elif error_type == 'swap':
            # Swap two adjacent characters
            if error_index < len(text) - 1:  # Ensure there's a character to swap with
                text = text[:error_index] + text[error_index + 1] + text[error_index] + text[error_index + 2:]
                errors_introduced += 1
    return text

def introduce_major_errors(text):
    """Replace or scramble parts of the text to introduce major errors."""
    # Randomly choose between scrambling or inserting irrelevant text
    if random.random() < 0.5:
        return ''.join(random.sample(text, len(text)))
    else:
        return "Irrelevant text " + ''.join(random.sample(text, len(text)))
    return text

# Function to randomly apply either minor or major errors to a text
def apply_random_error(text):
    if random.random() < 0.40:  # 15% chance to introduce an error
        #error_type = random.choice(['minor', 'major'])
        #if error_type == 'minor':
        #    return introduce_minor_errors(text)
        #else:
            return introduce_major_errors(text)   # only major errors
    return text


def apply_errors_with_limit(row, fields, max_errors=2):
    """
    Randomly apply errors to a limited number of fields in a row.

    Parameters:
    - row: The DataFrame row to apply errors to.
    - fields: A list of field names to potentially apply errors to.
    - max_errors: Maximum number of fields to apply errors to.
    """
    # Randomly decide how many fields to apply errors to (0 to max_errors)
    errors_to_apply = random.randint(0, max_errors)

    # Randomly select the fields where errors will be applied
    fields_with_errors = random.sample(fields, errors_to_apply)

    # Apply errors to the selected fields
    for field in fields:
        if field in fields_with_errors:
            row[field + ' Error'] = apply_random_error(row[field])
        else:
            row[field + ' Error'] = row[field]

    return row

import numpy as np
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Define the fields to potentially introduce errors
fields = ['Business Activity Description', 'Vendor', 'Comment']

# Apply errors to 2 or fewer fields for each row
activity_df = activity_df.apply(lambda row: apply_errors_with_limit(row, fields), axis=1)

# Combine the possibly altered text fields into a new 'combined_text' column
activity_df['combined_text'] = activity_df['Business Activity Description Error'] + " " + activity_df['Vendor Error'] + " " + activity_df['Comment Error']
# Now, 'combined_text' contains the concatenated texts with either minor or major errors introduced


# Split data into features and labels
# activity_df['combined_text'] = activity_df['Business Activity Description'] + " " + activity_df['Vendor'] + " " + activity_df['Comment']
X = activity_df['combined_text']  # Feature
y = activity_df['label']  # Assuming 'label' is already encoded as numeric labels

# Splitting dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the TF-IDF vectorizer on training data
tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust max_features as needed
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

# Initialize and fit the RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)  # You can adjust parameters as needed
clf.fit(X_train_tfidf, y_train)

# Transform the test data using the same TF-IDF vectorizer
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Make predictions on the test data
y_pred = clf.predict(X_test_tfidf)

# Evaluate the model
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# You can now use clf to make predictions on new data using the same tfidf_vectorizer to transform the new data

import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer  # Assuming you've already fitted this with your training data

# Assuming clf is your trained RandomForestClassifier and tfidf_vectorizer is your fitted TF-IDF vectorizer

test_df['encoded_labels'] = test_df['2017 NAICS Title'].apply(lambda x: label_dict.get(x, -1))  # Unseen labels get -1

# Apply errors to 2 or fewer fields for each row
test_df = test_df.apply(lambda row: apply_errors_with_limit(row, fields), axis=1)
# Combine the possibly altered text fields into a new 'combined_text' column
test_df['combined_text'] = test_df['Business Activity Description Error'] + " " + test_df['Vendor Error'] + " " + test_df['Comment Error']

# Prepare the test data features and labels
# test_df['combined_text'] = test_df['Business Activity Description'] + " " + test_df['Vendor'] + " " + test_df['Comment']

X_test_new = test_df['combined_text']  # Feature
y_test_new = test_df['encoded_labels']  # Replace 'label' with the actual column name for labels in your test data

# Transform the test data using the already fitted TF-IDF vectorizer
X_test_new_tfidf = tfidf_vectorizer.transform(X_test_new)

# Make predictions on the new test data
y_pred_new = clf.predict(X_test_new_tfidf)

# Evaluate the model on the new test data
print("New Test Data - Classification Report:\n", classification_report(y_test_new, y_pred_new))
print("New Test Data - Accuracy:", accuracy_score(y_test_new, y_pred_new))

# Convert y_pred_new and y_test_new to a DataFrame for easier manipulation
results_df = pd.DataFrame({'combined_text': X_test_new, 'Actual Label': y_test_new, 'Predicted Label': y_pred_new})

# Filter the DataFrame to only include rows where the prediction failed
failed_predictions = results_df[results_df['Actual Label'] != results_df['Predicted Label']]

# Display the details of rows with failed predictions
print("Rows with Failed Predictions:")
pd.set_option('display.max_colwidth', None)  # For pandas versions < 1.0, use -1 instead of None
print(failed_predictions[['combined_text']])
pd.reset_option('display.max_colwidth')

# Ensure that '2017 NAICS Title' in both dataframes are of the same format for accurate mapping
# Map 'Supply Chain Emission Factors without Margins' from factor_df to test_df based on '2017 NAICS Title'
test_df['Emission Factor'] = test_df['2017 NAICS Title'].map(
    factor_df.set_index('2017 NAICS Title')['Supply Chain Emission Factors without Margins']
)

# Calculate the emissions for each row before grouping
test_df['Calculated_Emissions'] = test_df['Emission Factor'] * test_df['Cost_USD']

# Selecting unique '2017 NAICS Title' and their corresponding 'Emission Factor' to avoid duplicates
unique_emission_factors = test_df[['2017 NAICS Title', 'Emission Factor']].drop_duplicates()

# Step 1: Match NAICS Titles in test_df with those in factor_df
# This step is simplified due to direct matching by '2017 NAICS Title'.
# In real-world scenarios, consider complexities of matching titles.

# Group 'test_df' by '2017 NAICS Title' and sum the 'Calculated_Emissions' for each group, also count the occurrences
aggregated_emissions = test_df.groupby('2017 NAICS Title').agg(
    Total_Emissions=('Calculated_Emissions', 'sum'),
    Count=('Calculated_Emissions', 'count')
).reset_index()

# Print the total emissions and count for each title
for index, row in aggregated_emissions.iterrows():
    print(f"Title: {row['2017 NAICS Title']}, Total Emissions: {row['Total_Emissions']:.2f}, Count: {row['Count']}")


# Calculate and print overall totals using DataFrame functions
total_count = aggregated_emissions['Count'].sum()
total_emissions = aggregated_emissions['Total_Emissions'].sum()

print(f"\nTotal Count of All Rows: {total_count}")
print(f"Total of Total Emissions: {total_emissions:.2f}")