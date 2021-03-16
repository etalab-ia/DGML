import pathlib
from typing import Dict

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# from open_ml_app.main import DATA_PATH
# from open_ml_app.main import DATA_PATH
from open_ml_app.utils import get_dataset_info, generate_kpi_card, get_reuses, filter_reuses, generate_badge
import dash_table

# Path
BASE_PATH = pathlib.Path(__file__).parent.parent.resolve()
DATA_PATH = BASE_PATH.joinpath("assets/datasets").resolve()


def generate_reuses_cards(resuses_dict: Dict):
    ml_reuses_dict = filter_reuses(resuses_dict)
    if not ml_reuses_dict:
        return
    list_cards = []
    for reuse in ml_reuses_dict:
        reuse_card = dbc.Card(
            [
                dbc.CardImg(src=reuse["image_thumbnail"], top=True),
                dbc.CardBody(
                    [
                        html.H4(reuse["title"], className="card-title"),
                        html.P(f"{reuse['description'][:100]}[...]", className="card-text",
                        ),
                        dbc.Button("See reuse", color="primary", href=reuse["url"], target="_blank"),
                    ]
                ),
            ],

        )
        list_cards.append(reuse_card)
    return dbc.CardDeck(list_cards, className="w-25")


def generate_table(dataset_id: str, table_type: str = "dict_data.csv"):
    dictionary_path = DATA_PATH.joinpath(f"resources/{dataset_id}/{table_type}")
    if not dictionary_path.exists():
        html_table = html.H5("Data dictionary preview not available")
    else:
        table_df = pd.read_csv(dictionary_path, sep="\t")
        if "mljar_profile" in table_type:
            # add links to mljar table
            table_df["name"] = table_df[["name", "url"]].apply(lambda row: html.A(html.P(row["name"]), href=row["url"],
                                                                                  target="_blank"), axis=1)
            table_df = table_df.drop(["url"], axis=1)
        html_table = html.Div(dbc.Table.from_dataframe(table_df, striped=True, size="sm", borderless=True),
                              style={"height": "300px", "overflow": 'auto'})
    return html_table


def generate_dataset_page(dataset_url: str, datasets_df: pd.DataFrame):
    dataset_id = dataset_url.split("/")[-1]
    dataset_row = datasets_df[datasets_df["dgf_resource_id"] == dataset_id].iloc[0]
    if dataset_row.empty:
        return dbc.Container(html.H2("This dataset was not found in our catalog."))
    dataset_dict = get_dataset_info(dataset_row)
    dictionary_table = generate_table(dataset_dict["dgf_resource_id"], table_type="dict_data.csv")
    mljar_table = generate_table(dataset_dict["dgf_resource_id"], table_type="mljar_profile.csv")

    container = dbc.Container([
        generate_badge("Go back", url="/openml/", background_color="red"),
        html.Title("FODML"),
        html.H2(dataset_dict["title"]),
        html.P(dataset_dict["description"]),
        html.P(generate_badge("Dataset in data.gouv.fr", url=dataset_dict['dgf_dataset_url'], background_color="#5783B7")),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Data Dictionary"),
        dictionary_table,
        html.P(generate_badge("Full Data Dictionary", url=dataset_dict['dict_url'], background_color="#F49390")),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Descriptive Summary"),

        dbc.CardDeck(
            [
                generate_kpi_card("Features", dataset_dict['nb_features']),
                generate_kpi_card("Lines", dataset_dict['nb_lines']),
                generate_kpi_card("Missing Cells", f"{dataset_dict['missing_cells_pct']:.2f} %"),
                generate_kpi_card("Continous", 29),
                generate_kpi_card("Categorical", 2),
                generate_kpi_card("High Cardinality", 10),
                generate_kpi_card("High Correlation", 10),
                # generate_kpi_card("Skewed", 10),
            ]
        ),
        generate_badge("Full Descriptive Profile", url=dataset_dict['profile_url'], background_color="#A4B494"),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("AutoML Summary"),
        mljar_table,
        generate_badge("Full AutoML Profile", url=dataset_dict['automl_url'], background_color="#EAB464"),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("ML Reuses"),
        html.Hr(style={"marginBottom": "20px"}),
        generate_reuses_cards(get_reuses(dataset_dict["dgf_dataset_id"])),
        html.H3("Load Data"),
        html.Hr(style={"marginBottom": "20px"}),
    ])

    return container
