# CVSS Severity Predictor

#### Author:

- Angelina Shibu 2001CS06
- Sanskriti Singh 2001CS60

## Load and run (Quickest)

- run the below code to load pretrained model and predict on the default testing data

```bash
python predictScoreCVSSV3.py -p 'testData' -s True -v True
```

## Train and run

Follow the steps to download the dataset and train the model, then predict

- Step 1: Download datasets from NVD feeds.

```bash
python updateDB.py
```

- Step 2: Train machine-learning models for different CVSS V3 mechanisms and store them.

```bash
python trainScoreCVSSV3.py
```

- Step 3: Using the trained machine-learning models to predict CVSS V3 scores for any vulnerability document.

```bash
python predictScoreCVSSV3.py -p 'testData' -s True -v True
```

## Severity Prediction Under CVSS V3

The purpose here is to be able to automatically assign a severity score to any vulnerability instance with a descriptive report, using the CVSS Version 3 standard. Two examples are shown below, whereby the TestingSamples have labels initially set as (CVSS score = 0) and other values as "l", and the labels of the PredictedSamples are predicted by the trained machine-learning models.

### Model

- Machine-learning model: [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) algorithm is utilised to show the applicability of the proposed approach. Any other machine-learning model can be applied to further improve the model performances.

### Dataset

- Training/Testing dataset: [NVD](https://nvd.nist.gov/vuln/full-listing) data feeds (2002-2020).
- Validating dataset: [NVD](https://nvd.nist.gov/vuln/full-listing) data feeds (2021).

## Sample Output

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>CVE_ID</th>
      <th>CVSS V3 Score</th>
      <th>Attack Vector</th>
      <th>Attack Complexity</th>
      <th>Privileges Required</th>
      <th>User Interaction</th>
      <th>Scope</th>
      <th>Confidentiality Impact</th>
      <th>Integrity Impact</th>
      <th>Availability Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CVE-2008-0176</td>
      <td>9.8</td>
      <td>Network</td>
      <td>Low</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Unchanged</td>
      <td>High</td>
      <td>High</td>
      <td>High</td>
    </tr>
    <tr>
      <td>CVE-2010-4597</td>
      <td>8.8</td>
      <td>Network</td>
      <td>Low</td>
      <td>NaN</td>
      <td>Required</td>
      <td>Unchanged</td>
      <td>High</td>
      <td>High</td>
      <td>High</td>
    </tr>
    <tr>
      <td>CVE-2011-1562</td>
      <td>9.8</td>
      <td>Network</td>
      <td>Low</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Unchanged</td>
      <td>High</td>
      <td>High</td>
      <td>High</td>
    </tr>
    <tr>
      <td>CVE-2011-1563</td>
      <td>9.8</td>
      <td>Network</td>
      <td>Low</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Unchanged</td>
      <td>High</td>
      <td>High</td>
      <td>High</td>
    </tr>
  </tbody>
</table>

- Refer [`testDataResult/test_predicted.csv`](testDataResult/test_predicted.csv) for the predictions generated.
