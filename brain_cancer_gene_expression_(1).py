#imported libraries for performing various data processing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import glob
import gc
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
#mounted the google drive for reading the data file
from google.colab import drive
drive.mount('/content/drive')
#reading the csv file
dataset = pd.read_csv("/content/brain_cancer_gene.csv")

all_columns_except_type = dataset.columns[(dataset.columns != 'type') & (dataset.columns != dataset.columns[0])]

random_columns = np.random.choice(all_columns_except_type, size=998, replace=False)

first_column = [dataset.columns[0]]

selected_columns = np.concatenate((first_column, random_columns, ['type']))

dataset = dataset[selected_columns]

# Check the first few rows
print(dataset.head())

# Summary of columns and missing values
print(dataset.info())

# Statistical summary of numerical features
print(dataset.describe())

"""# EDA

Class Distribution (Target Variable):
Visualize the distribution of the target variable ('type' column in this case).
"""

# Distribution of the target variable
sns.countplot(x='type', data=dataset)
plt.title('Distribution of Types')
plt.show()

"""Feature Distributions:
Visualize distributions of individual features.
"""

# Plotting distributions of individual features
all_columns_except_type = dataset.columns[(dataset.columns != 'type') & (dataset.columns != dataset.columns[0])]

random_columns = np.random.choice(all_columns_except_type, size=10, replace=False)
first_column = [dataset.columns[0]]

selected_columns = np.concatenate((first_column, random_columns, ['type']))

display = dataset[selected_columns]
for column in display.columns:
    if column not in ['samples', 'type']:
        plt.figure()
        sns.histplot(data=dataset, x=column)
        plt.title(f'Distribution of {column}')
        plt.show()

sum(dataset.isna().sum().values)

"""#### Hence there is no Null value in the Dataset"""

classes = dataset.type.unique().tolist()
x_data = dataset.drop(['samples', 'type'], axis = 1).values
y_data = dataset.type.values
func = lambda x : classes.index(x)
y_data = np.asarray([func(i) for i in y_data], dtype = "float32")

print(f"X_data Shape : {x_data.shape}")
print(f"Y_data Shape : {y_data.shape}")

x_data[:5]

pca_scaler = Pipeline([
    ('Scaler', MinMaxScaler()),
    #('PCA', PCA(n_components = 0.9))
])

x_data = pca_scaler.fit_transform(x_data)

x_data.shape

x_data[:5]

"""#### After performing PCA and Scaling"""

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, random_state = 42, shuffle = True, stratify = y_data)

x_train[:5]

# Initializing classifiers
classifiers = {
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'SVM': SVC(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42)
}

# Training and evaluating each classifier
results = {}
for name, clf in classifiers.items():
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    # Generating metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)

    results[name] = {
        'Accuracy': accuracy,
        'Classification Report': report,
        'Confusion Matrix': confusion
    }

    # Visualizing confusion matrix
    plt.figure(figsize=(6, 4))
    sns.heatmap(confusion, annot=True, cmap='Blues', fmt='g')
    plt.title(f'Confusion Matrix - {name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# Printing results
for name, metrics in results.items():
    print(f"===== {name} =====")
    print(f"Accuracy: {metrics['Accuracy']}")
    print("Classification Report:")
    print(metrics['Classification Report'])
    print("Confusion Matrix:")
    print(metrics['Confusion Matrix'])
    print("=" * 30)

# Applying majority vote
from collections import Counter

all_predictions = {}
for name, clf in classifiers.items():
    all_predictions[name] = clf.predict(x_test)

majority_predictions = []
for i in range(len(x_test)):
    votes = [all_predictions[name][i] for name in classifiers]
    majority = Counter(votes).most_common(1)[0][0]
    majority_predictions.append(majority)

# Calculating majority vote accuracy
majority_vote_accuracy = accuracy_score(y_test, majority_predictions)
print(f"Majority Vote Accuracy: {majority_vote_accuracy}")

