import dash
from dash import html
import dash_bootstrap_components as dbc

from info import info_tab
from dashboard_tabs import CreateDashboardTabs

app = dash.Dash(external_stylesheets=[dbc.themes.SIMPLEX]) # MATERIA JOURNAL MORPH SANDSTONE SIMPLEX 
app.title = "SG Hawkers"

server = app.server

def update_layout():
    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Singapore Hawker Centre Dashboard",
                                style={
                                    "font-size": 30,
                                    "font-weight": "bold",
                                    },
                            ),
                        ),
                    ],
                ),
            ),
        ],
        color="#ed2e38", # "dark",
        dark=True,
        style={"border":"none"},
    )

    hc_map_tab, hawker_table_tab = CreateDashboardTabs()
    tabs = dbc.Tabs(
        [
        dbc.Tab(hc_map_tab, id="label_tab1", label="Hawker Centre Map",), 
        dbc.Tab(hawker_table_tab, id = "label_tab3", label = "Hawker Centre Data Table",), 
        dbc.Tab(info_tab, id="label_tab5", label="Additional Information",), 
        ],
        style = {
            "font-size": 15, 
            "font-weight": "bold",
            },
    )

    layout = html.Div(
        [
            navbar,
            tabs,
        ],
        style={}
    )
    return layout

app.layout = update_layout


if __name__ == "__main__":
    app.run_server(debug=True, host = "0.0.0.0", port=80, use_reloader=True)
