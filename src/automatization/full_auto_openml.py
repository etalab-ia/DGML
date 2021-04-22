import shutil
from pathlib import Path

from get_dataset import *
from get_statistic_summary import *
from get_mljar import *
import json
import glob

def create_output_folder(output_dir):
    if not output_dir.exists():
        output_dir.mkdir()
    return output_dir


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


def fill_main_csv(id, catalog, statistics_summary, target_variable, task):
    """This function adds a new row in open_ml_datasets.csv containing info of a chosen dataset."""
    main_csv_path = Path().home().joinpath('open_ML/open_ml_app/assets/datasets/open_data_ml_datasets.csv')
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
    new_row['automl_url'] = f"https://etalab-ia.github.io/open_ML/automodels/{id}/README.html"
    new_row['dgf_resource_id'] = id
    main_df = main_df.append(new_row, ignore_index=True)
    # main_df.to_csv(main_csv_path, index=False)
    return main_df


def check_constraints(data):
    """This function checks that the given dataset respects the following constraints:
    * 200 <= number of lines <= 2*10⁶
    * 3 <= number of columns <= 500
    * lines_cols_ratio >=10
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


def main():
    sample_datasets = Path().home().joinpath('open_ML/data/data.gouv/csv_top')
    ids = [Path(p).stem for p in glob.glob(sample_datasets.as_posix() + f"/*.csv", recursive=True)]
    catalog = latest_catalog()  # or latest_catalog for using the last catalog
    for id in ids:
        output_dir = Path().home().joinpath('open_ML/datasets/resources').joinpath(id)
        catalog_info = info_from_catalog(id, catalog)
        output_dir = create_output_folder(output_dir)

        data = load_dataset(id, catalog_info, output_dir=output_dir)
        print("Successfully loaded dataset.")
        if check_constraints(data):
            profiling = generate_pandas_profiling(id, data, output_dir=output_dir, config_path=None)
            statistics_summary = get_statistics_summary(profiling, output_dir=output_dir)
            get_dict_data(id, profiling, output_dir=output_dir)
            print("Successfully generated Pandas Profiling.")
            for target_variable in data.columns:
                prep_data = prepare_to_mljar(data=data, target_variable=target_variable,
                                             profiling=profiling)
                automl = generate_mljar(data=prep_data, target_variable=target_variable, output_dir=output_dir)
                get_mljar_info(output_dir=output_dir, automl_report=automl)
                #plot_mljar_table(id)
                print("Successfully generated AutoML report.")
                task = automl.ml_task
                fill_main_csv(id=id, catalog=catalog, statistics_summary=statistics_summary,
                              target_variable=target_variable, task=task)
                print("Added info to main csv.")
        else:
            raise Exception('This dataset is not adequate for Machine Learning')


if __name__ == "__main__":
    main()
