import json
from pathlib import Path

# ============================
# CORE
# ============================
from src.core.config_loader import load_config
from src.core.data_loader import load_and_validate_data

# ============================
# STATISTICS
# ============================
from src.statistics.frequentist import hypothesis_test
from src.statistics.power import achieved_power, required_sample_size
from src.statistics.bayesian import bayesian_ab_test

# ============================
# REPORTING
# ============================
from src.reporting.report_generator import generate_pdf_report


# ============================
# PIPELINE
# ============================
def run_experiment():

    # -------------------------------------------------
    # 1. Load experiment configuration
    # -------------------------------------------------
    config = load_config("experiments/config/experiment.yaml")

    control_path = config["data"]["control_path"]
    test_path = config["data"]["test_path"]

    metrics = config["metrics"]["continuous"]
    binary_metric = config["metrics"]["binary"]["conversion_column"]

    alpha = config["statistics"]["alpha"]
    target_power = config["statistics"]["power_target"]

    bayesian_cfg = config["bayesian"]

    # -------------------------------------------------
    # 2. Load & validate data
    # -------------------------------------------------
    combined_df, control_df, test_df = load_and_validate_data(
        control_path,
        test_path
    )

    frequentist_results = []

    # -------------------------------------------------
    # 3. Frequentist A/B Testing
    # -------------------------------------------------
    for metric in metrics:
        control_series = control_df[metric].dropna()
        test_series = test_df[metric].dropna()

        result = hypothesis_test(
            control_series,
            test_series,
            metric,
            alpha=alpha
        )

        n_obs = min(len(control_series), len(test_series))

        result["achieved_power"] = achieved_power(
            result["effect_size"],
            n_obs,
            alpha=alpha
        )

        result["required_sample_size"] = required_sample_size(
            result["effect_size"],
            alpha=alpha,
            power=target_power
        )

        frequentist_results.append(result)

    # Save frequentist results
    Path("experiments/results").mkdir(parents=True, exist_ok=True)
    with open("experiments/results/frequentist_results.json", "w") as f:
        json.dump(frequentist_results, f, indent=4)

    # -------------------------------------------------
    # 4. Bayesian A/B Testing
    # -------------------------------------------------
    if bayesian_cfg["enabled"]:
        bayesian_results = bayesian_ab_test(
            control_conversions=int(control_df[binary_metric].sum()),
            control_total=len(control_df),
            test_conversions=int(test_df[binary_metric].sum()),
            test_total=len(test_df),
            draws=bayesian_cfg["draws"],
            tune=bayesian_cfg["tune"]
        )

        with open("experiments/results/bayesian_results.json", "w") as f:
            json.dump(bayesian_results, f, indent=4)
    else:
        bayesian_results = {
            "expected_lift": None,
            "prob_test_better": None
        }

    # -------------------------------------------------
    # 5. Generate PDF Report (THE ONLY PLACE IT SHOULD BE)
    # -------------------------------------------------
    context = {
        "experiment_name": config["experiment"]["name"],
        "description": config["experiment"]["description"],
        "frequentist_results": frequentist_results,
        "bayesian_prob": bayesian_results["prob_test_better"],
        "bayesian_lift": bayesian_results["expected_lift"],
        "recommendation": generate_recommendation(
            frequentist_results,
            bayesian_results,
            bayesian_cfg
        )
    }

    generate_pdf_report(context)

    print("Experiment completed successfully")
    print("Results saved in experiments/results/")
    print("PDF report generated in reports/")


# ============================
# DECISION LOGIC
# ============================
def generate_recommendation(freq_results, bayes_results, bayes_cfg):

    significant_metrics = [
        r for r in freq_results if r["significant"]
    ]

    if bayes_cfg["enabled"]:
        prob = bayes_results["prob_test_better"]
        if prob is not None and prob >= bayes_cfg["decision_threshold"]:
            return (
                f"Bayesian probability {prob:.2f} exceeds threshold. "
                "Recommend rollout."
            )

    if significant_metrics:
        return (
            "Frequentist tests show significant improvement. "
            "Recommend cautious rollout."
        )

    return (
        "No strong statistical evidence detected. "
        "Recommend continuing experiment."
    )


# ============================
# ENTRY POINT
# ============================
if __name__ == "__main__":
    run_experiment()
