from datetime import datetime

from pandas._testing import assert_frame_equal

from gdp_forecast.cross_validate import cross_validate, build_design_matrix
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def test_cross_validate():
    input_df = pd.DataFrame(
        data={
            "date": pd.date_range(
                start=datetime(2020, 1, 1), end=datetime(2020, 10, 1), freq="MS"
            ),
            "feature": range(1, 20, 2),
            "feature_lag": range(-1, 9),
            "target": range(1, 11),
        }
    )
    lr = LinearRegression()
    actual = cross_validate(
        input_df,
        lr,
        initial=3,
        period=1,
        horizon=1,
        date_col="date",
        feature_cols=["feature", "feature_lag"],
        target_col="target",
    )
    expected = pd.DataFrame(
        data={
            "date":pd.date_range(
                start=datetime(2020, 5, 1), end=datetime(2020, 10, 1), freq="MS"
            ),
            "pred":[5.0,6.0,7.0,8.0,9.0,10.0],
            "actual":[5,6,7,8,9,10],
        }
    )
    assert_frame_equal(actual, expected)


def test_build_design_matrix():
    input_df = pd.DataFrame(
        data={
            "date": pd.date_range(
                start=datetime(2019, 12, 1), end=datetime(2020, 11, 1), freq="MS"
            ),
            "feature": [np.nan] + list(range(1, 20, 2)) + [np.nan],
            "gdp": range(0, 12),
        }
    )
    actual = build_design_matrix(input_df, date_col="date", var_col="gdp", horizon=1)
    expected = pd.DataFrame(
        data={
            "date": pd.date_range(
                start=datetime(2020, 1, 1), end=datetime(2020, 10, 1), freq="MS"
            ),
            "feature": range(1, 20, 2),
            "target_lag": range(0, 10),
            "target": range(2, 12),
        }
    ).astype({"feature":float, "target_lag":float, "target":float})
    assert_frame_equal(actual, expected)