import pandas as pd
import kagglehub
import xgboost as xgb
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

path = kagglehub.dataset_download("adityakadiwal/water-potability")
filename = "water_potability.csv"
csv_path = os.path.join(path, filename)
data = pd.read_csv(csv_path)

data = data.fillna(data.mean())

Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1
data = data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]

# data['ph_hardness'] = data['ph'] * data['Hardness']

X = data.drop(columns=['Potability'])
y = data['Potability']

smote = SMOTE(random_state=42)
X, y = smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [4, 6, 8],
    'subsample': [0.7, 0.8, 0.9],
    'colsample_bytree': [0.7, 0.8, 0.9]
}

xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='logloss')

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=cv, n_jobs=-1, verbose=1)
grid_search.fit(X_train_scaled, y_train)

print("\n--- Grid Search Results ---")
print(f"Best parameters found: {grid_search.best_params_}")
print(f"Best cross-validation accuracy: {grid_search.best_score_:.4f}")

best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test_scaled)

print("\n--- Final Model Performance on Test Set ---")
print(f"Accuracy on test data: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\n--- Feature Importance ---")
xgb.plot_importance(best_model)
plt.show()

rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_scaled, y_train)
rf_pred = rf_model.predict(X_test_scaled)
print("\n--- Random Forest Performance ---")
print(f"Accuracy: {accuracy_score(y_test, rf_pred):.4f}")
print(classification_report(y_test, rf_pred))

import pickle
filename = 'savedmodel.sav'
pickle.dump(rf_model, open(filename, 'wb'))