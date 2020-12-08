import pandas as pd
from typing import List


def build_design_matrix(
    df: pd.DataFrame,
    date_col: str,
    var_col: str,
    horizon: int,
    start_date: str,
    end_date: str,
):
    """
    Shift the var_col to create AR(1) feature and forecast target.

    If the feature cols are at time t, the lag should be at time t-1, and the target at time t+horizon.

    Args:
        df: A DataFrame which contains a date, feature(s) and a variable column.
        date_col: A string for the date column name
        var_col: A string for the variable name we wish to forecast
        horizon: An integer to specify the forecast horizon (to create the target column)
        start_date: A start date to filter on the df
        end_date:

    Returns: A design matrix where each row is a monthly training sample, and each column is a feature/target.

    Example:
    |        date        | feature | GDP_lag | GDP_forecast |
    |   start_date + 1   |    0.1  |    0.3  |     0.4      |
    |         ...        |    ...  |    ...  |     ...      |
    | end_date - horizon |   -0.2  |    0.2  |     0.5      |

    """
    # use date as an index to filter and sort
    design_df = df.set_index(date_col).loc[start_date:end_date].sort_index()
    # create lag column
    design_df["GDP_lag"] = design_df[var_col].shift(periods=1)
    # create target column
    design_df["GDP_forecast"] = design_df[var_col].shift(periods=-horizon)

    # drop variable column
    design_df = design_df.drop(columns=var_col)
    # drop rows without features
    design_df = design_df.dropna().reset_index()
    return design_df


def cross_validate(
    df: pd.DataFrame,
    date_col: str,
    feature_cols: List[str],
    target_col: str,
    estimator,
    initial: int,
    period: int,
    horizon: int,
    return_model: bool = False,
):
    """
    Cross validate time series by fitting the model on the train set and predicting on a single test sample.

    This cross validation procedure will be done for a range of historical cutoffs by specifying the size of the
    initial training period (initial) and the spacing between cutoff dates (period).

    Args:
        df: A DataFrame which contains a date, feature(s) and a target column.
        date_col: A string for the date column name
        feature_cols: A List of strings for the feature columns names
        target_col: A string for the target column name
        estimator: A duck typed object which implements fit and predict method. If using sklearn estimator, need to
                   instantiate the object before passing it in.
        initial: An integer to specify the size of the initial training period
        period: An integer to specify the spacing between cutoff dates
        horizon: An integer to specify the forecast horizon
        return_model: A flag to determine whether to return the fitted model

    Returns: A DataFrame which contains a date, a prediction and an actual column.

    """
    df = df.sort_values(by=date_col).reset_index(drop=True)
    assert initial < len(
        df
    ), "Initial training period is not strictly smaller than sample size"
    # set the first train_end date
    train_end = initial
    result_list = []
    while train_end + horizon + 1 <= len(df):
        # df is 0-indexed so subtract 1 from train_end
        train_df = df.loc[0 : train_end - 1]
        model = estimator.fit(train_df[feature_cols], train_df[target_col])
        # set a single test sample
        test_df = df.loc[[train_end + horizon]]
        pred = model.predict(test_df[feature_cols])
        # store result in a dict
        result = {
            "date": test_df[date_col].iloc[0],
            "pred": pred[0],
            "actual": test_df[target_col].iloc[0],
        }
        if return_model:
            result["model"] = model
        result_list.append(result)
        train_end += period
    result_df = pd.DataFrame(result_list)
    return result_df


def evaluate_features(
    df,
    date_col: str,
    var_col: str,
    horizon: int,
    estimator,
    initial: int,
    period: int,
    start_date: str = "2015-03-01",
    end_date: str = "2020-03-01",
):
    """
    A wrapper around build design matrix and cross validate.

    Steps:
    1. Create AR(1) feature and forecast target
    2. Train and evaluate the model

    Args:
        df: A DataFrame which contains a date, feature(s) and a variable column.
        date_col: A string for the date column name
        var_col: A string for the variable name we wish to forecast
        horizon:
        estimator:
        initial:
        period:
        start_date:
        end_date:

    Returns: A design matrix and a result DataFrame

    """
    design_df = build_design_matrix(
        df,
        date_col=date_col,
        var_col=var_col,
        horizon=horizon,
        start_date=start_date,
        end_date=end_date,
    )

    feature_cols = [
        col for col in design_df.columns if col not in (date_col, "GDP_forecast")
    ]

    result_df = cross_validate(
        design_df,
        date_col=date_col,
        feature_cols=feature_cols,
        target_col="GDP_forecast",
        estimator=estimator,
        initial=initial,
        period=period,
        horizon=horizon,
    )

    return design_df, result_df
