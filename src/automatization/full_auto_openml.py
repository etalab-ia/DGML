# from get_mljar import *
import glob
from pathlib import Path
from typing import Union
from csv_detective.explore_csv import routine
import pandas as pd
from tqdm import tqdm

from src.automatization.get_dataset import latest_catalog, info_from_catalog, load_dataset
from src.automatization.get_mljar import prepare_to_mljar, generate_mljar
from src.automatization.get_statistic_summary import generate_pandas_profiling, get_statistics_summary, get_dict_data, \
    is_a_warning_col

SAMPLE_DATASETS = Path('../../data/data.gouv/csv_top')
OUTPUT_DIR = Path('../../datasets/resources')


def create_output_folder(output_dir):
    if not output_dir.exists():
        output_dir.mkdir()


def get_mljar_info(output_dir, automl_report):
    # 1. Move the leaderboard.csv file (automl summary) to the upper level
    automl_report.get_leaderboard().to_csv(output_dir.joinpath("leaderboard.csv"), index=False)

    # 2. Delete all models (bc they are heavy and we don't use them)
    automl_path = output_dir.joinpath("automl")
    model_file_paths = [Path(p) for p in glob.glob(automl_path.as_posix() + f"/**/learner_fold_*.*", recursive=True)]
    model_file_paths = [p for p in model_file_paths if
                        p.suffix not in [".csv", ".png", ".log", ".svg"]]
    for model_path in model_file_paths:
        model_path.unlink()


def fill_main_csv(id, catalog, statistics_summary, target_variable='', task=''):
    """This function adds a new row in open_ml_datasets.csv containing info of a chosen dataset."""
    main_csv_path = Path('../../open_ml_app/assets/datasets/open_data_ml_datasets.csv')
    main_df = pd.read_csv(main_csv_path)
    new_row = {}
    for col in main_df.columns:
        new_row.update({col: ''})
    dict_main_df = {'title': 'dataset.title', 'dgf_dataset_url': 'dataset.url', 'dgf_resource_url': 'url'}
    for key, item in dict_main_df.items():
        new_row[key] = catalog[catalog['id'] == id][item].values.item()
    new_row['target_variable'] = target_variable
    new_row['task'] = task
    new_row['nb_lines'] = statistics_summary['Number of lines'][0]
    new_row['nb_features'] = statistics_summary['Number of variables'][0]
    new_row['profile_url'] = f"https://etalab-ia.github.io/open_ML/profilings/{id}.html"
    if not target_variable and not task:
        new_row['automl_url'] = f"https://etalab-ia.github.io/open_ML/automodels/{id}/README.html"
    else:
        new_row['automl_url'] = ''
    new_row['dgf_resource_id'] = id
    main_df = main_df.append(new_row, ignore_index=True)
    main_df.to_csv(main_csv_path, index=False)
    return main_df


def check_constraints(data):
    """This function checks that the given dataset respects the following constraints:
    * 200 <= number of lines <= 2*10⁶
    * 3 <= number of columns <= 500
    * nb_lines / nb_columns >=10
    * has both numerical and categorical variables
    * < 30% missing values overall
    :param:     :data: dataset we want to check
    :type:      :data: pandas dataframe
    """
    passed_constraints = False
    nb_lines = len(data)
    nb_columns = len(data.columns)
    check_categorical = data.select_dtypes(include='object').empty
    check_numerical = data.select_dtypes(include=['float64', 'int64']).empty
    total_nan = data.isna().sum().sum() / (nb_lines * nb_columns)
    if (200 <= nb_lines <= 2 * (10 ** 6)) and (3 <= nb_columns <= 500) and ((nb_lines / nb_columns) >= 10) and (
            check_categorical is False) and (check_numerical is False) and (total_nan <= 30):
        passed_constraints = True
    return passed_constraints


# TO DO: add these parameters to a config file
def load_dataset_wrapper(dataset_name: Union[Path, str]):
    if isinstance(dataset_name, Path):
        csv_metadata = routine(dataset_name.as_posix(), user_input_tests=None)
        encoding = csv_metadata.get("encoding", "latin-1")
        separator = csv_metadata.get("separator", ",")
        dataset_df = pd.read_csv(dataset_name, sep=separator, encoding=encoding)
        id_data = dataset_name.stem
    else:
        catalog = latest_catalog()  # or fixed_catalog to use our catalog
        catalog_info = info_from_catalog(dataset_name, catalog)
        dataset_df = load_dataset(id=dataset_name, catalog_info=catalog_info)
        id_data = dataset_name
    return dataset_df, id_data


def main():
    global OUTPUT_DIR
    ids = [Path(p) for p in glob.glob(SAMPLE_DATASETS.as_posix() + f"/*.csv", recursive=True)]

    catalog = latest_catalog()  # or fixed_catalog to use our catalog
    for id_ in tqdm(ids, desc="CSVs", unit="csv-file"):
        data, id_data = load_dataset_wrapper(id_)
        print(f"Treating file with id {id_}")
        current_output_dir = OUTPUT_DIR.joinpath(id_data)
        create_output_folder(current_output_dir)
        print("Successfully loaded dataset.")
        if check_constraints(data):
            profiling = generate_pandas_profiling(id_data, data, output_dir=current_output_dir, config_path=None)
            statistics_summary = get_statistics_summary(profiling, output_dir=current_output_dir)
            get_dict_data(id_data, profiling, output_dir=current_output_dir)
            print("Successfully generated Pandas Profiling.")
            for column in tqdm(data.columns):
                if is_a_warning_col(column, profiling=profiling):
                    data = data.drop(columns=column)
            if len(data.columns) >= 3:
                for target_variable in data.columns:
                    prep_data = prepare_to_mljar(data=data, target_variable=target_variable,
                                                 profiling=profiling)
                    automl = generate_mljar(data=prep_data, target_variable=target_variable,
                                            output_dir=current_output_dir)
                    get_mljar_info(output_dir=current_output_dir, automl_report=automl)
                    # plot_mljar_table(id)
                    print("Successfully generated AutoML report.")
                    task = automl._get_ml_task()
                    fill_main_csv(id=id_data, catalog=catalog, statistics_summary=statistics_summary,
                                  target_variable=target_variable, task=task)
                    print("Added info to main csv.")
            else:
                print(f'The dataset with id {id_data} cannot be used to obtain meaningful results with AutoML.')
                fill_main_csv(id=id_data, catalog=catalog, statistics_summary=statistics_summary)
        else:
            print(f'The dataset with id: {id_data} is not adequate for Machine Learning')



if __name__ == "__main__":
    main()
