"""Causal features; the target and its history are never predictors."""
FEATURES = ["flow_index", "temperature_index", "salinity_index", "lab_age_hours",
            "flow_previous_6h", "salinity_flow_interaction"]

def engineer(frame):
    frame = frame.sort_values("timestamp").copy()
    frame["flow_previous_6h"] = frame.flow_index.shift(1).rolling(6, min_periods=1).mean()
    frame["salinity_flow_interaction"] = frame.salinity_index * frame.flow_index
    return frame
