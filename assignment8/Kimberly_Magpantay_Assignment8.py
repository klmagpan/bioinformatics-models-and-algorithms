# Import necessary libraries
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# Load the training and test data
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

# Preprocessing - One-Hot Encoding for Categorical Variables
train_data = pd.get_dummies(train_data, drop_first=True)
test_data = pd.get_dummies(test_data, drop_first=True)

# Align train and test data to ensure they have the same columns
X = train_data.drop(columns=["breast_cancer", "id"])
y = train_data["breast_cancer"]
X_test = test_data.drop(columns=["id"])  # Drop id in test for consistency
X, X_test = X.align(X_test, join='left', axis=1, fill_value=0)  # Align columns and fill missing with 0

# Split training data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Alternative Model - XGBoost
xgb_model = XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42)
xgb_model.fit(X_train, y_train)
y_pred_prob_xgb = xgb_model.predict_proba(X_val)[:, 1]
xgb_auc = roc_auc_score(y_val, y_pred_prob_xgb)
print("XGBoost AUC:", xgb_auc)

# Predict on test data
test_pred_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]

# Create submission file
submission = pd.DataFrame({
    "id": test_data["id"],
    "breast_cancer": test_pred_prob_xgb
})
submission.to_csv("submission.csv", index=False)
print("Submission file created: submission.csv")

# # Alternative Model - Random Forest
# rf_model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=10)
# rf_model.fit(X_train, y_train)
# y_pred_prob_rf = rf_model.predict_proba(X_val)[:, 1]
# rf_auc = roc_auc_score(y_val, y_pred_prob_rf)
# print("Random Forest AUC:", rf_auc)

# # Predict on test data for submission
# test_pred_prob_rf = rf_model.predict_proba(X_test)[:, 1]  # Probability of the positive class

# # Create submission file
# submission = pd.DataFrame({
#     "id": test_data["id"],
#     "breast_cancer": test_pred_prob_rf
# })
# submission.to_csv("submission.csv", index=False)
# print("Submission file created: submission.csv")



