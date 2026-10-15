import unittest
import numpy as np
import pandas as pd
from src.synthetic import generate
from src.preprocessing import prepare
from src.features import engineer, FEATURES
from src.modeling import evaluate

class PipelineTests(unittest.TestCase):
    def test_causality_and_expiration(self):
        process, lab = generate()
        lab = lab.iloc[:1]
        aligned, _ = prepare(process, lab)
        self.assertTrue(aligned.loc[aligned.timestamp > lab.available_at.iloc[0], "lab_age_hours"].dropna().le(18).all())
        self.assertTrue(aligned.loc[aligned.timestamp > lab.available_at.iloc[0] + pd.Timedelta('18h'), "salinity_index"].isna().all())
        first = engineer(aligned)
        changed = aligned.copy()
        changed.loc[100:, "flow_index"] = 999
        second = engineer(changed)
        np.testing.assert_allclose(first.flow_previous_6h.iloc[:101], second.flow_previous_6h.iloc[:101], equal_nan=True)

    def test_train_only_preprocessing_and_baseline(self):
        aligned, _ = prepare(*generate(n=240))
        frame = engineer(aligned)
        metrics, predictions, models, cut = evaluate(frame)
        np.testing.assert_allclose(predictions["Median baseline"], frame.dose_index.iloc[:cut].median())
        np.testing.assert_allclose(models['Ridge'].steps[0][1].statistics_, frame[FEATURES].iloc[:cut].median())
        self.assertTrue(np.isfinite(metrics.to_numpy()).all())
        self.assertLess(frame.timestamp.iloc[cut-1], frame.timestamp.iloc[cut])

if __name__ == '__main__':
    unittest.main()
