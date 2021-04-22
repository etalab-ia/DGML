import shutil
from pathlib import Path

from get_dataset import *
from get_statistic_summary import *
from get_mljar import *
import json
import glob

PARAMETER_FILE = Path("config/auto_ml_parameters.json")
if PARAMETER_FILE.exists():
    with open(PARAMETER_FILE) as fout:
        PARAMETERS = json.load(fout)
else:
    raise FileNotFoundError(f"Config file {PARAMETER_FILE.as_posix()} does not exist.")


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


def fill_main_csv(id, catalog, statistics_summary):
    """This function adds a new row in open_ml_datasets.csv containing info of a chosen dataset."""
    main_csv_path = Path().home().joinpath('open_ML/open_ml_app/assets/datasets/open_data_ml_datasets.csv')
    main_df = pd.read_csv(main_csv_path)
    new_row = {}
    for col in main_df.columns:
        new_row.update({col: ''})
    dict_main_df = {'title': 'dataset.title', 'dgf_dataset_url': 'dataset.url', 'dgf_resource_url': 'url'}
    for key, item in dict_main_df.items():
        new_row[key] = catalog[catalog['id'] == id][item].values.item()
    for param in PARAMETERS:
        new_row['target_variable'] = param["target"]
        new_row['task'] = param["task"]
    new_row['nb_lines'] = statistics_summary['Number of lines'][0]
    new_row['nb_features'] = statistics_summary['Number of variables'][0]
    new_row['profile_url'] = f"https://etalab-ia.github.io/open_ML/profilings/{id}.html"
    new_row['automl_url'] = f"https://etalab-ia.github.io/open_ML/automodels/{id}/README.html"
    new_row['dgf_resource_id'] = id
    main_df = main_df.append(new_row, ignore_index=True)
    #main_df.to_csv(main_csv_path, index=False)
    return main_df


def main():
    for param in PARAMETERS:
        id = param["id"]
        output_dir = Path(param["output_dir"]).joinpath(id)
        catalog = fixed_catalog()  # or latest_catalog for using the last catalog

        catalog_info = info_from_catalog(id, catalog)
        output_dir = create_output_folder(output_dir)

        data = load_dataset(id, catalog_info, output_dir=output_dir)
        print("Successfully loaded dataset.")
        profiling = generate_pandas_profiling(id, data, output_dir=output_dir, config_path=None)
        statistics_summary = get_statistics_summary(id, profiling, output_dir=output_dir)
        get_dict_data(id, profiling, output_dir=output_dir)
        print("Successfully generated Pandas Profiling.")
        prep_data = prepare_to_mljar(data=data, target_variable=param["target"],
                                     task=param["task"], profiling=profiling)
        automl = generate_mljar(data=prep_data, target_variable=param["target"], output_dir=output_dir)
        get_mljar_info(output_dir=output_dir, automl_report=automl)
        plot_mljar_table(id)
        print("Successfully generated AutoML report.")
        fill_main_csv(id=id, catalog=catalog, statistics_summary=statistics_summary)
        print("Added info to main csv.")


if __name__ == "__main__":
    main()
