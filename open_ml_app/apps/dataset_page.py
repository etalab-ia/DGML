from typing import Dict

import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from pathlib import Path
from .utils import get_dataset_info, generate_kpi_card, get_reuses, filter_reuses, generate_badge, slugify

# Path
DATA_PATH = Path("./assets/datasets")

def generate_reuses_cards(resuses_dict: Dict):
    ml_reuses_dict = filter_reuses(resuses_dict)
    if not ml_reuses_dict:
        return html.P("There are no data science reuses for this dataset 😞")
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
    display_table_path = DATA_PATH.joinpath(f"resources/{dataset_id}/{table_type}")
    if not display_table_path.exists():
        if "dict_data" in table_type:
            html_table = html.H5("Data dictionary preview not available")
        if "leaderboard" in table_type:
            html_table = html.H5("MLJAR profile preview not available")
    else:
        table_df = pd.read_csv(display_table_path)
        if "leaderboard" in table_type:
            # add links to mljar table
            table_df["name"] = table_df[["name", "url"]].apply(lambda row: html.A(html.P(row["name"]), href=row["url"],
                                                                                  target="_blank"), axis=1)
            table_df = table_df.drop(["url"], axis=1)
        html_table = html.Div(dbc.Table.from_dataframe(table_df, striped=True, size="sm", borderless=True),
                              style={"height": "300px", "overflow": 'auto'})
    return html_table


def generate_mljar_table(dataset_id: str, target_variable: str, base_url: str):
    display_table_path = DATA_PATH.joinpath(f"resources/{dataset_id}/automl_{slugify(target_variable)}/leaderboard.csv")
    experiment_path = display_table_path.parent
    if not display_table_path.exists():
        html_table = html.H5("MLJAR profile preview not available")
    else:
        table_df = pd.read_csv(display_table_path)
        table_df["metric_value"] = table_df["metric_value"].round(decimals=3)
        algorithm_urls = [html.A(html.P(n), href=experiment_path.joinpath(f"{n}/README.html").as_posix(),
                                 target="_blank")
                          for n in table_df.name]
        # table_df["name"] = table_df[["name", "url"]].apply(lambda row: html.A(html.P(row["name"]), href=row["url"],
        #                                                                       target="_blank"), axis=1)
        # table_df = table_df.drop(["url"], axis=1)
        table_df["name"] = algorithm_urls
        html_table = html.Div(dbc.Table.from_dataframe(table_df, striped=True, size="sm", borderless=True),
                              style={"height": "300px", "overflow": 'auto'})
    return html_table


def generate_stats_df(dataset_id: str, table_type: str = "statistics_summary.csv"):
    display_stats_path = DATA_PATH.joinpath(f"resources/{dataset_id}/{table_type}")
    if not display_stats_path.exists():
        html_table = html.H5("Descriptive summary not available.")
    else:
        statistics_df = pd.read_csv(display_stats_path)
    return statistics_df


def generate_dataset_page(dataset_url: str, datasets_df: pd.DataFrame, app):
    dataset_id = dataset_url.split("/")[-1]
    dataset_row = datasets_df[datasets_df["dgf_resource_id"] == dataset_id].iloc[0]
    if dataset_row.empty:
        return dbc.Container(html.H2("This dataset was not found in our catalog."))
    dataset_dict = get_dataset_info(dataset_row)
    target_variable = dataset_row["target_variable"]
    dictionary_table = generate_table(dataset_dict["dgf_resource_id"], table_type="dict_data.csv")
    mljar_table = generate_mljar_table(dataset_dict["dgf_resource_id"],
                                       target_variable=target_variable, base_url=app.config["url_base_pathname"])
    statistics_df = generate_stats_df(dataset_dict["dgf_resource_id"], table_type="statistics_summary.csv")

    container = dbc.Container([
        # html.H4(generate_badge("Go back", url="/openml/", background_color="red")),
        html.H5(generate_badge("Go back", url="/openml/", background_color="#cadae6")),
        html.Title("FODML: French Open Data for Machine Learning"),
        html.H2([dataset_dict["title"]]),
        html.P(dataset_dict["description"]),
        # html.H4(generate_badge("Dataset in data.gouv.fr", url=dataset_dict['dgf_dataset_url'], background_color="#5783B7")),
        html.H4(
            generate_badge("Dataset in data.gouv.fr", url=dataset_dict['dgf_dataset_url'], background_color="#6d92ad")),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Data Dictionary"),
        dictionary_table,
        html.H4(generate_badge("Full Data Dictionary", url=dataset_dict['dict_url'], background_color="#6d92ad")),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Descriptive Summary"),

        dbc.CardDeck(
            [
                generate_kpi_card("Number of Columns", statistics_df['Number of variables']),
                generate_kpi_card("Number of Lines", statistics_df['Number of lines']),
                generate_kpi_card("Missing Cells",
                                  f"{round(float(statistics_df['Percentage of missing cells']), 2)} %"),
                generate_kpi_card("Numeric variables", statistics_df['Numeric']),
                generate_kpi_card("Categorical variables", statistics_df['Categorical']),
                generate_kpi_card("High Cardinality", statistics_df['High cardinality variables']),
                generate_kpi_card("High Correlation", statistics_df['High correlation variables']),
                # generate_kpi_card("Skewed", 10),
            ]
        ),
        html.H4(
            generate_badge("Full Pandas Profile", url=dataset_dict['profile_url'], background_color="#6d92ad")),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("AutoML Summary"),
        html.P(children=[f"Models trained with this dataset using the following target variable : ", html.B(dataset_dict['target_variable'])]),
        mljar_table,
        html.H4(generate_badge("Full Mljar Profile", url=dataset_dict['automl_url'], background_color="#6d92ad")),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Machine Learning Reuses (data.gouv.fr)"),
        generate_reuses_cards(get_reuses(dataset_dict["dgf_dataset_id"])),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Our Experiments"),
        html.P("Check out our experiments on this dataset : "),
        html.H4(generate_badge("See notebook", url=dataset_dict['etalab_xp_url'], background_color="#cadae6")),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Load Data"),
        html.Hr(style={"marginBottom": "20px"}),
    ])

    return container
