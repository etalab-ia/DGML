import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import os
print(os.getcwd())
from apps.dataset_page import generate_dataset_page
from apps.utils import generate_kpi_card, DATASET_COLUMNS

load_dotenv(verbose=True)

from apps.utils import add_nb_features_category, add_nb_lines_category, NB_FEATURES_CATEGORIES, NB_LINES_CATEGORIES, \
    get_dataset_info

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    url_base_pathname="/openml/",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "FODML"

server = app.server
# app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("assets/datasets").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath("open_data_ml_datasets.csv"))

task_list = df["task"].unique()
nb_features_bins = list(NB_FEATURES_CATEGORIES.keys())
nb_lines_bins = list(NB_LINES_CATEGORIES.keys())
topic_list = df["topic"].unique()

add_nb_features_category(df)
add_nb_lines_category(df)


def description_card():
    """
    The section dealing with the description of the website
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("French Open Datasets for ML (FODML)"),
            html.H3("Welcome to the FODML Repository"),
            html.Div(
                id="intro",
                children=["Explore French Open Datasets from",
                          html.A(" data.gouv.fr (DGF)", href="https://www.data.gouv.fr",
                                 target="_blank"),
                          "by task, number of features, number of examples, and topic."
                          "Click on the chosen dataset to visualize its descriptive summary and the AutoMl report."],
            ),
        ],
    )


def generate_control_card():
    """
    The section that presents the control filtering options
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
            html.P("Sort by:"),
            dcc.Dropdown(
                id="sort-by",
                options=[{"label": i, "value": i} for i in DATASET_COLUMNS],
                value="Task"
            ),
            html.Br(),
            dcc.RadioItems(
                id="sort-by-order",
                options=[{"label": i, "value": i} for i in ["Ascending", "Descending"]],
                value="Ascending",
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),

        ],
        style={"width": "100%"}
    )


app_layout = html.Div(
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

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.layout = url_bar_and_content_div


# app.validation_layout = html.Div([
#     url_bar_and_content_div,
#     generate_dataset_page("test")
# ])


def generate_dataset_block(tasks, features, lines, topics, reset_click):
    chosen_tasks_df = df[df.task.isin(tasks)]
    chosen_features_df = chosen_tasks_df[chosen_tasks_df.nb_features_cat.isin(features)]
    chosen_lines_df = chosen_features_df[chosen_features_df.nb_lines_cat.isin(lines)]
    chosen_topics_df = chosen_lines_df[chosen_lines_df.topic.isin(topics)]
    cards_list = []

    for index, dataset_row in chosen_topics_df.iterrows():
        dataset_dict = get_dataset_info(dataset_row)

        main_dataset_card = html.Div(dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(
                            [
                                dcc.Link(f"{dataset_dict['title']}", href=f"{app.config['url_base_pathname']}"
                                                                          f"datasets/{dataset_dict['dgf_resource_id']}"),
                            ],
                            className="card-title"),
                        # html.P(
                        #     f"{dataset_dict['description']}",
                        #     style={"font-family": "AcuminL"},
                        # ),
                        dbc.CardDeck([
                            # profiling
                            generate_kpi_card("Task", f"{dataset_dict['task']}"),
                            generate_kpi_card("Topic", f"{dataset_dict['topic']}"),
                            generate_kpi_card("Columns", dataset_dict['nb_features']),
                            generate_kpi_card("Lines", dataset_dict['nb_lines']),
                            # generate_kpi_card("Missing Cells", f"{dataset_dict['missing_cells_pct']:.2f} %")
                        ]),
                    ]
                ),
            ],
        ),
            style={"marginTop": "20px"}
        )

        cards_list.append(main_dataset_card)

    return cards_list


# Index callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == app.config['url_base_pathname']:
        return app_layout
    else:
        return generate_dataset_page(pathname, df)


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
    app.run_server(debug=True, port=8050)
