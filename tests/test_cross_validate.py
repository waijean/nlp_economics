from datetime import datetime

from pandas._testing import assert_frame_equal

from gdp_forecast.cross_validate import (
    cross_validate,
    build_design_matrix,
    evaluate_features,
)
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np


def test_build_design_matrix(test_input_df, test_design_df):
    actual_design_df = build_design_matrix(
        test_input_df,
        date_col="date",
        var_col="gdp",
        horizon=1,
        start_date="2019-12-01",
        end_date="2020-11-01",
    )
    assert_frame_equal(actual_design_df, test_design_df)


def test_cross_validate(test_design_df, test_result_df):
    lr = LinearRegression()
    actual_result = cross_validate(
        test_design_df,
        date_col="date",
        feature_cols=["feature", "GDP_lag"],
        target_col="GDP_forecast",
        estimator=lr,
        window=3,
        period=1,
        horizon=1,
    )
    assert_frame_equal(actual_result, test_result_df)


def test_evaluate_features(test_input_df, test_design_df, test_result_df):
    lr = LinearRegression()
    actual_design, actual_result = evaluate_features(
        test_input_df,
        date_col="date",
        var_col="gdp",
        horizon=1,
        estimator=lr,
        window=3,
        period=1,
        return_model=False,
        start_date="2019-12-01",
        end_date="2020-11-01",
    )
    assert_frame_equal(actual_result, test_result_df)
    assert_frame_equal(actual_design, test_design_df)
