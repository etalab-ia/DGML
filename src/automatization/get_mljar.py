import re
import unicodedata

import pandas as pd

from get_dataset import *
from get_statistic_summary import *
import numpy as np
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown
import matplotlib.pyplot as plt


# Minimal rules to be followed to get mljar working
# 1. No nan in the target variable
# 2. Drop columns with > 70%? of  missing values because useless
# 3. Drop columns labeled as unsupported by Pandas Profiling and redundant columns
# c. url and long texts are unsupported
# d. drop columns with 100% of distinct values


def prepare_to_mljar(data, target_variable, profiling):
    """This function returns a dataset properly prepared to be used by mljar
    :param:     id: id of the dgf resource (must be a txt, csv or xls file)
    :type:      id: string
    :param:     target_variable: name of the target variable of the chosen ML task
    :type:      target_variable: string
    :param:     task: chosen ML task (regression, binary_classification, multi_classification
    :type:      task: string
    """
    data = data[data[target_variable].isna() == False]  # handle NaN in target variable
    if data.isna().sum().sum() / (len(data) * len(data.columns)) < 30:  # check total number of NaN in dataset
        list_rej = rejected_var(profiling)
        if len(list_rej) != 0:
            data = data.drop(columns=list_rej)  # drop unsupported variables
        data = data.drop(columns=[col for col in data.columns if
                                  data[col].isna().sum() / len(data) > 0.7])  # drop columns with more than 70% of NaN
        data = data.loc[:, ~data.columns.duplicated()]  # drop redundant columns if there are any
        description = profiling.get_description()
        type_target = str(description['variables'][target_variable]['type'])
        pandas_cat_col = [key for key, value in description['variables'].items() if
                          str(value['type']) == 'Categorical']
        pandas_cat_col = [col for col in pandas_cat_col if col in data.columns]
        long_text_cols = [(data[col].str.split().str.len().mean(), col) for col in pandas_cat_col if
                          np.any([isinstance(val, str) for val in data[col]])]
        url_columns = [col for col in pandas_cat_col if (str(data[col][1]).startswith('https'))]  # drop urls
        columns_to_drop = [long_text_cols[i][1] for i in range(len(long_text_cols)) if
                           long_text_cols[i][0] > 15]  # drop columns with long text
        columns_to_drop = columns_to_drop + url_columns
        data = data.drop(columns=columns_to_drop)
        # check if the type of the target variable is right
        # if task == 'regression':
        #     if type_target == 'Categorical':
        #         data[target_variable] = data[target_variable].str.replace(',', '.', regex=True)
        #         try:
        #             data[target_variable] = data[target_variable].astype(float)
        #         except ValueError:
        #             raise TypeError('Please modify the target variable: values must be numeric.')
        #     elif type_target == 'Unsupported':
        #         raise TypeError('Please choose another target variable. This target variable is unsupported.')
        #     else:
        #         print('The type of your target variable is ok.')
        # elif (task == 'binary_classification') or (task == 'multi_classification'):
        #     if type_target == 'Unsupported':
        #         raise TypeError('Please choose another target variable. This target variable is unsupported.')
        #     else:
        #         print(
        #             'The type of your target variable is ok. AutoML will tranform it into a categorical variable if needed.')
        # else:
        #     raise ValueError(
        #         'Please enter one of the following words as task: regression, binary_classification, multi_classification')
    else:
        raise Exception('This dataset contains too many missing values. No ML task will be performed')
    return data


def generate_mljar(data, target_variable, output_dir):
    """This function takes a properly prepared dataframe and performs AutoML on it. The generated output is the html report.
    ------------------------------------------------
    :param:     :data: dataframe on which we want to perform a given ML task
    :type:      :data: pandas dataframe
    :param:     :target_variable: chosen target_variable for the ML task
    :type:      :target_variable: string"""
    y = data[target_variable].values
    X = data.drop(columns=[target_variable])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    results_path = output_dir.joinpath(f"automl_{slugify(target_variable)}")
    automl = AutoML(results_path=results_path.as_posix(), total_time_limit=5 * 60, mode='Explain')
    automl.fit(X_train, y_train)
    predictions = automl.predict(X_test)
    automl.report()
    return automl


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

# def plot_mljar_table(id):
#     """Returns a plot from the mljar leaderboard with train_time of the x-axis and metric_value on the y axis"""
#     leaderboard = pd.read_csv(Path().home().joinpath(f'open_ML/datasets/resources/{id}/leaderboard.csv'))
#     fig, ax = plt.subplots(1, 1, figsize=(15, 10))
#     leaderboard['train_time'] = leaderboard['train_time'].astype(float)
#     leaderboard['metric_value'] = leaderboard['metric_value'].astype(float)
#     ax.plot(leaderboard['train_time'], leaderboard['metric_value'], 'o')
#     leaderboard['name'] = leaderboard['name'].astype('category')
#     groups = leaderboard.groupby("name")
#     for name, group in groups:
#         plt.plot(group["train_time"], group["metric_value"], marker="o", linestyle="", label=name)
#     for i, txt in enumerate(leaderboard['name']):
#         ax.annotate(txt, (leaderboard['train_time'][i], leaderboard['metric_value'][i]), va='bottom')
#     if leaderboard['metric_type'][1] == 'logloss':
#         ax.set(xlabel='train_time (seconds)', ylabel='metric_value (logloss)')
#     else:
#         ax.set(xlabel='train_time(seconds)', ylabel='metric_value (rmse)')
#     return figure