# Assignment 8: Breast Cancer Prediction with Polygenic Risk Scores (PRS)
## Overview
This assignment involves developing a machine learning model to predict breast cancer risk using Polygenic Risk Scores (PRS). The goal is to achieve the highest possible Area Under the Curve (AUC) score by accurately predicting breast cancer risk.

## Kaggle Competition
This assignment is based on the Kaggle Competition: Breast Cancer Prediction with PRS hosted by the University of California, Santa Cruz (UCSC). You can participate in the competition and submit your model for evaluation by following this link: https://www.kaggle.com/competitions/breast-cancer-prediction-with-prs-ucsc

## Breast Cancer Background
Breast cancer is one of the most common cancers worldwide, with a significant impact on women. Early prediction of breast cancer risk can improve outcomes through preventive measures and early interventions. Various factors contribute to breast cancer risk, including age, family history, lifestyle factors, genetic predisposition, and environmental influences. This assignment emphasizes the genetic component of risk prediction using PRS, which aggregates the effects of many genetic variants (SNPs) across the genome.

## Polygenic Risk Scores (PRS)
Polygenic Risk Scores estimate an individual's genetic predisposition to a particular disease by combining the effects of many genetic variants.

PRS are used to predict an individual’s risk of developing diseases, such as breast cancer, by considering multiple genetic factors. These scores are based on data derived from genome-wide association studies (GWAS) and provide a quantitative measure of an individual’s genetic risk.


## Standardization:
PRS values are standardized to ensure comparability across populations. This transformation results in Z-scores, where a higher score indicates a higher genetic risk for the disease.

## Converting PRS to Absolute Risk:
To convert PRS to clinically meaningful predictions, it is mapped to the absolute risk of developing the disease using a logistic model. This helps calibrate the model to account for population-specific differences.

## Risk Interpretation:
The Z-scores (standardized PRS) follow a normal distribution. Scores are interpreted as follows:

Z = 0: Average risk
Z = ±1: Moderate risk
Z = ±2: High risk
Higher positive scores indicate an increased genetic risk, while lower scores suggest reduced risk.

## Evaluation Metric: AUC-ROC
The Area Under the Receiver Operating Characteristic Curve (AUC-ROC) is used to evaluate model performance. AUC-ROC measures the ability of the model to discriminate between individuals with and without breast cancer across all possible thresholds.

## AUC Interpretation:
AUC represents the probability that a randomly chosen positive case (someone with breast cancer) has a higher predicted risk than a randomly chosen negative case.

## Implementation:
The AUC can be calculated using the roc_auc_score function from scikit-learn to evaluate how well the model distinguishes between positive and negative cases based on the predicted probabilities.