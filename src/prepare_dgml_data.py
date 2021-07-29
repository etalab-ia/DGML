"""
This script is the processing pipeline used to create the "automatic" datasets files shown in DGML. The automatic
datasets are those that are not curated but created by this script. There are ___ steps in this pipeline:

   1. Get csv files' paths from dataset_path input parameter
   2. Filter csv paths according to a specific_file text file
   3. Load DGF catalog to retrieve info about datasets
   4. For each dataset (csv) path, do: a. Return the csv dataframe and its metadata load_wrapper() b. Create an output
      folder with the id of the dataset as name c. Discard datasets not passing the first level constraints d. Generate
      pandas profiling. Create file {id}_pandas_profile.html e. Generate pandas profiling summary. Create file
      statistics_summary.csv f. Get data dictionary. Create file dict_data.csv g. Returns clean dataset before mljar.
      h. Discard empty datasets and datasets with less than 3 columns. Save its pandas profile report. i. For each
      target variable (column) in the dataset, do:

            1. Remove missing values in target variable column
            2. Run mljar process. Save output files in {dataset_id}/{automl_target-var}/
            3. Compute and store a score to this mljar run with this dataset and with this target var
            4. Add a new line to the open_data_ml_datasets.csv file with the info of this dataset (pandas profile +
               mljar profile for this run, etc)



Notes:

    1. We remove non-ascii characters within the categorical (nominal) values (it does not work if we don't do this)
    2. We remove the lines with missing values in the target variable

"""

import glob
import logging
import shutil
from pathlib import Path
from typing import Union, Optional

import fire
from pandas.util import hash_pandas_object
from dotenv import load_dotenv
import fs
import pandas as pd
from csv_detective.explore_csv import routine
from fs.glob import GlobMatch
from supervised.model_framework import ModelFramework
from src.get_dataset import latest_catalog, info_from_catalog, load_dataset
from src.get_mljar import prepare_for_mljar, generate_mljar
from src.get_statistic_summary import (
    generate_pandas_profiling,
    get_statistics_summary,
    get_data_dictionary,
)
from app.apps.utils import slugify

load_dotenv(".env")
logging.root.handlers = []
# noinspection PyArgumentList
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"./logs/{Path(__file__).stem}.log", mode="w"),
        logging.StreamHandler(),
    ],
)


def get_specific_datasets(specific_datasets_path: Optional[Path] = None):
    """
    If there is a specific_datasets_path file, take the ids within and process them exclusively. :param
    specific_datasets_path: The path of a text file with id per line :return: List of read ids from the
    specific_datasets_path file
    """
    if specific_datasets_path is None:
        return
    specific_datasets_path = Path(specific_datasets_path)
    with open(specific_datasets_path) as filo:
        specific_datasets = [l.strip() for l in filo.readlines()]
    logging.info(f"We found specific ids. They are: {specific_datasets}")
    return specific_datasets


def create_folder(output_dir, delete_if_exist: bool = False):
    if output_dir.exists() and delete_if_exist:
        shutil.rmtree(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)


def get_mljar_info(output_dir, automl_report):
    """

    :param output_dir:
    :param automl_report:
    :return:
    """
    # 1. Move the leaderboard.csv file (automl summary) to the upper level
    automl_report.get_leaderboard().to_csv(
        output_dir.joinpath("leaderboard.csv"), index=False
    )

    # 2. Delete all models (bc they are heavy and we don't use them)
    model_file_paths = [
        Path(p)
        for p in glob.glob(
            output_dir.as_posix() + f"/**/learner_fold_*.*", recursive=True
        )
    ]
    model_file_paths = [
        p
        for p in model_file_paths
        if p.suffix not in [".csv", ".png", ".log", ".svg"]
    ]
    for model_path in model_file_paths:
        model_path.unlink()


def fill_main_csv(
        id_,
        catalog,
        statistics_summary,
        output_dir=Path("../app/assets/datasets/"),
        target_variable=None,
        task=None,
        score="",
        automl=None,
):
    """This function adds a new row in dgml_datasets.csv containing info of a chosen dataset."""
    main_csv_path = output_dir.joinpath("dgml_datasets.csv")
    new_row = {}
    dict_main_df = {
        "title": "dataset.title",
        "dgf_dataset_url": "dataset.url",
        "dgf_dataset_id": "dataset.id",
        "dgf_resource_url": "url",
        "description": "description"
    }
    for key, item in dict_main_df.items():
        new_row[key] = catalog[catalog["id"] == id_][item].values.item()
    new_row["nb_lines"] = statistics_summary["Number of lines"][0]
    new_row["nb_features"] = statistics_summary["Number of variables"][0]
    new_row["profile_url"] = f""
    if target_variable is None and task is None:
        # In this case, we only computed the pandas profiling
        new_row["automl_url"] = ""
        new_row["target_variable"] = ""
        new_row["task"] = ""
    else:
        new_row["automl_url"] = ""
        new_row["target_variable"] = target_variable
        if "classification" in task.lower():
            new_row["task"] = "Classification"
        else:
            new_row["task"] = task.capitalize()
    new_row["is_validated"] = False
    new_row["topic"] = "Undefined"
    new_row["dict_url"] = ""
    new_row["dgf_resource_id"] = id_
    new_row["openml_id"] = ""
    # add info about best model:
    if automl is None:
        new_row["best_model"] = ""
        new_row["metric_type"] = ""
        new_row["metric_value"] = ""
    else:
        if isinstance(automl._best_model, ModelFramework):
            new_row["best_model"] = automl._best_model.get_name()
            new_row["metric_type"] = automl._best_model.metric_name
            new_row["metric_value"] = automl._best_model.get_final_loss()
        else:
            new_row["best_model"] = automl._best_model.algorithm_short_name
            new_row["metric_type"] = automl._get_eval_metric()
            new_row["metric_value"] = automl._best_model.best_loss
    if main_csv_path.exists():
        main_df = pd.read_csv(main_csv_path)
        main_df = main_df.append(new_row, ignore_index=True)
    else:
        main_df = pd.DataFrame([new_row])
    # add score to main csv file:
    main_df.loc[
        (main_df["dgf_resource_id"] == id_)
        & (main_df["target_variable"] == target_variable),
        ["score"],
    ] = score
    main_df.to_csv(main_csv_path, index=False)
    return main_df


def check_constraints(data):
    """
    This function checks that the given dataset respects the following constraints:

    * 200 <= number of lines <= 2*10⁶
    * 3 <= number of columns <= 500
    * nb_lines / nb_columns >=10
    * has both numerical and categorical variables
    * < 30% missing values overall
    :param: :data: dataset we want to check :type: :data: pandas dataframe
    """
    passed_constraints = False
    nb_lines = len(data)
    nb_columns = len(data.columns)
    check_categorical = data.select_dtypes(include="object").empty
    check_numerical = data.select_dtypes(include=["float64", "int64"]).empty
    total_nan = data.isna().sum().sum() / (nb_lines * nb_columns)
    if (
            (200 <= nb_lines <= 2 * (10 ** 6))
            and (3 <= nb_columns <= 500)
            and ((nb_lines / nb_columns) >= 10)
            and (check_categorical is False)
            and (check_numerical is False)
            and (total_nan <= 0.30)
    ):
        passed_constraints = True
    return passed_constraints


# TO DO: add these parameters to a config file
def load_dataset_wrapper(dataset_name: Union[Path, str]):
    csv_data = None
    if isinstance(dataset_name, Path):
        try:
            csv_data = routine(dataset_name.as_posix(), num_rows=200)
        except Exception as e:
            logging.exception(
                f"Dataset {dataset_name}: csv-detective analysis failed"
            )
            raise e

        encoding = csv_data.get("encoding", "latin-1")
        separator = csv_data.get("separator", ",")
        dataset_df = pd.read_csv(dataset_name, sep=separator, encoding=encoding)
        dataset_df.rename(columns=slugify, inplace=True)
        id_data = dataset_name.stem

    else:
        catalog = latest_catalog()  # or fixed_catalog to use our catalog
        catalog_info = info_from_catalog(dataset_name, catalog)
        dataset_df = load_dataset(id=dataset_name, catalog_info=catalog_info)
        id_data = dataset_name

    return dataset_df, id_data, csv_data


def get_csv_paths(datasets_path: Path):
    def create_files_iterator(remote_globber: GlobMatch):
        """

        :param remote_globber:
        :return:
        """
        temp_path = Path("/tmp").joinpath(
            Path(remote_globber.path).stem.split("--")[1] + ".csv"
        )
        with open(temp_path, "wb") as tmp:
            my_fs.download(remote_globber.path, tmp)
        return Path(tmp.name)

    """Return the paths of each dataset in the source CSVs folder, whether local or through a sftp connection"""
    # 1. If the dataset_path is local, just return the lisst of csv files
    if "sftp" not in datasets_path.as_posix():
        if not datasets_path.exists():
            raise FileNotFoundError(
                f"File {datasets_path} not found. Please choose another csv folder"
            )
        csv_paths = [
            Path(p)
            for p in glob.glob(
                datasets_path.as_posix() + f"/*.csv", recursive=True
            )
        ]
    else:
        # 2. Try to connect to this remote resource (only dealing with sftp)
        # noinspection PyBroadException
        try:
            my_fs = fs.open_fs(datasets_path)
            csv_paths = (
                create_files_iterator(path)
                for path in my_fs.glob("**/*.csv").__iter__()
            )
        except Exception as e:
            logging.exception(f"Connecting to {datasets_path} did not work")
            raise e
    return csv_paths


def generate_score(statistics_summary, columns_to_drop, automl):
    """
    Returns a score of the evaluating the 'goodness' of a given dataset. Datasets with an higher score will be selected
    for the app. The score takes into account:

    * the overall percentage of missing values, extracted from the pandas df of statistics_summary.csv (30%)
    * the percentage of variables not retained when running mljar (warning columns and columns detected by csv
      detective) (40%)
    * the logloss (for classification) or rmse (for regression) value for the best model (30%), extracted
      leaderboard.csv
    """
    prop_missing = statistics_summary["Percentage of missing cells"] / 100
    prop_not_retained = (
            len(columns_to_drop) / statistics_summary["Number of variables"]
    )
    best_metric = automl.get_leaderboard()["metric_value"].min()
    score = 1 / (
            0.3 * prop_missing + 0.4 * prop_not_retained + 0.3 * best_metric
    )
    return score


def main(
        dataset_path: str,
        output_dir: str,
        specific_datasets_path: str = None,
        automl_mode: str = "Explain",
):
    """

    :param dataset_path: Folder with CSVs files :param output_dir: Folder were the output is saved :param
    specific_datasets_path: Path to a text file with a file name per line. Only this files will be treated :param
    automl_mode: "perform" ou "explain". Perform maximizes the model performance. Explain maximizes the explicability
    of the models. :return: None
    """

    seen_dataframes = set()
    output_dir = Path(output_dir)
    dataset_path = Path(dataset_path)
    dataset_paths = get_csv_paths(dataset_path)

    specific_datasets = get_specific_datasets(specific_datasets_path)
    automl_mode = automl_mode
    catalog = latest_catalog()  # or fixed_catalog to use our catalog
    for ix, path in enumerate(dataset_paths):
        if specific_datasets and path.stem not in specific_datasets:
            logging.warning(
                f"We are only analysing specific ids. Id {path.stem} is not a specified id. Trying "
                f"next..."
            )
            continue
        try:
            data_df, id_data, csv_detective_data = load_dataset_wrapper(path)
            df_hash = hash_pandas_object(data_df).sum()
            if df_hash in seen_dataframes:
                logging.info(
                    f"Dataset {id_data}: Same hash dataset already treated. Skipping dataset."
                )
                continue
            seen_dataframes.add(df_hash)
            logging.info(f"Treating Dataset {id_data} ({ix})")
            current_output_dir = output_dir.joinpath(id_data)
            logging.info(f"Dataset {id_data}: Successfully loaded dataset.")
            create_folder(current_output_dir, delete_if_exist=True)
            create_folder(current_output_dir / "our_experiments")
            if not check_constraints(data_df):
                logging.warning(
                    f"The Dataset {id_data} did not pass the first-level constraints. It seems not adequate for Machine "
                    f"Learning"
                )
                continue
            logging.info(
                f"Dataset {id_data}: passed the first-level constraints"
            )
            profiling = generate_pandas_profiling(
                id_data,
                data_df,
                output_dir=current_output_dir,
                config_path=None,
            )
            statistics_summary = get_statistics_summary(
                profiling, output_dir=current_output_dir
            )

            get_data_dictionary(profiling, output_dir=current_output_dir)
            logging.info(
                f"Dataset {id_data}: Successfully generated Pandas Profiling."
            )
            prep_data, columns_to_drop = prepare_for_mljar(
                data=data_df, profiling=profiling, csv_data=csv_detective_data
            )
            logging.info(
                f"Dataset {id_data}: removed the following columns: {columns_to_drop}"
            )
            logging.info(
                f"Dataset {id_data}: the following columns are left: {list(prep_data.columns)}"
            )
            if prep_data is not None and len(prep_data.columns) < 3:
                logging.warning(
                    f"Dataset {id_data}: We have less than 3 columns. "
                    f"We will only generate the pandas profiling"
                )
                fill_main_csv(
                    id_=id_data,
                    catalog=catalog,
                    output_dir=output_dir,
                    statistics_summary=statistics_summary,
                    score="",
                )
                continue
            for target_variable in prep_data.columns:
                try:
                    logging.info(
                        f"Dataset {id_data}: Testing AutoML models with target var {target_variable}"
                    )
                    # drop nan lines
                    notna_data = prep_data[prep_data[target_variable].notna()]
                    mljar_output_dir = current_output_dir.joinpath(
                        f"automl_{target_variable}"
                    )
                    automl = generate_mljar(
                        data=notna_data,
                        target_variable=target_variable,
                        output_dir=mljar_output_dir,
                        automl_mode=automl_mode,
                    )
                    get_mljar_info(
                        output_dir=mljar_output_dir, automl_report=automl
                    )
                    # plot_mljar_table(id)
                    logging.info(
                        f"Dataset {id_data}: Successfully generated AutoML report."
                    )
                    task = automl._get_ml_task()
                    score = generate_score(
                        statistics_summary=statistics_summary,
                        columns_to_drop=columns_to_drop,
                        automl=automl,
                    )
                    logging.info(f"Dataset {id_data}: The score is: {score[0]}")
                    fill_main_csv(
                        id_=id_data,
                        catalog=catalog,
                        statistics_summary=statistics_summary,
                        output_dir=output_dir,
                        target_variable=target_variable,
                        task=task,
                        score=score[0],
                        automl=automl,
                    )
                    logging.info(
                        f"Dataset {id_data}: Added info to main datasets csv."
                    )
                except Exception:
                    logging.exception(
                        f"Dataset {id_data}: Fatal error while testing var {target_variable}"
                    )
                    continue

        except Exception:
            logging.exception(
                f"Dataset {path}: Fatal error while treating file"
            )


if __name__ == "__main__":
    fire.Fire(main)
