from statsmodels.stats.power import TTestIndPower


def required_sample_size(effect_size, alpha=0.05, power=0.80):
    analysis = TTestIndPower()
    return int(
        analysis.solve_power(
            effect_size=abs(effect_size),
            alpha=alpha,
            power=power
        )
    )


def achieved_power(effect_size, n_obs, alpha=0.05):
    analysis = TTestIndPower()
    power_value = analysis.power(
        effect_size=abs(effect_size),
        nobs1=n_obs,
        alpha=alpha
    )
    return float(round(power_value, 4))
