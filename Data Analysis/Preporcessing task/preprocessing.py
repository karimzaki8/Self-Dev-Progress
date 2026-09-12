"""
preprocessing.py
-----------------
Core preprocessing functions for the pipeline:

    1. Read_data_file        -> load a CSV safely
    2. Drop_unnecessary_features -> remove columns given by the caller
    3. Check_data_type       -> produce a small data-quality report

None of these functions know anything specific about the Titanic dataset.
Every dataset-specific detail (which file to read, which columns to drop)
is passed in from the outside (main.py / config/config.py).
"""

import os
import pandas as pd


def Read_data_file(file_path):
    """
    Read a CSV file and return it as a pandas DataFrame.

    Instead of letting the program crash with a long, confusing pandas
    traceback when something goes wrong, we catch the common problems
    ourselves and print a short, useful message. On failure we return
    None so the caller can decide what to do next (e.g. stop the
    pipeline) instead of continuing with a broken DataFrame.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame or None
        The loaded data, or None if the file could not be read.
    """
    # Problem 1: the path is not even a usable string
    if not file_path or not isinstance(file_path, str):
        print("Error: please provide a valid file path (non-empty string).")
        return None

    # Problem 2: the file simply does not exist at that location
    if not os.path.exists(file_path):
        print(f"Error: the file '{file_path}' does not exist. "
              f"Please check the path and try again.")
        return None

    # Problem 3: the path exists but points to a folder, not a file
    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' is not a file (looks like a folder).")
        return None

    # Problem 4: the file exists but pandas still can't read it
    # (empty file, corrupted content, wrong encoding, etc.)
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print(f"Error: the file '{file_path}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: the file '{file_path}' could not be parsed as a CSV. "
              f"It may be corrupted or in the wrong format.")
        return None
    except UnicodeDecodeError:
        print(f"Error: the file '{file_path}' has an unsupported encoding.")
        return None
    except Exception as e:
        # Catch-all so the pipeline never crashes with a raw traceback
        print(f"Error: could not read '{file_path}' ({e}).")
        return None

    print(f"Successfully loaded '{file_path}' -> {df.shape[0]} rows, "
          f"{df.shape[1]} columns.")
    return df


def Drop_unnecessary_features(df, cols_to_drop):
    """
    Remove the columns listed in cols_to_drop from df.

    This function is completely generic: it has no knowledge of what
    dataset it is working on. The list of columns to remove always
    comes from the caller (in practice, from config/config.py), so the
    configuration can change without ever touching this function.

    Parameters
    ----------
    df : pandas.DataFrame
    cols_to_drop : list of str
        Column names to remove. Columns that don't exist in df are
        simply ignored (with a warning) instead of raising an error.

    Returns
    -------
    pandas.DataFrame
        A new DataFrame without the dropped columns.
    """
    if df is None:
        print("Error: no DataFrame was provided.")
        return None

    if not cols_to_drop:
        print("No columns specified to drop - returning the DataFrame unchanged.")
        return df

    # Only drop columns that actually exist, and warn about the rest
    existing = [c for c in cols_to_drop if c in df.columns]
    missing = [c for c in cols_to_drop if c not in df.columns]

    if missing:
        print(f"Warning: these columns were not found and will be skipped: {missing}")

    new_df = df.drop(columns=existing)
    print(f"Dropped columns: {existing}. Remaining columns: {list(new_df.columns)}")
    return new_df


def Check_data_type(df):
    """
    Produce a small, easy-to-read data-quality report.

    For every column, show:
        - Column name
        - Datatype
        - Number of unique values

    The result is returned as a TRANSPOSED DataFrame so that each
    original column becomes a row in the report - much easier to scan
    than the default df.dtypes output.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame or None
        A report DataFrame indexed by column name, with
        'Datatype' and 'Unique Values' columns.
    """
    if df is None:
        print("Error: no DataFrame was provided.")
        return None

    report = pd.DataFrame({
        "Datatype": df.dtypes.astype(str),
        "Unique Values": df.nunique(),
    })

    # Transpose so it reads as one row of info per column, laid out
    # horizontally - quick to scan for "what is Age?", "how many
    # unique values does Embarked have?", etc.
    report_t = report.T

    print("Data-quality report (columns x [Datatype, Unique Values]):")
    print(report_t)
    return report_t
