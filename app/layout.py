from dash import html, dash_table, dcc, Output, Input, State, ctx
import dash_leaflet as dl

def build_layout(geojson):
    print("RENDER DO MAPA")
    return html.Div([
        # Mapa + botão + caixa flutuante
        html.Div([
            # Mapa
            dl.Map(
                id="mapa",
                children=[
                    dl.TileLayer(),
                    dl.FeatureGroup([
                        dl.EditControl(
                            id="edit_control",
                            draw={"rectangle": True, "marker": False, "circle": False, "polyline": False, "polygon": False, "circlemarker": False},
                            editToolbar=False
                        )
                    ]),
                    dl.GeoJSON(
                        data=geojson,
                        cluster=True,
                        zoomToBoundsOnClick=False,
                        hideout={}
                    ),
                    dl.LayerGroup(id="selected-marker"),
                    dl.Popup(id="popup")
                ],
                style={"height": "65vh", "width": "100%"},
                center=[-19.92, -43.94],
                zoom=12
            ),
            html.Div([
                html.Button(
                    "Restaurantes Comida di Buteco",
                    id="btn-toggle-floating-table",
                    n_clicks=0,
                    style={
                        "backgroundColor": "#c4b194",
                        "color": "white",
                        "border": "none",
                        "padding": "8px 12px",
                        "borderRadius": "5px",
                        "fontFamily": "Arial",
                        "fontSize": "14px",
                        "cursor": "pointer",
                        "boxShadow": "1px 1px 5px rgba(0,0,0,0.2)"
                    }
                )
            ],
            style={
                "position": "absolute",
                "bottom": "20px",
                "right": "20px",
                "zIndex": "1000"
            }),
            html.Div([
                dash_table.DataTable(
                    id="floating-table",
                    columns=[{"name": "NOME", "id": "NOME"}],
                    data=[],
                    page_size=5,
                    style_table={
                        "maxHeight": "200px",
                        "overflowY": "auto",
                        "borderRadius": "10px",
                        "overflow": "hidden"
                    },
                    style_cell={
                        "textAlign": "left",
                        "padding": "8px 12px",
                        "fontFamily": "Arial",
                        "fontSize": "12px",
                        "backgroundColor": "#ffffff",
                        "border": "none",
                        "color": "#333"
                    },
                    style_header={
                        "backgroundColor": "#c4b194",
                        "fontWeight": "bold",
                        "fontSize": "13px",
                        "color": "#5c4a2f",
                        "borderBottom": "2px solid #d6c1a3"
                    },
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "#fdfaf6"},
                        {"if": {"state": "selected"}, "backgroundColor": "#f3ede4", "border": "1px solid #c9bca8"}
                    ]
                )
            ],
            id="floating-table-box",
            style={
                "display": "none",
                "position": "absolute",
                "top": "50%",
                "right": "1%",
                "width": "320px",
                "zIndex": "1000",
                "backgroundColor": "#ffffff",
                "borderRadius": "10px",
                "boxShadow": "2px 2px 8px rgba(0,0,0,0.2)",
                "padding": "10px",
                "border": "none"
            }),
        ],
        style={"position": "relative"}),

        # Tabela flutuante real (agora fixada na tela no canto inferior direito)
        

        # Tabela principal
        html.Div([
            html.H3("Restaurantes e Bares", style={
                "margin": "20px 0",
                "fontFamily": "Arial",
                "textAlign": "center",
                "color": "#444"
            }),
            dash_table.DataTable(
                id="establishments-table",
                columns=[
                    {"name": "Nome", "id": "NOME"},
                    {"name": "Endereço", "id": "ENDERECO"},
                    {"name": "Possui Alvará?", "id": "IND_POSSUI_ALVARA"},
                    {"name": "Abertura", "id": "DATA_INICIO_ATIVIDADE"},
                ],
                data=[],
                page_size=5,
                style_table={
                    "overflowX": "auto",
                    "border": "none",
                    "boxShadow": "none",
                    "width": "100%",
                    "borderRadius": "10px",
                    "overflow": "hidden"
                },
                style_cell={
                    "backgroundColor": "#ffffff",
                    "border": "none",
                    "textAlign": "left",
                    "padding": "8px 12px",
                    "fontFamily": "Arial",
                    "fontSize": "12px",
                    "color": "#333",
                    "height": "40px",
                    "whiteSpace": "normal"
                },
                style_header={
                    "backgroundColor": "#c4b194",
                    "fontWeight": "bold",
                    "fontSize": "13px",
                    "color": "#5c4a2f",
                    "borderBottom": "2px solid #d6c1a3"
                },
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": "#fdfaf6"},
                    {"if": {"state": "selected"}, "backgroundColor": "#f3ede4", "border": "1px solid #c9bca8"}
                ]
            )
        ],
        style={
            "padding": "0 5vw",
            "margin": "0 auto",
            "width": "100%",
            "boxSizing": "border-box"
        }),
        dcc.Store(id="floating-visibility", data=False)
    ],
    style={
        "backgroundColor": "#eee3d1",
        "minHeight": "100vh",
        "margin": "0",
        "padding": "0",
        "overflowX": "hidden",
        "width": "100%"
    })
