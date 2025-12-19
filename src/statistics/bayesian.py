import pymc as pm
import arviz as az
import numpy as np


def bayesian_ab_test(
    control_conversions,
    control_total,
    test_conversions,
    test_total,
    draws=4000,
    tune=2000
):
    with pm.Model() as model:

        p_control = pm.Beta("p_control", 1, 1)
        p_test = pm.Beta("p_test", 1, 1)

        pm.Binomial(
            "control_obs",
            n=control_total,
            p=p_control,
            observed=control_conversions
        )

        pm.Binomial(
            "test_obs",
            n=test_total,
            p=p_test,
            observed=test_conversions
        )

        lift = pm.Deterministic("lift", p_test - p_control)

        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=4,
            target_accept=0.95,
            progressbar=False
        )

    lift_samples = trace.posterior["lift"].values.flatten()

    return {
        "expected_lift": float(lift_samples.mean()),
        "prob_test_better": float((lift_samples > 0).mean())
    }
