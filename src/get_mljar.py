import logging

from src.get_statistic_summary import rejected_var, is_a_warning_col
from src.utils import slugify

logger = logging.getLogger()

import numpy as np
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML


# Minimal rules to be followed to get mljar working
# 1. No nan in the target variable
# 2. Drop columns with > 70%? of  missing values because useless
# 3. Drop columns labeled as unsupported by Pandas Profiling and redundant columns
# c. url and long texts are unsupported
# d. drop columns with 100% of distinct values (such as IDs)


def prepare_for_mljar(data, profiling, csv_data=None):
    """
    This function returns a dataset properly prepared to be used by mljar
    :param csv_data:
    :param: id: id of the dgf resource (must be a txt, csv or xls file)
    :type: id: string
    :param: target_variable: name of the target variable of
    the chosen ML task
    :type: target_variable: string
    :param: task: chosen ML task (regression, binary_classification, multi_classification
    :type: task: string
    """
    columns_to_drop = []
    # 1. Check total number of NaN in dataset
    if data.isna().sum().sum() / (len(data) * len(data.columns)) >= 30:
        logger.warning(
            "This dataset contains too many missing values. No ML task will be performed"
        )
        return

    # 2. Remove pandas profiling rejected variables
    columns_to_drop.extend(rejected_var(profiling))

    # 3. Remove pandas profiling warning variables
    columns_to_drop.extend(
        [col for col in data.columns if is_a_warning_col(col, profiling=profiling)]
    )

    # 4. Remove variables with more than 70% of NaNs
    columns_to_drop.extend(
        [col for col in data.columns if data[col].isna().sum() / len(data) > 0.7]
    )

    # 5. Remove redundant variables
    data = data.loc[:, ~data.columns.duplicated()]
    description = profiling.get_description()
    pandas_cat_col = [
        key
        for key, value in description["variables"].items()
        if str(value["type"]) == "Categorical"
    ]
    pandas_cat_col = [col for col in pandas_cat_col if col in data.columns]
    text_cols = [
        (data[col].str.split().str.len().mean(), col)
        for col in pandas_cat_col
        if np.any([isinstance(val, str) for val in data[col]])
    ]
    # 6. Remove long text columns
    columns_to_drop.extend(
        [text_cols[i][1] for i in range(len(text_cols)) if text_cols[i][0] > 15]
    )

    # 7. Remove url columns
    columns_to_drop.extend(
        [col for col in pandas_cat_col if (str(data[col][1]).startswith("https"))]
    )

    # 8. Remove csv-detective detected columns
    if csv_data and "columns" in csv_data:
        columns_to_drop.extend(
            [
                slugify(col_name)
                for col_name, col_type in csv_data["columns"].items()
                if col_type not in ["booleen"]
            ]
        )

    # Actually remove columns
    data = data.drop(columns=set(columns_to_drop))
    return data, columns_to_drop


def generate_mljar(data, target_variable, output_dir, automl_mode):
    """
    This function takes a properly prepared dataframe and performs AutoML on it. The generated output is the html
    report. ------------------------------------------------
    :param: :data: dataframe on which we want to perform a
    given ML task
    :type: :data: pandas dataframe
    :param: :target_variable: chosen target_variable for the ML task
    :type: :target_variable: string
    :param: :output_dir: directory path for the mljar report :type: :output_dir: Path
    :param: :automl_mode: mode for AutoMl computing: choose 'Perform' to have more visualisations and features (but
    slower and not always better performing; choose 'Explain' otherwise
    """
    y = data[target_variable].values
    X = data.drop(columns=[target_variable])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    if automl_mode == "Explain":
        automl = AutoML(
            results_path=output_dir.as_posix(),
            total_time_limit=5 * 60,
            mode="Explain",
        )
        automl.fit(X_train, y_train)
        automl.report()
    else:
        automl = AutoML(
            results_path=output_dir.as_posix(),
            total_time_limit=7 * 60,
            mode="Perform",
        )
        automl.fit(X_train, y_train)
        automl.report()
    return automl
