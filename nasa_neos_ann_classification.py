# -*- coding: utf-8 -*-
"""NASA_NEOs_ANN_Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PvqOfmnM4X7vF228KfGMZVXbMS0HebQm

**<h1 align=center><font size = 5>Predictive Modeling of Near-Earth Objects using Artificial Neural Networks</font></h1>**

<br>

<img src="https://www.techexplorist.com/wp-content/uploads/2021/12/NASAs-Eyes-on-Asteroids.jpg" alt="Techexplorist">

<small>Picture Source: <a href="https://www.techexplorist.com/wp-content/uploads/2021/12/NASAs-Eyes-on-Asteroids.jpg">Techexplorist</a>

<br>

<h3><b>Near-Earth Objects - NEOs</b></h3>

<p>Near-Earth Objects (NEOs) are a group of celestial objects, including asteroids and comets, whose orbits bring them into close proximity to Earth. These objects can potentially pose a risk to our planet due to their potential for collision. Understanding and tracking NEOs is an important part of planetary defense and space science.

NASA provides access to data about NEOs through its publicly available API (Application Programming Interface) called the "Near-Earth Object Web Service" (NeoWs). This API allows researchers, developers, and the public to access information about NEOs, including their orbits, physical characteristics, and close approaches to Earth.</p>

<br>

<h3><b>About NEOs</b></h3>

<p>NEOs could potentially hit our planet and, depending on their size, produce considerable damage. While the chance of a large object hitting Earth is very small, it would produce a great deal of destruction. NEOs thus merit active detection and tracking efforts.</p>

The goal of SSA’s NEO Segment (SSA-NEO) is to:

<ul>
    <li>Become aware of the current and future position of NEOs relative to our planet.</li>
    <li>Estimate the likelihood of Earth impacts.</li>
    <li>Assess the consequences of any possible impact.</li>
    <li>Develop NEO deflection methods.</li>
</ul>

<p>The NEO Segment observes NEOs, predicts their orbits, produces impact warnings when necessary and is involved in potential mitigation measures.</p>

<br>

<h3><b>Context</b></h3>

<p>There is an infinite number of objects in the outer space. Some of them are
closer than we think. Even though we might think that a distance of 70,000 Km
can not potentially harm us, but at an astronomical scale, this is a very small
distance and can disrupt many natural phenomena. These objects/asteroids can
thus prove to be harmful. Hence, it is wise to know what is surrounding us and
what can harm us amongst those. Thus, this dataset compiles the list of <b>NASA</b>
certified asteroids that are classified as the nearest earth object.<p>

<br>

<b>License</b>
    
CC0: Public Domain

<br>

<h3><b>Sources</b></h3>
<p>Sources related to Near-Earth Objects (NEOs):</p>
<ul>
  <li><a href="https://api.nasa.gov/">NASA Open API</a></li>
  <li><a href="https://cneos.jpl.nasa.gov/ca/">NEO Earth Close Approaches</a></li>
  <li><a href="https://www.jpl.nasa.gov/news/twenty-years-of-tracking-near-earth-objects">NASA/JPL-Caltech</a></li>
  <li><a href="https://www.esa.int/Safety_Security/Near-Earth_Objects_-_NEO_Segment#:~:text=Near%2DEarth%20objects%20(NEOs),than%2020%20000%20are%20NEOs.">ESA Near-Earth Objects - NEO Segment</a></li>
</ul>

# **Objective for this Notebook**

Within the scope of this project, a classification model was builded whether NEOs are dangerous or not, through data obtained from NASA.

<div class="alert alert-block alert-info" style="margin-top: 20px">
<li><a href="https://#library">Importing Libraries</a></li>
<li><a href="https://#data_preprocessing">Data Preprocessing</a></li>
<li><a href="https://#ann">Building Artificial Neural Network Model for Classification</a></li>

<br>
<p></p>
Estimated Time Needed: <strong>10 min</strong>
</div>

<a id="library"></a>

<h2 align=center><b>Importing Libraries</b></h2>
"""

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patheffects as path_effects
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
import time
from sklearn.utils import resample
import warnings
warnings.filterwarnings('ignore')

keras.__version__

pd.__version__

sns.__version__

"""<a id="data_preprocessing"></a>

<h2 align=center><b>Data Preprocessing</b></h2>

<p>Data preprocessing can refer to manipulation or dropping of data before it is used in order to ensure or enhance performance, and is an important step in the data mining process. The phrase "garbage in, garbage out" is particularly applicable to data mining and machine learning projects.</p>

### 2.1. Uploading data
"""

df = pd.read_csv('neo.csv')
HAZARDOUS=df['hazardous']

df.head(10)

HAZARDOUS

"""### 2.2. Removing unnecessary columns

<p>As we can see, there is only 1 unique value in <code>orbiting_body</code> and <code>sentry_object</code>. Because of that, we are dropping there columns. In addition, we don't need to use id and name parameters.</p>
"""

df['orbiting_body'].value_counts()

df['sentry_object'].value_counts()

df.drop(['orbiting_body', 'sentry_object', 'id', 'name'], axis = 1, inplace = True)

"""### 2.3. Looking for anomalies and duplicated datas

<p>Dependent and independent variables, in other words, the data in the columns are checked for unspecified values.</p>
"""

df.isnull().sum()

"""Let's get first and last 10 rows."""

df.head(10)

df.tail(10)

"""Now, let's get description of the data in the DataFrame."""

df.describe().T

"""Check number of duplicated rows with <code>duplicated().sum()</code>."""

df.duplicated().sum()

"""Drop duplicated rows."""

dp = df[df.duplicated(keep=False)]
dp.head(2)
df.drop_duplicates(inplace= True)

"""Done!"""

df.duplicated().sum()

"""Let's print a concise summary of our DataFrame."""

df.info()

"""We can see number of unique values and it self in our independent variables with <code>.value_counts()</code>"""

HAZARDOUS.value_counts()

"""Find the unique elements of an array with <code>.unique()</code>"""

HAZARDOUS.unique()

"""### 2.4. Plotting

<p>Plots were created in order to gain a different perspective on values and provide visuality.<p>
"""

explode = (0, 0.1)
fig = plt.figure(figsize = (7, 7), facecolor='w')
out_df=pd.DataFrame(df.groupby('hazardous')['hazardous'].count())

patches, texts, autotexts = plt.pie(out_df['hazardous'], autopct='%1.1f%%',
                                    textprops={'color': "w"},
                                    explode=explode,
                                    startangle=90, shadow=True)

for patch in patches:
    patch.set_path_effects({path_effects.Stroke(linewidth=2.5,
                                                foreground='w')})

plt.legend(labels=['False','True'], bbox_to_anchor=(1., .95))
plt.title('Dependent Variables Distribution')
# plt.savefig('gender_pie')
plt.show()

"""As we can see from the pie chart, our dependent variables are imbalanced. Dealing with imbalanced datasets is a common challenge in machine learning. When your dependent variable classes are imbalanced, it can lead to biased models that perform poorly on the minority class. We are going to deal with it before training our Deep Neural Network (DNN) model."""

rows_to_plot = df.columns[:5]

plt.figure(figsize=(15, 20))
for i, label in enumerate(rows_to_plot, 1):
    plt.subplot(len(rows_to_plot), 1, i)
    plt.hist(df[df['hazardous'] == 1][label], color='blue', label="True", alpha=0.7, density=True, bins=15)
    plt.hist(df[df['hazardous'] == 0][label], color='red', label="False", alpha=0.7, density=True, bins=15)
    plt.title(label)
    plt.ylabel("Probability")
    plt.xlabel(label)
    plt.legend()

plt.tight_layout()
plt.show()

"""Creating correlation heatmap."""

plt.figure(figsize = (15, 6))
plt.title('Correlation Heatmap')
sns.heatmap(df.corr(), annot = True)

"""### 2.5. Label encoding

<p> Building Label Encoding to handle categorical variables (for hazardous/label column).</p>
"""

from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
label_encoder.fit(df['hazardous'])
df['label'] = label_encoder.transform(df['hazardous'])
df['label'].unique()

"""Let's see what we have done;"""

df.head()

"""We categorized the unique values in the hazardous column and transferred them to a different column named label.

### 2.6. Dealing with imbalanced dataset

There are several strategies you can use to address this issue before training your Deep Neural Network (DNN) model:

**Resampling**:

 - *Oversampling*: Increase the number of instances in the minority class by duplicating samples or generating synthetic data points.
 - *Undersampling*: Decrease the number of instances in the majority class by randomly removing some samples.

**Weighted Loss Function**:

Assign higher weights to the minority class during model training. This makes the model pay more attention to the minority class.

The resample function is then applied to the `minority_class`. This function duplicates samples from the minority class with replacement `(replace=True)` until it matches the number of samples in the majority class `(n_samples=len(majority_class))`. This effectively increases the representation of the minority class in the dataset.
"""

minority_class = df[df['label'] == 1]
majority_class = df[df['label'] == 0]
minority_upsampled = resample(minority_class, replace=True, n_samples=len(majority_class), random_state=42)

"""The upsampled minority class, stored in minority_upsampled, is concatenated with the original majority class `(majority_class)` using pd.concat. This creates a new DataFrame called `balanced_df`, where both classes are balanced."""

balanced_df = pd.concat([majority_class, minority_upsampled])

"""Shuffle the dataset."""

balanced_df = balanced_df.sample(frac=1, random_state=42)
balanced_df.head()

balanced_df.shape

"""After these steps, `balanced_df` contains a balanced dataset with an equal number of samples for each class. This balanced dataset can be used for training machine learning models, such as your DNN, to mitigate the issues caused by class imbalance and potentially improve the model's performance on the minority class.

### 2.6. Determination of dependent and independent variables

<p>To build model and make prediction, we need to seperate our data as dependent and independent variables.
"""

X = balanced_df.drop(["label", "hazardous"], axis = 1)
y = balanced_df["label"]

"""<b>Independent variables</b>"""

X

"""<b>Dependent variables</b>"""

y

"""### 2.7. Splitting test and train

<p>The train-test split is a technique for evaluating the performance of a machine learning algorithm. Seperated %66.6 for train and %33.3 for test set.</p>
"""

from sklearn.model_selection import train_test_split

x_train, x_temp, y_train, y_temp = train_test_split(X, y, test_size=0.33, random_state=0)
x_test, x_val, y_test, y_val = train_test_split(x_temp, y_temp, test_size=0.175, random_state=0)

print(x_train.shape, y_train.shape)

print(x_val.shape, y_val.shape)

print(x_test.shape, y_test.shape)

"""### 2.8. Scaling datas

<p>This means that you're transforming your data so that it fits within a specific scale like 0-1.</p>
"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)
X_val = sc.transform(x_val)

"""<a id="ann"></a>

<h2 align=center><b>Building Artificial Neural Network Model for Classification</b></h2>

<p>Artificial neural networks, usually simply called neural networks or, more simply yet, neural nets, are computing systems. Artificial Neural Networks (ANNs) are computational models inspired by the structure and function of the human brain. They are a subset of machine learning and deep learning techniques. For more, please check <a href="https://en.wikipedia.org/wiki/Artificial_neural_network">Wikipedia</a>.</p>

We can directly import our model with keras function <code>load_model</code>.

### 3.1 Loading created model
"""

# from keras.models import load_model
# model = load_model('model.h5')

"""### 3.2 Checking the architecture of the model"""

# model.summary()

"""### 3.3. Define neural network parameters

<p>We have 5 dependent variables and we want 12 epochs in our model.</p>
"""

INPUT = X.shape[1]
epoch = 16 # @param {type:"integer"}
batch_size = 32 # @param {type:"integer"}

"""### 3.4. Building Deep Neural Network (DNN).

- **ANN (Artificial Neural Network)**: This is a broad term referring to any neural network model, including shallow networks (those with a single hidden layer) and deep networks (those with multiple hidden layers).

- **DNN (Deep Neural Network)**: This is a specific type of ANN characterized by having multiple hidden layers, making it deep. The model I provided in the code is an example of a DNN because it has multiple hidden layers (more than one hidden layer).
"""

model = Sequential()

model.add(Dense(64, activation="relu", input_dim=INPUT))

model.add(Dense(32, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(16, activation="relu"))

model.add(Dense(1, activation="sigmoid"))

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

model.summary()

"""### 3.5. Training

<p>Let's fit and train our model.</p>
"""

start = time.time()

model_history = model.fit(X_train, y_train, epochs=epoch, batch_size=batch_size, validation_data=(X_val, y_val))

end = time.time()
cal_time = end - start
print("\nTraining model for NASA - Nearest Earth Objects data set took {} seconds.".format(cal_time))

"""### 3.6. Show summary and save model

<p>Let's save our model for further predictions and see summary of our model.</p>
"""

model.save('model_dnn.h5') # @markdown Run for saving weights.
print("Model saved as 'model_dnn.h5'.")

"""### 3.7. Plot loss and accuracy"""

print(model_history.history.keys())

def plot_accuracy_loss(training_results):
  plt.figure(figsize = (15, 6))
  plt.subplot(2, 1, 1)
  plt.plot(training_results.history['loss'], 'r')
  plt.ylabel('Loss')
  plt.title('Training loss iterations')
  plt.subplot(2, 1, 2)
  plt.plot(training_results.history['accuracy'])
  plt.ylabel('Accuracy')
  plt.xlabel('Epochs')
  plt.show()

plot_accuracy_loss(model_history)

"""### 3.8. System success

A confusion matrix is a table used in machine learning and classification tasks to evaluate the performance of a predictive model. It provides a detailed breakdown of the model's predictions compared to the actual outcomes, allowing you to assess the model's accuracy, precision, recall, and other important metrics. A confusion matrix is especially useful in binary classification problems (where there are only two classes), but it can also be extended to multi-class problems.
"""

y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)  #  Comparing results
print("\nConfusion Matrix:\n", cm)

from sklearn.metrics import accuracy_score
print(f"\nAccuracy score: {accuracy_score(y_test, y_pred)}")

"""**Precision**: The ratio of true positives to the total number of positive predictions TP / (TP + FP). It measures how many of the predicted positive cases were actually positive.
    
**Recall (Sensitivity or True Positive Rate)**: The ratio of true positives to the total number of actual positive cases TP / (TP + FN). It measures the model's ability to correctly identify all positive cases.
    
**Specificity (True Negative Rate)**: The ratio of true negatives to the total number of actual negative cases TN / (TN + FP). It measures the model's ability to correctly identify all negative cases.
    
**F1-Score**: The harmonic mean of precision and recall, which balances the trade-off between precision and recall.
"""

true_positive = cm[1, 1]
false_positive = cm[0, 1]
true_negative = cm[0, 0]
false_negative = cm[1, 0]

precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
specificity = true_negative / (true_negative + false_positive)
f1 = 2 * (precision * recall) / (precision + recall)

print("Precision:", precision)
print("Recall:", recall)
print("Specificity:", specificity)
print("F1 Score:", f1)

"""<a id="conclusion"></a>

<h2 align=center><b>Conclusion</b></h2>

The binary classification model trained to predict whether Near-Earth Objects (NEOs) are hazardous or not has yielded promising results. The evaluation metrics reveal the following key insights:

-   **Accuracy**: The model achieved an accuracy score of approximately 87.92%, indicating that it correctly classified a significant portion of NEOs.
    
-   **Precision**: With a precision score of approximately 81.16%, the model demonstrates its ability to identify hazardous NEOs with a relatively low rate of false positives. This is essential for ensuring that resources are appropriately allocated to address potential threats.
    
-   **Recall**: The recall score, measuring around 98.76%, signifies the model's effectiveness in capturing a vast majority of actual hazardous NEOs. It minimizes the risk of failing to detect dangerous objects.
    
-   **Specificity**: The specificity score of approximately 77.09% reflects the model's capability to correctly identify non-hazardous NEOs. This is crucial for preventing unnecessary alarm or resource allocation for harmless objects.
    
-   **F1 Score**: The F1 score, which combines precision and recall, stands at approximately 89.10%. This balanced metric highlights the model's ability to strike a compromise between minimizing false alarms and ensuring high detection rates.

<br>

In summary, the classification model, leveraging Artificial Neural Networks (ANNs), demonstrates a solid performance in identifying hazardous Near-Earth Objects. Its accuracy, precision, and recall indicate its potential utility in early detection and tracking efforts, contributing to the ongoing mission of safeguarding our planet from potential impacts.
"""

from datetime import datetime
print(f"Changes have been made to the project on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")