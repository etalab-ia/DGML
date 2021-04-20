import shutil
from pathlib import Path

from get_dataset import *
from get_statistic_summary import *
from get_mljar import *
import json
import glob

PARAMETER_FILE = Path("./open_ml_app/automatization/config/auto_ml_parameters.json")
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
        get_statistics_summary(id, profiling, output_dir=output_dir)
        get_dict_data(id, profiling, output_dir=output_dir)
        print("Successfully generated Pandas Profiling.")
        prep_data = prepare_to_mljar(data=data, target_variable=param["target"],
                                     task=param["task"], profiling=profiling)
        automl = generate_mljar(data=prep_data, target_variable=param["target"], output_dir=output_dir)
        get_mljar_info(output_dir=output_dir, automl_report=automl)
        plot_mljar_table(id)
        print("Successfully generated AutoML report.")


if __name__ == "__main__":
    main()
