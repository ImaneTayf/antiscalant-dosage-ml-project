"""Invented dimensionless signals; no industrial inputs or calibration."""
import numpy as np
import pandas as pd

SEED = 42

def generate(n=1440, seed=SEED):
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    times = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    salinity = 1 + .15 * np.sin(t / 90) + rng.normal(0, .025, n)
    flow = 1 + .12 * np.sin(t / 23) + rng.normal(0, .03, n)
    temperature = 1 + .1 * np.cos(t / 120) + rng.normal(0, .02, n)
    # This deliberately learnable equation is fictional, not a dosing law.
    dose = .5 + .6 * salinity + .25 * flow + .15 * temperature + rng.normal(0, .07, n)
    process = pd.DataFrame(dict(timestamp=times, flow_index=flow,
        temperature_index=temperature, dose_index=dose))
    lab = pd.DataFrame(dict(available_at=times[::12], salinity_index=salinity[::12]))
    # Synthetic missing readings, invalid readings and duplicate records.
    process.loc[rng.choice(n, 40, replace=False), "flow_index"] = np.nan
    process.loc[rng.choice(n, 8, replace=False), "temperature_index"] = -1
    process = pd.concat([process, process.iloc[[20, 70]]], ignore_index=True)
    lab.loc[5, "salinity_index"] = np.nan
    return process, lab
