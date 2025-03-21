# lrg_omics.proteomics.analysis.maxquant

import pandas as pd
import numpy as np

from os.path import isfile


def get_maxquant_txt(path, txt="proteinGroups.txt", raw_file=None):
    """
    Graps a MaxQuant txt based on the name of the
    .RAW file and the name of the pipeline. raw_file
    and pipename are added to all rows. Pipename is
    removed from all column names.
    """
    full_path = f"{path}/{txt}"
    if isfile(full_path):
        df = pd.read_table(full_path)
    else:
        print(f"File not found: {full_path}")
        return pd.DataFrame()
    if "RawFile" not in df.columns and raw_file is not None:
        df["RawFile"] = raw_file
        df = df.set_index("RawFile").reset_index()
    return df


def melt_protein_quant(df, id_vars=None, var_name="TMT"):
    if id_vars is None:
        id_vars = df.filter(regex="^(?!.*Reporter.*)").columns
    output = df.melt(id_vars=id_vars, var_name=var_name, value_name="ReporterIntensity")
    output["TMT"] = (
        output["TMT"].str.replace("Reporter intensity corrected ", "").astype(int)
    )
    return output


def log2p1(x):
    return np.log2(x + 1)


def get_protein_quant(
    path,
    melt=False,
    normed=None,
    take_log=False,
    divide_by_column_mean=False,
    mean_centering_per_plex=False,
    drop_zero_q=False,
    data_cols=["RawFile"],
    protein_col="Majority protein IDs",
    pipename=None,
    mq_run_name=None,
):
    """
    Gets the proteinGroups file based on the .RAW name
    and the pipename. Records starting with REV or CON
    are removed. The "Reporter intensity corrected"
    columns are extracted.
    -----
    Args:
        - divide_by_column_mean: bool
            * divide intensities by column-wise mean
        - take_log: apply log2p1 transformation, devide_by_mean
            is applied before log-transformation if set to True.
        - normed:
            * None: Don't apply further normalization
            * diff_to_ref: Substract intensities of reference
            column (super-mix in channel 1).
            * fold_change: Divide by reference intensities.
        - drop_zero_q
        - melt: Return a melted DataFrame
    """
    df = get_maxquant_txt(path, txt="proteinGroups.txt")

    if len(df) == 0:
        return None
    df = df[
        ~(
            df["Protein IDs"].str.startswith("REV_")
            | df["Protein IDs"].str.startswith("CON_")
        )
    ]
    if drop_zero_q:
        df = df[df["Q-value"] != 0]
    # Data columns
    data = df[data_cols + [protein_col]].copy()
    # Formating protein to shorter names.
    # Take second element by '|', if possible else
    # the first element and allow 30 letters at max.
    # data[protein_col] = data[protein_col].apply(lambda x: x.split('|')[:2][-1][:30])
    # Just the reporter intensities
    reporter_intensity = df.iloc[:, list(range(22, 33))]
    # Replace 0 with NaN
    reporter_intensity = reporter_intensity.replace(0, np.NaN)
    assert normed in [
        None,
        "fold_change",
        "diff_to_ref",
    ], "Normed should be from [None, 'fold_change', 'diff_to_ref']"
    if divide_by_column_mean is True:
        # Devide by the mean column-wise
        reporter_intensity = reporter_intensity / reporter_intensity.mean()
    if take_log is True:
        # Apply log(x+1) transformation
        reporter_intensity = reporter_intensity.apply(log2p1)
    if normed == "diff_to_ref":
        # Substract reference strain (TMT-channel 1) intensity
        reporter_intensity = reporter_intensity.add(
            -reporter_intensity["Reporter intensity corrected 1"], axis=0
        )
        del reporter_intensity["Reporter intensity corrected 1"]
    if normed == "fold_change":
        reporter_intensity = reporter_intensity.divide(
            reporter_intensity["Reporter intensity corrected 1"], axis=0
        )
        del reporter_intensity["Reporter intensity corrected 1"]
    if mean_centering_per_plex:
        cols = reporter_intensity.filter(regex="Reporter intensity corrected").columns
        a = reporter_intensity.loc[:, cols].copy()
        row_means = a.mean(axis=1)
        a = a.subtract(row_means, axis=0)
        reporter_intensity.loc[:, cols] = a
    # Combine data with reporter int
    output = pd.concat([data, reporter_intensity], axis=1)
    if melt:
        output = melt_protein_quant(output)
    return output


def protein_quant_from_paths(
    paths, pipename, protein_col="Protein IDs", mq_run_names=None
):
    # Combine data with reporter int

    if mq_run_names is None:
        mq_run_names = paths

    dfs = []
    for path, name in zip(paths, mq_run_names):
        print(path, name)
        df = get_protein_quant(
            path,
            pipename=pipename,
            mq_run_name=name,
            normed="diff_to_ref",
            take_log=True,
            divide_by_column_mean=True,
            mean_centering_per_plex=True,
            drop_zero_q=False,
        )
        dfs.append(df)

    protein_quant = pd.concat(dfs)
    protein_quant = melt_protein_quant(protein_quant)
    protein_quant = protein_quant.pivot_table(
        values="ReporterIntensity", columns=["MaxQuantRun", "TMT"], index=protein_col
    )
    protein_quant = protein_quant.T.reset_index()
    protein_quant["TMT"] = protein_quant["TMT"].apply(lambda x: f"{x:02.0f}")
    protein_quant = protein_quant.reset_index(drop=True).set_index(
        ["MaxQuantRun", "TMT"]
    )
    return protein_quant


def extract_protein_quant(
    df,
    melt=False,
    normed=None,
    take_log=False,
    divide_by_column_mean=False,
    mean_centering_per_plex=False,
    drop_zero_q=False,
    protein_col="Majority protein IDs",
):
    """
    Gets the proteinGroups file based on the .RAW name
    and the pipename. Records starting with REV or CON
    are removed. The "Reporter intensity corrected"
    columns are extracted.
    -----
    Args:
        - divide_by_column_mean: bool
            * divide intensities by column-wise mean
        - take_log: apply log1p transformation, devide_by_mean
            is applied before log-transformation if set to True.
        - normed:
            * None: Don't apply further normalization
            * diff_to_ref: Substract intensities of reference
            column (super-mix in channel 1).
            * fold_change: Divide by reference intensities.
        - drop_zero_q
        - melt: Return a melted DataFrame
    """
    if len(df) == 0:
        return None
    df = df[
        ~(
            df["Protein IDs"].str.startswith("REV_")
            | df["Protein IDs"].str.startswith("CON_")
        )
    ]

    if drop_zero_q:
        df = df[df["Q-value"] != 0]

    # Data columns
    data = df[protein_col].copy()
    # Formating protein to shorter names.
    # Take second element by '|', if possible else
    # the first element and allow 30 letters at max.
    # data[protein_col] = data[protein_col].apply(lambda x: x.split('|')[:2][-1][:30])
    # Just the reporter intensities
    reporter_intensity = df.iloc[:, list(range(22, 33))]
    # Replace 0 with NaN
    reporter_intensity = reporter_intensity.replace(0, np.NaN)
    assert normed in [None, "fold_change", "diff_to_ref"]
    if divide_by_column_mean is True:
        # Devide by the mean column-wise
        reporter_intensity = reporter_intensity / reporter_intensity.mean()
    if take_log is True:
        # Apply log(x+1) transformation
        reporter_intensity = reporter_intensity.apply(np.log1p)
    if normed == "diff_to_ref":
        # Substract reference strain (TMT-channel 1) intensity
        reporter_intensity = reporter_intensity.add(
            -reporter_intensity["Reporter intensity corrected 1"], axis=0
        )
        del reporter_intensity["Reporter intensity corrected 1"]
    if normed == "fold_change":
        reporter_intensity = reporter_intensity.divide(
            reporter_intensity["Reporter intensity corrected 1"], axis=0
        )
        del reporter_intensity["Reporter intensity corrected 1"]
    if mean_centering_per_plex:
        cols = reporter_intensity.filter(regex="Reporter intensity corrected").columns
        a = reporter_intensity.loc[:, cols].copy()
        row_means = a.mean(axis=1)
        a = a.subtract(row_means, axis=0)
        reporter_intensity.loc[:, cols] = a
    # Combine data with reporter int
    output = pd.concat([data, reporter_intensity], axis=1)
    if melt:
        output = melt_protein_quant(output)
    return output
