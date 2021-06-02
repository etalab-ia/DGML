import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

from apps.dataset_page import generate_dataset_page
from apps.utils import generate_kpi_card, DATASET_COLUMNS, generate_badge
from open_ml_app.apps.banner import get_banner

load_dotenv(verbose=True)

from apps.utils import add_nb_features_category, add_nb_lines_category, NB_FEATURES_CATEGORIES, NB_LINES_CATEGORIES, \
    get_dataset_info

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    url_base_pathname="/dgml/",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "DGML"

server = app.server
# app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("assets/datasets").resolve()

# Read data
encoded_image_validated = base64.b64encode(open(DATA_PATH.parent.joinpath("quality.png"), 'rb').read()).decode()
df = pd.read_csv(DATA_PATH.joinpath("open_data_ml_datasets.csv"))

task_list = df["task"].unique()
nb_features_bins = list(NB_FEATURES_CATEGORIES.keys())
nb_lines_bins = list(NB_LINES_CATEGORIES.keys())
topic_list = df["topic"].unique()

add_nb_features_category(df)
add_nb_lines_category(df)


def check_if_resource(df):
    dataset_folders = [pathlib.Path(paths).stem for paths in DATA_PATH.joinpath(f"resources/").glob('*')]
    filtered_df = df[df['dgf_resource_id'].isin(dataset_folders)]
    return filtered_df


df = check_if_resource(df)


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
                algorithm_urls = [html.A(html.P(n), href=tar_var_path.joinpath(f"{n}/README.html").as_posix(),
                                         target="_blank")
                                  for n in table_df.name]
                table_df["name"] = algorithm_urls
                html_table = dbc.Table.from_dataframe(table_df, striped=True, size="sm", borderless=True)
            dict_target_vars[tar_var_path.stem.split("_")[1]] = (
                html_table, display_table_path.parent.joinpath("README.html"))
        return dict_target_vars

    dict_dataset_mljar = {}
    dataset_folders = [pathlib.Path(paths).stem for paths in DATA_PATH.joinpath(f"resources/").glob('*')]
    for dataset_id in dataset_folders:
        available_target_variables = {var_path.stem.split("_")[1]: var_path for var_path in
                                      DATA_PATH.joinpath(f"resources/{dataset_id}/").glob("automl*")
                                      if var_path.joinpath("leaderboard.csv").exists()}
        dict_dataset_mljar[dataset_id] = generate_mljar_model_tables(available_target_variables.values())
    return dict_dataset_mljar


MLJAR_INFO_DICT = get_mljar_info()


def description_card():
    """
    The section dealing with the description of the website
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Data Gouv pour le Machine Learning (DGML)"),
            html.H3("Bienvenue sur DGML!"),
            html.Div(
                id="intro",
                children=["Data Gouv pour le Machine Learning (DGML) est le catalogue des jeux de données de",
                          html.A(" data.gouv.fr", href="https://www.data.gouv.fr",
                                 target="_blank"),
                          " pour le Machine Learning. ",
                          html.Br(),

                          "Cliquez sur un jeu de données pour voir: ses statistiques, les résultats ",
                          "de l'entraînement et test automatique d'algorithmes de Machine Learning sur les données, ainsi que des ",
                          "exemples de code et des réutilisations qui vont vous guider dans la mise en oeuvre de votre modèle de Machine Learning avec ces données.",
                          html.Br(), "DGML a été développé par le ",
                          html.A("Lab IA d'Etalab: ",
                                 href="https://www.etalab.gouv.fr/datasciences-et-intelligence-artificielle",
                                 target="_blank"),
                          "visitez notre Github pour en savoir plus sur le projet, sur le choix des jeux de données, pour mieux comprendre les résultats ou nous contacter."],
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
            html.P("Tâche"),
            dcc.Checklist(
                id="task-select",
                options=[{"label": f" {i}", "value": i} for i in task_list],
                value=task_list,
            ),
            html.Br(),
            html.P("Nombre de colonnes"),
            dcc.Checklist(
                id="features-select",
                options=[{"label": f" {i}", "value": i} for i in nb_features_bins],
                value=nb_features_bins,
            ),
            html.Br(),
            html.P("Nombre de lignes"),
            dcc.Checklist(
                id="lines-select",
                options=[{"label": f" {i}", "value": i} for i in nb_lines_bins],
                value=nb_lines_bins,
            ),
            html.Br(),
            html.P("Validation"),
            dcc.Checklist(
                id="valid-select",
                options=[{'label': f" {l}", "value": l} for l in ["Sélectionné", "Automatique"]],
                value=["Sélectionné", "Automatique"],
            ),
            html.Br(),
            html.P("Thème"),
            dcc.Dropdown(
                id="topic-select",
                options=[{"label": f" {i}", "value": i} for i in topic_list],
                multi=True,
                value=topic_list,
                clearable=False
            ),
            html.Br(),
            html.P("Filtrer par:"),
            dcc.Dropdown(
                id="sort-by",
                options=[{"label": f" {i}", "value": i} for i in DATASET_COLUMNS],
                value="Validé",
                clearable=False
            ),
            html.Br(),
            dcc.RadioItems(
                id="sort-by-order",
                options=[{"label": i, "value": i} for i in ["Ascendant", "Descendant"]],
                value="Ascendant",
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0, hidden=True),
            ),

        ],
        style={"width": "100%"}
    )


app_layout = html.Div(
    id="app-container",
    children=[
        # Banner
        get_banner(),
        html.Div(id='app-page-content',
                 children=[
                     # Left column
                     html.Div(
                         id="left-column",
                         className="four columns",
                         children=[description_card(), generate_control_card()]
                     ),
                     # Right column
                     html.Div(
                         id="right-column",
                         className="seven columns",
                         children=[
                             html.Div(id="dataset-card-div")
                         ],
                     )
                 ])
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


def generate_dataset_block(tasks, features, lines, valid, topics, sort_by, sort_order, reset_click):
    curated_dict = {"Sélectionné": True, "Automatique": False}
    chosen_tasks_df = df[df.task.isin(tasks)]
    chosen_features_df = chosen_tasks_df[chosen_tasks_df.nb_features_cat.isin(features)]
    chosen_lines_df = chosen_features_df[chosen_features_df.nb_lines_cat.isin(lines)]
    chosen_topics_df = chosen_lines_df[chosen_lines_df.topic.isin(topics)]
    chosen_validation = chosen_topics_df[chosen_topics_df["is_validated"].isin([curated_dict[v] for v in valid])]
    chosen_sort_by_df = chosen_validation.sort_values(by=DATASET_COLUMNS[sort_by],
                                                      ascending=True if sort_order == 'Ascendant' and sort_by != "Validé"
                                                      else False)
    cards_list = []

    for index, dataset_row in chosen_sort_by_df.iterrows():
        dataset_dict = get_dataset_info(dataset_row)

        main_dataset_card = html.Div(dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(
                            [
                                dcc.Link(f"{dataset_dict['title']}", href=f"{app.config['url_base_pathname']}"
                                                                          f"{dataset_dict['dgf_resource_id']}"),
                                html.Img(id="validated-img",
                                         src="data:image/png;base64,{}".format(encoded_image_validated),
                                         style={'height': '3%', 'width': '3%', "float": "right"},
                                         hidden=not dataset_dict["is_validated"]),
                                dbc.Tooltip("Ce jeu de données a été sélectionné et analysé manuellement.",
                                            target="validated-img",
                                            style={'font-size': 13}
                                            )
                            ],
                            className="card-title"),
                        dbc.CardDeck([
                            # profiling
                            generate_kpi_card("Tâche proposée", f"{dataset_dict['task']}"),
                            generate_kpi_card("Thème", f"{dataset_dict['topic']}"),
                            generate_kpi_card("Colonnes", dataset_dict['nb_features']),
                            generate_kpi_card("Lignes", dataset_dict['nb_lines']),
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


#
@app.callback([Output('mljar-div', 'children'),
               Output('mljar-link-badge', 'children')],
              [Input('target-var-model-select', 'value'),
               Input('url', 'pathname')])
def update_automl_model(target_var, pathname):
    if pathname == app.config['url_base_pathname']:
        return None, None
    dataset_id = pathname.split("/")[-1]
    if dataset_id not in MLJAR_INFO_DICT or target_var not in MLJAR_INFO_DICT[dataset_id]:
        return html.P("On n'a pas des modèles AutoML pour ce dataset"), None
    models_table, mljlar_profile_url = MLJAR_INFO_DICT[dataset_id][target_var]
    mljar_profile_badge = generate_badge("Full Mljar Profile", url=mljlar_profile_url.as_posix(),
                                         background_color="#6d92ad",
                                         new_tab=True)

    return models_table, mljar_profile_badge


@app.callback(
    Output("dataset-card-div", "children"),
    [
        Input("task-select", "value"),
        Input("features-select", "value"),
        Input("lines-select", "value"),
        Input("valid-select", "value"),
        Input("topic-select", "value"),
        Input("sort-by", "value"),
        Input("sort-by-order", "value"),
        Input("reset-btn", "n_clicks"),
    ],
)
def update_dataset_block(task, feature, line, valid, topic, sort_by, sort_order, reset_click):
    reset = False
    # Find which one has been triggered
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn":
            reset = True
    # Return to original hm(no colored annotation) by resetting
    return generate_dataset_block(task, feature, line, valid, topic, sort_by, sort_order, reset_click)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
