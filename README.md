🧪 A/B Experimentation Platform

Industry-Grade | Reproducible | Statistically Correct








🚀 Overview

This repository contains a production-style A/B experimentation platform built to reflect how real analytics and data science teams operate in industry.

Unlike toy A/B test scripts, this system emphasizes:

Correct statistical assumptions

Clean, modular architecture

Config-driven experiments

Automated, executive-ready reporting

Reproducibility and auditability

Key principle:
If a statistical method is not valid for the data, it is explicitly disabled.

🏗️ System Architecture
High-Level Architecture
flowchart TD
    A[experiment.yaml] --> B[Pipeline Orchestrator]
    B --> C[Data Loader & Validator]
    C --> D[Frequentist Tests]
    D --> E[Effect Size & Power]
    E --> F[JSON Results]

    B -->|if valid| G[Bayesian A/B Testing]
    G --> F

    F --> H[PDF Report Generator]
    H --> I[Executive Report]

Folder Structure
ab-experimentation-platform/
│
├── data/
│   ├── raw/                # Immutable input data
│   ├── interim/            # CUPED-ready layer
│   └── processed/          # Aggregated outputs
│
├── experiments/
│   ├── config/             # YAML-driven experiments
│   └── results/            # JSON outputs
│
├── src/
│   ├── core/               # Data loading & validation
│   ├── statistics/         # All statistical logic
│   ├── reporting/          # PDF generation
│   └── pipeline/           # Orchestration only
│
├── reports/                # Final PDF reports
├── templates/              # Report templates
├── tests/                  # Extensible testing layer
│
└── README.md

Design Rationale

statistics/ contains zero I/O → pure, testable math

pipeline/ contains zero math → orchestration only

config/ drives behavior → no hard-coded experiments

This separation mirrors production experimentation platforms.

▶️ Running an Experiment
python -m src.pipeline.run_experiment


This single command:

Loads experiment.yaml

Validates input data

Runs frequentist tests

Computes effect size & power

(Conditionally) runs Bayesian inference

Writes JSON outputs

Generates a PDF report

📊 Statistical Methodology
Frequentist Testing (Primary)

For each continuous metric:

Normality: Shapiro–Wilk test

Variance: Levene’s test

Test selection:

Welch’s t-test (default)

Mann–Whitney U when assumptions fail

Effect size: Cohen’s d

Power analysis:

Achieved power

Required sample size (target = 0.80)

flowchart LR
    A[Metric Data] --> B{Normal?}
    B -->|Yes| C[T-Test]
    B -->|No| D[Mann–Whitney U]
    C --> E[Effect Size]
    D --> E
    E --> F[Power Analysis]

🧠 Why Bayesian A/B Testing Was Disabled

Bayesian A/B testing was implemented but intentionally disabled for this dataset.

Reason (Statistical Integrity)

The data is aggregated daily metrics, not trial-level data.

Bayesian Binomial models require:

n = number of trials (users / impressions)

k = number of successes

This dataset contains:

Daily aggregates

Purchase totals exceeding daily rows

Running a Binomial Bayesian model here would be mathematically invalid.

flowchart TD
    A[Daily Aggregates] -->|Invalid| B[Binomial Bayesian Model]
    B --> C[Incorrect Inference ❌]

    A -->|Correct| D[Frequentist Tests]
    D --> E[Valid Decisions ✅]


Industry rule followed:
Do not force a model when assumptions are violated.

Bayesian testing can be re-enabled instantly when user-level or impression-level data is available.

📄 Outputs
JSON (Machine-Readable)
experiments/results/frequentist_results.json


Includes:

Metric

Test used

p-value

Effect size

Achieved power

Required sample size

Significance flag

Ideal for dashboards, APIs, or automation.

PDF (Executive-Ready)
reports/ab_test_report.pdf


Contains:

Experiment overview

Metric-level statistical results

Practical interpretation

Final recommendation

Designed for non-technical stakeholders.

💼 Business Interpretation Framework

This platform answers three business questions:

Is the result real? → Statistical significance

Is it meaningful? → Effect size

Can we trust it? → Power analysis

A result is not shipped unless all three are satisfied.

This prevents:

False positives

Premature launches

Costly misinterpretations

🧩 Example Decision Logic
flowchart TD
    A[p < 0.05] --> B{Effect Size Meaningful?}
    B -->|No| C[Do Not Roll Out]
    B -->|Yes| D{Power >= 0.80?}
    D -->|No| E[Collect More Data]
    D -->|Yes| F[Approve Rollout]

🔮 Future Extensions

CUPED variance reduction

Sequential testing / early stopping

Dashboard integration (Tableau / Power BI)

User-level Bayesian modeling

Experiment versioning & logging

🏁 Why This Project Stands Out

✔ Not a notebook
✔ Not a toy script
✔ Statistically correct
✔ Config-driven
✔ Production-style architecture

This project demonstrates how to run experiments correctly, not just how to compute p-values.

### Reporting Templates

The `templates/` directory is reserved for HTML-based report templates.

During development, the system initially supported HTML → PDF rendering
(Jinja2 + WeasyPrint). Due to OS-level native dependencies on Windows,
the final implementation uses ReportLab for reliable, pure-Python PDF
generation.

The folder is intentionally retained to support future HTML-based
reporting without changing the project structure.

📌 Author Note

This system was built with real-world constraints in mind:
dependency issues, invalid assumptions, debugging, and trade-offs.

