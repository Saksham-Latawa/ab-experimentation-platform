import numpy as np
from scipy.stats import (
    ttest_ind,
    mannwhitneyu,
    shapiro,
    levene
)

# -----------------------------
# Assumption Checks
# -----------------------------

def check_normality(series, alpha=0.05):
    stat, p = shapiro(series)
    return p > alpha


def check_equal_variance(control, test, alpha=0.05):
    stat, p = levene(control, test)
    return p > alpha


# -----------------------------
# Effect Size
# -----------------------------

def cohens_d(control, test):
    mean_diff = test.mean() - control.mean()
    pooled_std = np.sqrt(
        (control.var(ddof=1) + test.var(ddof=1)) / 2
    )
    return mean_diff / pooled_std


# -----------------------------
# Hypothesis Test
# -----------------------------

def hypothesis_test(control, test, metric, alpha=0.05):

    normal = (
        check_normality(control) and
        check_normality(test)
    )

    equal_var = check_equal_variance(control, test)

    if normal:
        stat, p_value = ttest_ind(
            control,
            test,
            equal_var=equal_var
        )
        test_used = "Welch T-Test" if not equal_var else "Student T-Test"
    else:
        stat, p_value = mannwhitneyu(
            control,
            test,
            alternative="two-sided"
        )
        test_used = "Mann-Whitney U"

    effect = cohens_d(control, test)

    return {
    "metric": str(metric),
    "test_used": str(test_used),
    "p_value": float(round(p_value, 6)),
    "effect_size": float(round(effect, 4)),
    "significant": bool(p_value < alpha)
}

