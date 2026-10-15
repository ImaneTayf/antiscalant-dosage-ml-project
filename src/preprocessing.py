"""Quality rules and causal alignment for the synthetic schema only."""
import numpy as np
import pandas as pd

def prepare(process, lab):
    process, lab = process.copy(), lab.copy()
    before = len(process)
    process["timestamp"] = pd.to_datetime(process.timestamp, utc=True)
    lab["available_at"] = pd.to_datetime(lab.available_at, utc=True)
    process = process.drop_duplicates("timestamp").sort_values("timestamp")
    lab = lab.drop_duplicates("available_at").sort_values("available_at")
    invalid = 0
    for frame, columns in [(process, ["flow_index", "temperature_index", "dose_index"]),
                           (lab, ["salinity_index"])]:
        for col in columns:
            bad = (~np.isfinite(frame[col]) | (frame[col] <= 0)) & frame[col].notna()
            invalid += int(bad.sum())
            frame.loc[bad, col] = np.nan
    aligned = pd.merge_asof(process, lab, left_on="timestamp", right_on="available_at",
                            direction="backward", tolerance=pd.Timedelta("18h"))
    audit = {"duplicates_removed": before-len(process), "invalid_values_masked": invalid,
             "missing_lab_values": int(aligned.salinity_index.isna().sum())}
    aligned["lab_age_hours"] = (aligned.timestamp-aligned.available_at).dt.total_seconds()/3600
    aligned = aligned.dropna(subset=["dose_index"])
    return aligned.reset_index(drop=True), audit
