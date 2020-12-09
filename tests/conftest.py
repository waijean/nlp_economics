import pandas as pd
import numpy as np
from datetime import datetime
import pytest


@pytest.fixture(scope="module")
def test_input_df():
    input_df = pd.DataFrame(
        data={
            "date": pd.date_range(
                start=datetime(2019, 12, 1), end=datetime(2020, 11, 1), freq="MS"
            ),
            "feature": [np.nan] + list(range(1, 20, 2)) + [np.nan],
            "GDP": range(0, 12),
        }
    )
    return input_df


@pytest.fixture()
def test_design_df():
    return pd.DataFrame(
        data={
            "date": pd.date_range(
                start=datetime(2020, 1, 1), end=datetime(2020, 10, 1), freq="MS"
            ),
            "feature": range(1, 20, 2),
            "GDP_lag": range(0, 10),
            "GDP_forecast": range(2, 12),
        }
    ).astype({"feature": float, "GDP_lag": float, "GDP_forecast": float})


@pytest.fixture()
def test_result_df():
    return pd.DataFrame(
        data={
            "date": pd.date_range(
                start=datetime(2020, 5, 1), end=datetime(2020, 10, 1), freq="MS"
            ),
            "pred": [6.0, 7.0, 8.0, 9.0, 10.0, 11.0],
            "actual": [6, 7, 8, 9, 10, 11],
        }
    ).astype({"actual": float})
