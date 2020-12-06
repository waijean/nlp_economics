import pandas as pd
from typing import List


def build_design_matrix(df:pd.DataFrame, date_col, var_col:str, horizon:int, start_date:str=None, end_date:str=None):
    """
    Return a design matrix where each row is a monthly training sample, and each column is a feature/target.

    If the feature cols are at time t, the lag should be at time t-1, and the target at time t+horizon.

    Args:
        df: A DataFrame which contains a date, feature(s) and a variable column.
        var_col: A string for the variable name we wish to forecast
        horizon: An integer to specify the forecast horizon (to create the target column)

    Returns:

    """
    design_df = df.sort_values(by=date_col).reset_index(drop=True)
    design_df["target_lag"] = design_df[var_col].shift(periods=1)
    design_df["target"] = design_df[var_col].shift(periods=-horizon)
    # drop rows without features
    design_df = design_df.dropna().reset_index(drop=True)
    if start_date:
        design_df = design_df.set_index("DATE").loc[start_date:end_date].reset_index()
    return design_df.drop(columns=var_col)


def cross_validate(
    df: pd.DataFrame,
    estimator,
    initial: int,
    period: int,
    horizon: int,
    date_col: str,
    feature_cols: List[str],
    target_col: str,
):
    """
    Cross validate time series by fitting the model on the train set and predicting on a single test sample.

    This cross validation procedure will be done for a range of historical cutoffs by specifying the size of the
    initial training period (initial) and the spacing between cutoff dates (period).

    Args:
        df: A DataFrame which contains a date, feature(s) and a target column.
        estimator: A duck typed object which implements fit and predict method. If using sklearn estimator, need to
                   instantiate the object before passing it in.
        initial: An integer to specify the size of the initial training period
        period: An integer to specify the spacing between cutoff dates
        horizon: An integer to specify the forecast horizon

    Returns: A DataFrame which contains a date, a prediction and an actual column.

    """
    df = df.sort_values(by=date_col).reset_index(drop=True)
    assert initial < len(df), "Initial training period needs to be strictly smaller than sample size"
    # set the first train_end date
    train_end = initial
    result = []
    while train_end + horizon + 1 <= len(df):
        # df is 0-indexed so subtract 1 from train_end
        train_df = df.loc[0:train_end-1]
        model = estimator.fit(train_df[feature_cols], train_df[target_col])
        # set a single test sample
        test_df = df.loc[[train_end + horizon]]
        pred = model.predict(test_df[feature_cols])
        result.append({"date":test_df[date_col].iloc[0], "pred":pred[0], "actual":test_df[target_col].iloc[0]})
        train_end += period
    result_df = pd.DataFrame(result)
    return result_df