import pandas_profiling
from pandas_profiling import ProfileReport
from get_dataset import *


def generate_pandas_profiling(id, data, output_dir, config_path=None):
    """Returns the Pandas Profiling of this dataset. The name of the output html file is id.html
    --------------------------------------------
    :param:       id: id of the dataset
    :type:        id: string
    """

    profiling = ProfileReport(data, minimal=True, config_file=config_path)
    profiling.to_file(output_dir.joinpath(f"{id}_pandas_profile.html"))
    return profiling


def get_statistics_summary(id, profiling, output_dir):
    """Returns a csv file containing all the relevant dataset statistics from pandas profiling.
    This summary is the info pandas profiling info we display in the web page
    -----------------------------------------------
    :param:       id: id of the dataset
    :type:        id: string
    """
    get_description = profiling.get_description()
    table = get_description['table']
    keys_to_extract = ['n', 'n_var', 'p_cells_missing']
    dict_stats_table = {key: table[key] for key in keys_to_extract}  # nb of rows, columns and percentage of nan
    dict_stats_table['Number of lines'] = dict_stats_table.pop('n')  # properly rename keys
    dict_stats_table['Number of variables'] = dict_stats_table.pop('n_var')
    dict_stats_table['Percentage of missing cells'] = dict_stats_table.pop('p_cells_missing')
    dict_stats_table['Percentage of missing cells'] = round(dict_stats_table['Percentage of missing cells'], 2) * 100
    table['types'] = {str(k): int(v) for k, v in table['types'].items()}  # categorical/numerical variables
    if 'Numeric' not in table['types']:
        table['types']['Numeric'] = 0
    elif 'Categorical' not in table['types']:
        table['types']['Categorical'] = 0
    messages = get_description["messages"]
    warnings = ["HIGH_CARDINALITY", "HIGH_CORRELATION"]  # high cardinality, high correlation columns
    nb_high_card = 0
    nb_high_corr = 0
    for message in messages:
        message_type = message.message_type.name
        if message_type in warnings[0]:
            nb_high_card += 1
        elif message_type in warnings[1]:
            nb_high_corr += 1
    dict_warnings = {"High cardinality variables": nb_high_card, "High correlation variables": nb_high_corr}
    dict_for_df = {**dict_stats_table, **table['types'], **dict_warnings}
    df = pd.DataFrame(dict_for_df, index=[0])
    df.to_csv(output_dir.joinpath("statistics_summary.csv"))
    return df


def get_dict_data(id, profiling, output_dir):
    """This function returns a csv file called dict_data containing a list of all the variables together with their detected types and
    two empty columns. These two should then be manually updated if a dictionary is available. If not, manually delete the two central columns.
    -----------------------------------------------
    :param:       id: id of the dataset
    :type:        id: str
    :param:       profiling: Pandas Profiling
    :type:        profiling: pandas profiling
    :param:       output_dir: output directory for the csv
    :type:        output_dir: str"""
    data_dict = {}
    get_description = profiling.get_description()
    variables_description = get_description['variables']
    for variable in variables_description:
        data_dict.update({str(variable): [variables_description[variable]['type']]})
    dict_df = pd.DataFrame.from_dict(data_dict, orient='index')
    dict_df = dict_df.reset_index()
    dict_df = dict_df.rename(columns={"index": "Name", 0: "Detected Type"})
    data_dict_df = pd.DataFrame({'Name': [], 'Dictionary Description': [], 'Dictionary Type': [], 'Detected Type': []})
    for col in data_dict_df.columns:
        if str(col) in dict_df:
            data_dict_df[col] = dict_df[col]
    data_dict_df.to_csv(output_dir.joinpath('dict_data.csv'), index=False)
    return data_dict_df


def rejected_var(profiling):
    """This function returns a list of the variables detected as unsupported by Pandas Profiling.
    -----------------------------------
    :param:       id: id of the dataset
    :type:        id: string
    """
    get_description = profiling.get_description()
    messages = get_description["messages"]
    pos_rej = -1
    list_rej = []
    for message in messages:
        pos_rej += 1
        message_type = message.message_type.name
        if message_type == 'REJECTED':
            rejected_mess = str(messages[pos_rej])
            rej_name = rejected_mess.split("warning on column ", 1)[1]
            list_rej.append(rej_name)
    return list_rej
