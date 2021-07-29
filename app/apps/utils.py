import json
from pathlib import Path
from typing import Dict, Tuple, Union, Optional

import dash_bootstrap_components as dbc
import dash_html_components as html

import pandas as pd
import requests


def load_data_path():
    data_path = Path(json.load(open("filters.json"))["DATA_PATH"])
    if not data_path.exists():
        raise FileNotFoundError(
            f"The output DGML folder {data_path} does not exist. Set the correct DATA_PATH in filters.json.")
    return data_path


DATA_PATH = load_data_path()

NB_FEATURES_CATEGORIES = {
    "<10": (1, 10),
    ">=10<100": (10, 100),
    ">=100<500": (100, 500),
    ">=500": (500, 1e100),
}

NB_LINES_CATEGORIES = {
    "<100": (1, 100),
    ">=100<1000": (100, 1000),
    ">=1000<5000": (1000, 5000),
    ">=5000<10000": (5000, 10000),
    ">=10000": (10000, 1e100),
}
DATASET_COLUMNS = {
    "Tâche": "task",
    "Thème": "topic",
    "Colonnes": "nb_features",
    "Lignes": "nb_lines",
    "Validé": "is_validated",
}

DATASET_NAME = {"Name": "title"}


def get_category(categories_dict: Dict[str, Tuple[int, int]], value: int):
    for cat, (min_val, max_val) in categories_dict.items():
        if min_val <= value < max_val:
            return cat
    else:
        return None


def add_nb_features_category(df: pd.DataFrame):
    df["nb_features_cat"] = df.nb_features.apply(
        lambda x: get_category(NB_FEATURES_CATEGORIES, x)
    )


def add_nb_lines_category(df: pd.DataFrame):
    df["nb_lines_cat"] = df.nb_lines.apply(
        lambda x: get_category(NB_LINES_CATEGORIES, x)
    )


def generate_kpi_card(title: str, value: Union[int, str], color: Optional = None):
    dataset_kpi_card = dbc.Card(
        [
            dbc.CardHeader(
                html.B(title),
                style={
                    "height": "50%",
                    "textAlign": "center",
                    "font-family": "Acumin",
                },
            ),
            dbc.CardBody(
                [
                    html.P(
                        value,
                        style={
                            "height": "100%",
                            "textAlign": "center",
                            "font-family": "AcuminL",
                        },
                    ),
                ],
            ),
        ],
        color="primary" if not color else color,
        outline=True,
        # style={"width": "1cm", "height": "10rem"},
    )
    return dataset_kpi_card


def get_reuses(dgf_dataset_id: str):
    api_request = f"https://www.data.gouv.fr/api/1/reuses/?dataset={dgf_dataset_id}&page=0&page_size=50"
    response = requests.get(api_request)
    if response.status_code != 200:
        return
    response_json = response.json()
    return response_json


def filter_reuses(reuses_dict: Dict):
    """
    Filter reuses and returns only those that contain some machine learning-y term in the description
    :param reuses_dict:
    :return:
    """
    list_ml_terms = [
        "deep learning",
        "apprentissage automatique",
        "machine learning",
        "classification",
        "data science",
        "prédire",
    ]
    ml_reuses = []
    for reuse in reuses_dict["data"]:
        if not reuse["featured"]:
            # reuse not featured, continue
            continue
        reuse_ml_terms = [
            term in reuse["description"].lower() for term in list_ml_terms
        ]
        if not any(reuse_ml_terms):
            # no ml terms, continue
            continue
        ml_reuses.append(reuse)

    return ml_reuses


def generate_badge(
        title: str,
        url: str,
        background_color: str,
        font_color: str = "#333333",
        new_tab: bool = False,
):
    if pd.isna(url):
        title = f"{title} non disponible 😞"
        badge = dbc.Badge(
            title,
            style={"backgroundColor": background_color, "color": font_color},
            pill=True,
            className="ml-2",
        )
    else:
        badge = dbc.Badge(
            title,
            href=url,
            target="_blank" if new_tab else False,
            style={"backgroundColor": background_color, "color": font_color},
            pill=True,
            className="ml-2",
            external_link=True,
        )
    return badge


def get_mljar_info():
    def generate_mljar_model_tables(available_target_variables):
        dict_target_vars = {}
        for tar_var_path in available_target_variables:
            display_table_path = tar_var_path.joinpath("leaderboard.csv")

            if not display_table_path.exists():
                html_table = html.H5("MLJAR profile preview not available")
            else:
                table_df = pd.read_csv(display_table_path)
                table_df["metric_value"] = table_df["metric_value"].round(decimals=3)
                algorithm_urls = [
                    html.A(
                        html.P(n),
                        href=tar_var_path.joinpath(f"{n}/README.html").as_posix(),
                        target="_blank",
                    )
                    for n in table_df.name
                ]
                table_df["name"] = algorithm_urls
                html_table = dbc.Table.from_dataframe(
                    table_df, striped=True, size="sm", borderless=True
                )
            dict_target_vars[tar_var_path.stem.split("_")[1]] = (
                html_table,
                display_table_path.parent.joinpath("README.html"),
            )
        return dict_target_vars

    dict_dataset_mljar = {}
    dataset_folders = [
        Path(paths).stem
        for paths in DATA_PATH.joinpath(f"").glob("*")
        if Path(paths).is_dir()
    ]
    for dataset_id in dataset_folders:
        available_target_variables = {
            var_path.stem.split("_")[1]: var_path
            for var_path in DATA_PATH.joinpath(f"{dataset_id}/").glob("automl*")
            if var_path.joinpath("leaderboard.csv").exists()
        }
        dict_dataset_mljar[dataset_id] = generate_mljar_model_tables(
            available_target_variables.values()
        )
    return dict_dataset_mljar


MLJAR_INFO_DICT = get_mljar_info()
