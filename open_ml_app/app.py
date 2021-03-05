from typing import Union, Optional

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

load_dotenv(verbose=True)

from utils import add_nb_features_category, add_nb_lines_category, NB_FEATURES_CATEGORIES, NB_LINES_CATEGORIES

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "FODML"

server = app.server
app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("assets/data").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath("open_data_ml_datasets.csv"))

task_list = df["task"].unique()
nb_features_bins = list(NB_FEATURES_CATEGORIES.keys())
nb_lines_bins = list(NB_LINES_CATEGORIES.keys())
topic_list = df["topic"].unique()

add_nb_features_category(df)
add_nb_lines_category(df)


# Read datasets sqlite db
# if not os.getenv("DATASETS_DB"):
#     raise FileExistsError("Could not found the datasets DB file! Set a path"
#                           "in the DATASETS_DB env var in .env file!")
# else:
#     DATASET_DB_PATH = os.getenv("DATASETS_DB")
#     DATASET_DB = SqliteDict(DATASET_DB_PATH, autocommit=True)


# Register all departments for callbacks
# all_departments = df["Department"].unique().tolist()
# wait_time_inputs = [
#     Input((i + "_wait_time_graph"), "selectedData") for i in all_departments
# ]
# score_inputs = [Input((i + "_score_graph"), "selectedData") for i in all_departments]


def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("French Open Datasets for ML (FODML)"),
            html.H3("Welcome to the FODML Repository"),
            html.Div(
                id="intro",
                children=["Explore French Open Datasets", html.A(" from data.gouv.fr"),
                          " by task, number of features, number of examples, and topic."
                          " Click on the chosen dataset to visualize its properties and its possible use cases."],
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Task"),
            dcc.Checklist(
                id="task-select",
                options=[{"label": i, "value": i} for i in task_list],
                value=task_list,
            ),
            html.Br(),
            html.P("Select Number of Features"),
            dcc.Checklist(
                id="features-select",
                options=[{"label": i, "value": i} for i in nb_features_bins],
                value=nb_features_bins,
            ),
            html.Br(),
            html.P("Select Number of Lines"),
            dcc.Checklist(
                id="lines-select",
                options=[{"label": i, "value": i} for i in nb_lines_bins],
                value=nb_lines_bins,
            ),
            html.Br(),
            html.P("Select Topic"),
            dcc.Dropdown(
                id="topic-select",
                options=[{"label": i, "value": i} for i in topic_list],
                multi=True,
                value=topic_list,
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
        style={"width": "100%"}
    )


app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="three columns",
            children=[description_card(), generate_control_card()]
                     + [
                         html.Div(
                             ["initial child"], id="output-clientside", style={"display": "none"}
                         )
                     ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="nine columns",
            children=[
                html.Div(id="dataset-card-div")
            ],
        ),
    ],
)


def generate_kpi_card(title: str, value: Union[int, str], color: Optional = None):
    dataset_kpi_card = dbc.Card(
        [
            dbc.CardHeader(html.B(title), className="card-title", style={"textAlign": "center"}),
            dbc.CardBody(
                [
                    # html.H5(title, className="card-title"),
                    html.P(value, className="card-text", style={"textAlign": "center"}),
                ]
            )
        ],
        color="primary" if not color else color, outline=True, style={"width": "10rem"}
    )
    return dataset_kpi_card


def generate_dataset_block(tasks, features, lines, topics, reset_click):
    chosen_tasks_df = df[df.task.isin(tasks)]
    chosen_features_df = chosen_tasks_df[chosen_tasks_df.nb_features_cat.isin(features)]
    chosen_lines_df = chosen_features_df[chosen_features_df.nb_lines_cat.isin(lines)]
    chosen_topics_df = chosen_lines_df[chosen_lines_df.topic.isin(topics)]
    cards_list = []

    for index, dataset in chosen_topics_df.iterrows():
        # get all required info
        dataset_id = dataset.resource_id
        dataset_title = dataset.title
        dataset_description = dataset.description
        dataset_task = dataset.task
        dataset_topic = dataset.topic
        dataset_label = dataset.label
        # descriptive stats
        dataset_nb_lines = dataset.nb_lines
        dataset_nb_features = dataset.nb_features
        dataset_missing_cells_pct = dataset.missing_cells_pct
        dataset_profile_url = dataset.profile_url


        # machine learning
        dataset_target_variable = dataset.target_variable
        dataset_model_metric = dataset.model_metric
        dataset_best_value = dataset.best_value
        dataset_best_model = dataset.best_model
        # resources

        dataset_automl_url = dataset.automl_url
        dataset_pprofiling_url = dataset.profile_url
        dataset_dict_data = dataset.dict_url

        # dataset_etalab_xp_url = dataset.etalab_xp_url
        main_dataset_card = html.Div(dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(
                            [
                                f"{dataset_title}",
                                dbc.Badge(dataset_task, color="dark", pill=True, style={"marginLeft": "20px"}),
                                dbc.Badge(dataset_topic, color="info", pill=True, className="ml-1")
                            ],
                            className="card-title"),
                        html.P(
                            f"{dataset_description}",
                            className="card-text",
                        ),
                        dbc.CardGroup([
                            # profiling
                            generate_kpi_card("Features", dataset_nb_features),
                            generate_kpi_card("Lines", dataset_nb_lines),
                            generate_kpi_card("Missing Cells", f"{dataset_missing_cells_pct:.2f} %"),
                            # models
                            generate_kpi_card("Target Var", dataset_target_variable, color="info"),
                            generate_kpi_card("Best Model", dataset_best_model, color="info"),
                            generate_kpi_card("Metric", dataset_model_metric, color="info"),
                            generate_kpi_card("Best Perf", f"{dataset_best_value:.2f}", color="info"),


                            # dbc.Card(dbc.CardBody(
                            #     dbc.Button("Pandas Profile", href=dataset_profile_url, external_link=True,
                            #                target='_blank', size="lg", color="primary")
                            # ), className='align-self-center'),
                            #
                            # dbc.Card(dbc.CardBody(
                            #     dbc.Button("AutoML Profile", href=dataset_automl_url, external_link=True,
                            #                target="_blank", size="lg", color="info")
                            # ), className='align-self-center'),
                            #

                        ], style={"marginTop": "20px"}
                        ),
                        html.Br(),
                        dbc.CardFooter([
                            html.H5("Resources:"),
                            dbc.Badge("Descriptive Profile", href=dataset_pprofiling_url,
                                      target="_blank", color="dark", pill=True),
                            dbc.Badge("AutoML Profile", href=dataset_automl_url,
                                      color="teal", pill=True, className="ml-2"),
                            dbc.Badge("Data Dictionary", href="www.google",
                                      color="info", pill=True, className="ml-2"),

                        ], style={"font-family": "Acumin", "font-size": "20px"})
                    ]
                ),
            ],
            # style={"width": "rem"}
        ),
            style={"marginTop": "20px"}
        )
        # dataset_external_xp_url = dataset.external_xp_url


        # card = html.Div([row_1], className="dataset-card")
        cards_list.append(main_dataset_card)

    return cards_list


@app.callback(
    Output("dataset-card-div", "children"),
    [
        Input("task-select", "value"),
        Input("features-select", "value"),
        Input("lines-select", "value"),
        Input("topic-select", "value"),
        Input("reset-btn", "n_clicks"),
    ],
)
def update_dataset_block(task, feature, line, topic, reset_click):
    reset = False
    # Find which one has been triggered
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn":
            reset = True
    # Return to original hm(no colored annotation) by resetting
    return generate_dataset_block(task, feature, line, topic, reset_click)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
