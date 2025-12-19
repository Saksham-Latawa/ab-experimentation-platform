import numpy as np

def apply_cuped(metric, pre_metric):
    """
    CUPED variance reduction
    """
    theta = np.cov(metric, pre_metric)[0, 1] / np.var(pre_metric)
    adjusted = metric - theta * (pre_metric - pre_metric.mean())
    return adjusted
