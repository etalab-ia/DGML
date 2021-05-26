import base64
import glob
from typing import Dict

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pathlib import Path
from .utils import get_dataset_info, generate_kpi_card, get_reuses, filter_reuses, generate_badge

DATA_PATH = Path("./assets/datasets")
encoded_image_validated = base64.b64encode(open(DATA_PATH.parent.joinpath("quality.png"), 'rb').read()).decode()


def get_available_target_variables():
    pass


def generate_etalab_cards(experiment_path: Path):
    notebook_html = [Path(p) for p in glob.glob(experiment_path.as_posix() + "/*.html")]

    if not notebook_html:
        return html.P("There are no experiments with this dataset 😞")
    list_cards = []
    for notebook in notebook_html:
        reuse_card = dbc.Card(
            [
                dbc.CardImg(src="./assets/jupyter_logo.png", top=True),
                dbc.CardBody(
                    [
                        html.H4(notebook.stem, className="card-title"),
                        html.P("A complete ML pipeline"
                               ),
                        dbc.Button("See experiments", color="primary", href=notebook.as_posix(), target="_blank",
                                   external_link=True),
                    ]
                ),
            ],

        )
        list_cards.append(reuse_card)
    return dbc.CardDeck(list_cards, className="w-25")


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
        html_table = html.H5("Data dictionary preview not available")
    else:
        table_df = pd.read_csv(display_table_path)
        html_table = html.Div(dbc.Table.from_dataframe(table_df, striped=True, size="sm", borderless=True),
                              style={"height": "300px", "overflow": 'auto'})
    return html_table


def generate_stats_df(dataset_id: str, table_type: str = "statistics_summary.csv"):
    display_stats_path = DATA_PATH.joinpath(f"resources/{dataset_id}/{table_type}")
    if not display_stats_path.exists():
        statistics_df = html.H5("Descriptive summary not available.")
    else:
        statistics_df = pd.read_csv(display_stats_path)
    return statistics_df


def generate_dataset_page(dataset_url: str, datasets_df: pd.DataFrame):
    dataset_id = dataset_url.split("/")[-1]
    dataset_row = datasets_df[datasets_df["dgf_resource_id"] == dataset_id].iloc[0]
    if dataset_row.empty:
        return dbc.Container(html.H2("This dataset was not found in our catalog."))
    dataset_dict = get_dataset_info(dataset_row)
    dictionary_table = generate_table(dataset_dict["dgf_resource_id"], table_type="dict_data.csv")

    target_vars = [var_path.stem.split("_")[1] for var_path in
                   DATA_PATH.joinpath(f"resources/{dataset_id}/").glob("automl*")]
    statistics_df = generate_stats_df(dataset_dict["dgf_resource_id"], table_type="statistics_summary.csv")
    pandas_profile_url = DATA_PATH.joinpath(f"resources/{dataset_id}/{dataset_id}_pandas_profile.html")
    experiments_url = DATA_PATH.joinpath(f"resources/{dataset_id}/our_experiments/")
    container = dbc.Container([
        html.H5(generate_badge("Go back", url="/dgml/", background_color="#cadae6", new_tab=False)),
        html.Title("DGML: Data Gouv for Machine Learning"),
        html.H2([dataset_dict["title"],
                 html.Img(id="validated-img2",
                          src="data:image/png;base64,{}".format(encoded_image_validated),
                          style={'height': '3%', 'width': '3%', "float": "right"},
                          hidden=not dataset_dict["is_validated"]),
                 dbc.Tooltip("This dataset has been selected and analysed manually.",
                             target="validated-img2",
                             style={'font-size': 13}
                             )
                 ]),
        html.P(dataset_dict["description"]),
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
            ]
        ),
        html.H4(
            generate_badge("Full Pandas Profile", url=pandas_profile_url.as_posix(), background_color="#6d92ad")),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("AutoML Summary"),
        html.Div([html.P(children=f"Models trained for "),
                  dcc.Dropdown(
                      id="task-model-select",
                      options=[{"label": i, "value": i} for i in ["Classification", "Regression"]],
                      multi=False,
                      value="Classification",
                      clearable=False,
                      style={"min-width": "120px", "marginLeft": "3px"}
                  ),
                  html.P("using ", style={"marginLeft": "6px"}),
                  dcc.Dropdown(
                      id="target-var-model-select",
                      options=[{"label": i, "value": i} for i in target_vars],
                      multi=False,
                      value=target_vars[0],
                      clearable=False,
                      style={"min-width": "300px", "marginLeft": "3px"}

                  ),
                  html.P("as target variable.", style={"marginLeft": "6px"})

                  ], style={"display": 'flex'}),
        html.Div(id="mljar-div", style={"height": "300px", "overflow": 'auto'}),
        html.H4(id="mljar-link-badge", children=None),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Machine Learning Reuses (data.gouv.fr)"),
        generate_reuses_cards(get_reuses(dataset_dict["dgf_dataset_id"])),
        html.Hr(style={"marginBottom": "20px"}),
        html.H3("Our Experiments"),
        # html.P("Check out our experiments on this dataset : "),
        generate_etalab_cards(experiments_url),
        # html.H4(generate_badge("See notebook", url=dataset_dict['etalab_xp_url'], background_color="#cadae6")),
        html.Hr(style={"marginBottom": "20px"}),
        # html.H3("Load Data"),
        # html.Hr(style={"marginBottom": "20px"}),
    ])

    return container
