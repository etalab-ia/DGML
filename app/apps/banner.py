import base64

import dash_html_components as html


def get_banner():
    banner = html.Div(
        id="app-page-header",
        children=[
            html.A(
                id="marianne-logo",
                children=[html.Img(src="https://www.etalab.gouv.fr/wp-content/uploads/2019/04/cropped-MarianneLogo-3"
                                       "-90x57.png")],
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
                        open("./app/assets/GitHub-Mark-64px.png", "rb").read()
                    ).decode()
                )
            ),
        ],
    )
    return banner
