import re
import unicodedata
from typing import Dict, Tuple, Union, Optional

import dash_bootstrap_components as dbc
import dash_html_components as html

import pandas as pd
import requests

NB_FEATURES_CATEGORIES = {
    "<10": (1, 10),
    ">=10<100": (10, 100),
    ">=100<500": (100, 500),
    ">=500": (500, 1e100)
}

NB_LINES_CATEGORIES = {
    "<100": (1, 100),
    ">=100<1000": (100, 1000),
    ">=1000<5000": (1000, 5000),
    ">=5000<10000": (5000, 10000),
    ">=10000": (10000, 1e100)
}
DATASET_COLUMNS = {"Task": 'task', "Topic": 'topic', "Columns": 'nb_features', "Lines": 'nb_lines',
                   "Validated": "is_validated"}

DATASET_NAME = {'Name': 'title'}


def get_category(categories_dict: Dict[str, Tuple[int, int]], value: int):
    for cat, (min_val, max_val) in categories_dict.items():
        if min_val <= value < max_val:
            return cat
    else:
        return None


def get_dataset_info(dataset: Union[pd.DataFrame, pd.Series]):
    # get all required info
    dataset_dict = dataset.to_dict()
    return dataset_dict


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


def add_nb_features_category(df: pd.DataFrame):
    df["nb_features_cat"] = df.nb_features.apply(lambda x: get_category(NB_FEATURES_CATEGORIES, x))


def add_nb_lines_category(df: pd.DataFrame):
    df["nb_lines_cat"] = df.nb_lines.apply(lambda x: get_category(NB_LINES_CATEGORIES, x))


def generate_kpi_card(title: str, value: Union[int, str], color: Optional = None):
    dataset_kpi_card = dbc.Card(
        [
            dbc.CardHeader(html.B(title), style={"height": "50%", "textAlign": "center", "font-family": "Acumin"}),
            dbc.CardBody(
                [
                    html.P(value, style={"height": "100%", "textAlign": "center", "font-family": "AcuminL"}),

                ],

            )
        ],
        color="primary" if not color else color, outline=True,
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
    Filter reuses and return only those contain some machine learning-y term in the description
    :param reuses_dict:
    :return:
    """
    list_ml_terms = ["deep learning", "apprentissage automatique", "machine learning", "classification",
                     "data science", "prédire"]
    ml_reuses = []
    for reuse in reuses_dict["data"]:
        if not reuse["featured"]:
            # reuse not featured, continue
            continue
        reuse_ml_terms = [term in reuse["description"].lower()
                          for term in list_ml_terms]
        if not any(reuse_ml_terms):
            # no ml terms, continue
            continue
        ml_reuses.append(reuse)

    return ml_reuses


def generate_badge(title: str, url: str, background_color: str, font_color: str = "#333333",
                   new_tab: bool = False):
    if pd.isna(url):
        title = f"{title} not available 😞"
        badge = dbc.Badge(title, style={"backgroundColor": background_color, "color": font_color},
                          pill=True, className="ml-2")
    else:
        badge = dbc.Badge(title, href=url,
                          target="_blank" if new_tab else False,
                          style={"backgroundColor": background_color, "color": font_color},
                          pill=True, className="ml-2", external_link=True)
    return badge
