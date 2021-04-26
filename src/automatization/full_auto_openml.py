import glob
import logging
import re
import shutil
import unicodedata
from pathlib import Path
from typing import Union

import fs
import pandas as pd
from csv_detective.explore_csv import routine
from fs.glob import GlobMatch

from get_dataset import latest_catalog, info_from_catalog, load_dataset
from get_mljar import prepare_to_mljar, generate_mljar
from get_statistic_summary import generate_pandas_profiling, get_statistics_summary, get_dict_data

logging.root.handlers = []
# noinspection PyArgumentList
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log", mode="w"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
DATASETS_PATH = '../../data/data.gouv/csv_top'

OUTPUT_DIR = Path('../../datasets/resources')


def create_output_folder(output_dir):
    if not output_dir.exists():
        output_dir.mkdir()


def get_mljar_info(output_dir, automl_report):
    # 1. Move the leaderboard.csv file (automl summary) to the upper level
    automl_report.get_leaderboard().to_csv(output_dir.joinpath("leaderboard.csv"), index=False)

    # 2. Delete all models (bc they are heavy and we don't use them)
    model_file_paths = [Path(p) for p in glob.glob(output_dir.as_posix() + f"/**/learner_fold_*.*", recursive=True)]
    model_file_paths = [p for p in model_file_paths if
                        p.suffix not in [".csv", ".png", ".log", ".svg"]]
    for model_path in model_file_paths:
        model_path.unlink()


def fill_main_csv(id_, catalog, statistics_summary, output_dir=Path("../../open_ml_app/assets/datasets/"),
                  target_variable='', task='', score=''):
    """This function adds a new row in open_ml_datasets.csv containing info of a chosen dataset."""
    main_csv_path = output_dir.joinpath('open_data_ml_datasets.csv')
    new_row = {}

    dict_main_df = {'title': 'dataset.title', 'dgf_dataset_url': 'dataset.url', 'dgf_resource_url': 'url'}
    for key, item in dict_main_df.items():
        new_row[key] = catalog[catalog['id'] == id_][item].values.item()
    new_row['target_variable'] = target_variable
    new_row['task'] = task
    new_row['nb_lines'] = statistics_summary['Number of lines'][0]
    new_row['nb_features'] = statistics_summary['Number of variables'][0]
    new_row['profile_url'] = f"https://etalab-ia.github.io/open_ML/profilings/{id_}.html"
    if not target_variable and not task:
        new_row['automl_url'] = f"https://etalab-ia.github.io/open_ML/automodels/{id_}/README.html"
    else:
        new_row['automl_url'] = ''
    new_row['dgf_resource_id'] = id_
    if main_csv_path.exists():
        main_df = pd.read_csv(main_csv_path)
        # for col in main_df.columns:
        #     new_row.update({col: ''})
        main_df = main_df.append(new_row, ignore_index=True)
    else:
        main_df = pd.DataFrame([new_row])
    # add score to main csv file:
    main_df.loc[
        (main_df['dgf_resource_id'] == id_) & (main_df['target_variable'] == target_variable), ['score']] = score
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
    csv_data = None
    if isinstance(dataset_name, Path):
        try:
            csv_data = routine(dataset_name.as_posix(), num_rows=200)
        except Exception as e:
            logger.exception(f"Dataset {dataset_name}: csv-detective analysis failed")
            raise e

        encoding = csv_data.get("encoding", "latin-1")
        separator = csv_data.get("separator", ",")
        dataset_df = pd.read_csv(dataset_name, sep=separator, encoding=encoding)
        id_data = dataset_name.stem
        # Delete file if it is a temp file (in /tmp)
        if "/tmp" in dataset_name.as_posix():
            dataset_name.unlink()

    else:
        catalog = latest_catalog()  # or fixed_catalog to use our catalog
        catalog_info = info_from_catalog(dataset_name, catalog)
        dataset_df = load_dataset(id=dataset_name, catalog_info=catalog_info)
        id_data = dataset_name

    return dataset_df, id_data, csv_data


def get_csv_paths(datasets_path: str):
    def create_files_iterator(remote_globber: GlobMatch):
        temp_path = Path("/tmp").joinpath(Path(remote_globber.path).stem.split("--")[1] + ".csv")
        with open(temp_path, "wb") as tmp:
            my_fs.download(remote_globber.path, tmp)
        return Path(tmp.name)

    """Return the paths of each dataset in the source CSVs folder, whether local or through a sftp connection"""
    # 1. If the dataset_path is local, just return the lisst of csv files
    if "sftp" not in datasets_path:
        csv_paths = [Path(p) for p in glob.glob(DATASETS_PATH + f"/*.csv", recursive=True)]
    else:
        # 2. Try to connect to this remote resource (only dealing with sftp)
        # noinspection PyBroadException
        try:
            my_fs = fs.open_fs(datasets_path)
            csv_paths = (create_files_iterator(path) for path in my_fs.glob("**/*.csv").__iter__())
        except Exception as e:
            logger.exception(f"Connecting to {datasets_path} did not work")
            raise e
    return csv_paths


def generate_score(statistics_summary, columns_to_drop, current_output_dir):
    """Returns a score of the evaluating the 'goodness' of a given dataset. Datasets with an higher score will be selected for the app.
    The score takes into account:
    * the overall percentage of missing values, extracted from the pandas df of statistics_summary.csv (30%)
    * the percentage of variables not retained when running mljar (warning columns and columns detected by csv detective) (40%)
    * the logloss (for classification) or rmse (for regression) value for the best model (30%), extracted leaderboard.csv """
    prop_missing = statistics_summary['Percentage of missing cells'] / 100
    prop_not_retained = len(columns_to_drop) / statistics_summary['Number of variables']
    path_leaderboard = current_output_dir.joinpath('leaderboard.csv')
    leaderboard_df = pd.read_csv(path_leaderboard)
    best_metric = leaderboard_df['metric_value'].min()
    score = 1 / (0.3 * (prop_missing) + 0.4 * (prop_not_retained) + 0.3 * (best_metric))
    return score


def main():
    global OUTPUT_DIR

    dataset_paths = get_csv_paths(DATASETS_PATH)
    catalog = latest_catalog()  # or fixed_catalog to use our catalog
    for ix, dataset_path in enumerate(dataset_paths):
        current_output_dir = None
        try:
            data, id_data, csv_data = load_dataset_wrapper(dataset_path)
            logger.info(f"Treating Dataset {id_data} ({ix})")
            current_output_dir = OUTPUT_DIR.joinpath(id_data)
            create_output_folder(current_output_dir)
            logger.debug(f"Dataset {id_data}: Successfully loaded dataset.")
            if not check_constraints(data):
                logger.warning(
                    f"The Dataset {id_data} did not pass the first-level constraints. It seems not adequate for Machine "
                    f"Learning")
                continue
            logger.info(f"Dataset {id_data}: passed the first-level constraints")
            profiling = generate_pandas_profiling(id_data, data, output_dir=current_output_dir, config_path=None)
            statistics_summary = get_statistics_summary(profiling, output_dir=current_output_dir)
            get_dict_data(id_data, profiling, output_dir=current_output_dir)
            logger.info(f"Dataset {id_data}: Successfully generated Pandas Profiling.")
            prep_data, columns_to_drop = prepare_to_mljar(data=data, profiling=profiling, csv_data=csv_data)
            logger.info(f"Dataset {id_data}: removed the following columns: {columns_to_drop}")
            logger.info(f"Dataset {id_data}: the following columns are left: {list(prep_data.columns)}")
            if prep_data is not None and len(prep_data.columns) < 3:
                logger.warning(f"Dataset {id_data}: We have less than 3 columns. "
                               f"We will only generate the pandas profiling")
                fill_main_csv(id_=id_data, catalog=catalog, output_dir=OUTPUT_DIR,
                              statistics_summary=statistics_summary, score='')
                continue
            for target_variable in prep_data.columns:
                slugified_target_variable = slugify(target_variable)
                try:
                    logger.info(f"Dataset {id_data}: Testing AutoML models with target var {target_variable}")
                    # drop nan lines
                    notna_data = prep_data[prep_data[target_variable].notna()]
                    mljar_output_dir = current_output_dir.joinpath(f"automl_{slugified_target_variable}")
                    automl = generate_mljar(data=notna_data, target_variable=target_variable,
                                            output_dir=mljar_output_dir)
                    get_mljar_info(output_dir=mljar_output_dir, automl_report=automl)
                    # plot_mljar_table(id)
                    logger.info(f"Dataset {id_data}: Successfully generated AutoML report.")
                    task = automl._get_ml_task()
                    score = generate_score(statistics_summary=statistics_summary, columns_to_drop=columns_to_drop,
                                           current_output_dir=mljar_output_dir)
                    logger.info(f"the score is: {score[0]}")
                    fill_main_csv(id_=id_data, catalog=catalog, statistics_summary=statistics_summary,
                                  output_dir=OUTPUT_DIR,
                                  target_variable=target_variable, task=task, score=score[0])
                    logger.info(f"Dataset {id_data}: Added info to main datasets csv.")
                except Exception:
                    logger.exception(f"Dataset {id_data}: Fatal error while testing var {target_variable}")
                    continue

        except Exception:
            logger.exception(f"Dataset {dataset_path}: Fatal error while treating file")
        finally:
            if current_output_dir is not None and not len(list(current_output_dir.iterdir())):
                shutil.rmtree(current_output_dir.as_posix())


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


if __name__ == "__main__":
    main()
