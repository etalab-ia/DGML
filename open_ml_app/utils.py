from typing import Dict, Tuple

import pandas as pd

NB_FEATURES_CATEGORIES = {
    "<10": (1, 10),
    ">=10<100": (10, 100),
    ">=100<500": (100, 500),
    ">=500": (500, 1e100)
}

NB_LINES_CATEGORIES = {
    "<100": (1, 100),
    ">=100<1000": (100, 1000),
    ">=1000<2000": (1000, 2000),
    ">=2000": (2000, 1e100)
}


def get_category(categories_dict: Dict[str, Tuple[int, int]], value: int):
    for cat, (min_val, max_val) in categories_dict.items():
        if min_val <= value < max_val:
            return cat
    else:
        return None


def add_nb_features_category(df: pd.DataFrame):
    df["nb_features_cat"] = df.nb_features.apply(lambda x: get_category(NB_FEATURES_CATEGORIES, x))


def add_nb_lines_category(df: pd.DataFrame):
    df["nb_lines_cat"] = df.nb_lines.apply(lambda x: get_category(NB_LINES_CATEGORIES, x))
