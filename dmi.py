def dmi(data, rsi_period=14, std_period=10, upper=70, lower=30):
    """Takes in a pandas dataframe of OHLC data and returns the Dynamic Momentum index

    data : pd.Dataframe()
        Dataframe of OHLC data
    rsi_period : int
        Length of the RSI period
    std_period : int
        Length of the standard deviation period
    upper : int
        Upper band of the DMI
    lower : int
        Lower band of the DMI

    Returns:
        pd.DataFrame
        DataFrame with the DMI, upper band, and lower band columns
    """

    # Calculate the standard deviation of the closing prices over the specified period.
    sdev = ta.stdev(close=pd.Series(data["Close"]), length=std_period)

    # Calculate the simple moving average of the standard deviation.
    stda = ta.sma(close=sdev, length=10)

    # Calculate the Directional Movement Index.
    Vi = pd.Series([sdev[i] / stda[i] if (sdev[i] != 0 and stda[i] != 0) else 0 for i, o in enumerate(sdev)])

    # Replace any NaN values in the Directional Movement Index with 0.
    Vi = Vi.replace(np.nan, 0)

    # Calculate the DMI Triggers.
    TD = pd.Series([int(rsi_period/ Vi[i]) if (Vi[i] != 0) else 0 for i, o in enumerate(Vi)])

    # Ensure that the DMI Triggers are between 5 and 30.
    TD = pd.Series([td if (5 <= td <= 30) else 5 if td <= 5 else 30 for i, td in enumerate(TD)])

    # Calculate the DMI.
    dm = pd.Series((ta.rsi(close=pd.Series(data["Close"][i - p - 1:i]), length=p).iloc[-1]) if i>p else 0 for i, p in enumerate(TD))

    # Create a new DataFrame.
    df = pd.DataFrame()

    # Add the DMI to the DataFrame.
    df["DMI"] = dm

    # Add the upper band of the DMI to the DataFrame.
    df["UPPER"] = pd.Series([upper for pos in dm])

    # Add the lower band of the DMI to the DataFrame.
    df["LOWER"] = pd.Series([lower for pos in dm])

    # Return the DataFrame.
    return df
