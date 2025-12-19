import pandas as pd


def load_and_validate_data(control_path, test_path):
    """
    Load control and test datasets, validate schema,
    and return combined, control, and test DataFrames.
    """

    control_df = pd.read_csv(control_path)
    test_df = pd.read_csv(test_path)

    # Add group labels
    control_df["group"] = "control"
    test_df["group"] = "test"

    # Basic schema validation
    if set(control_df.columns) != set(test_df.columns):
        raise ValueError(
            "Schema mismatch between control and test datasets"
        )

    combined_df = pd.concat(
        [control_df, test_df],
        ignore_index=True
    )

    return combined_df, control_df, test_df
