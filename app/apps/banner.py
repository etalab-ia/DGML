import base64

import dash_html_components as html


def get_banner():
    banner = html.Div(
        id="app-page-header",
        children=[
            html.A(
                id="dashbio-logo",
                children=[html.Img(src="./assets/MarianneLogo-3-90x57.png")],
                href="https://www.etalab.gouv.fr/",
            ),
            html.H2(
                ["Data Gouv pour le Machine Learning (DGML)", html.Sup("β")],
                style={"fontFamily": "Acumin"},
            ),
            html.A(
                id="gh-link",
                children=["Voir sur Github"],
                href="https://github.com/etalab-ia/dgml",
                style={"color": "black", "border": "solid 1px black"},
                target="_blank",
            ),
            html.Img(
                src="data:image/png;base64,{}".format(
                    base64.b64encode(
                        open("./assets/GitHub-Mark-64px.png", "rb").read()
                    ).decode()
                )
            ),
        ],
    )
    return banner
