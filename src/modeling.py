"""Fixed illustrative settings; all learned preprocessing uses training data."""
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge, HuberRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from .features import FEATURES

def evaluate(frame):
    cut = int(.8 * len(frame))
    train, test = frame.iloc[:cut], frame.iloc[cut:]
    specs = {"Median baseline": DummyRegressor(strategy="median"),
             "Ridge": Ridge(alpha=1.0), "PLS": PLSRegression(n_components=3, scale=False),
             "Huber": HuberRegressor(max_iter=2000),
             "Random Forest": RandomForestRegressor(n_estimators=200, min_samples_leaf=5,
                                                      random_state=42, n_jobs=1)}
    rows, predictions, fitted = [], pd.DataFrame({"timestamp": test.timestamp,
                                                 "actual": test.dose_index}), {}
    for name, estimator in specs.items():
        steps = [SimpleImputer(strategy="median")]
        if name in {"Ridge", "PLS", "Huber"}:
            steps.append(StandardScaler())
        model = make_pipeline(*steps, estimator)
        model.fit(train[FEATURES], train.dose_index)
        pred = np.asarray(model.predict(test[FEATURES])).ravel()
        predictions[name] = pred
        rows.append(dict(model=name, MAE=mean_absolute_error(test.dose_index, pred),
                         RMSE=np.sqrt(mean_squared_error(test.dose_index, pred)),
                         R2=r2_score(test.dose_index, pred)))
        fitted[name] = model
    return pd.DataFrame(rows).set_index("model"), predictions, fitted, cut
