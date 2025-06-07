from dash import html, dash_table, dcc, Output, Input, State, ctx
import dash_leaflet as dl

def build_layout(geojson):
    return html.Div([
        dl.Map(id="mapa", children=[
            dl.TileLayer(),
            dl.FeatureGroup([
                dl.EditControl(
                    id="edit_control",
                    draw={"rectangle": True, "marker": False, "circle": False, "polyline": False, "polygon": False, "circlemarker": False},
                    editToolbar=False
                )
            ]),
            dl.GeoJSON(data=geojson, cluster=True, zoomToBoundsOnClick=True)
        ], style={"height": "65vh", "width": "100vw"}, center=[-19.92, -43.94], zoom=17),

        html.Button("Mostrar/Esconder Tabela", id="btn-toggle-tabela-flutuante", n_clicks=0,
                    style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"}),

        # Tabela flutuante (nova) — começa escondida
        html.Div([
            dash_table.DataTable(
                id="tabela-flutuante",
                columns=[
                    {"name": "NOME", "id": "NOME"}
                ],
                data=[],
                page_size=5,
                style_table={"maxHeight": "200px", "overflowY": "auto"},
                style_cell={"textAlign": "left", "padding": "5px"},
                style_header={"fontWeight": "bold"},
            )
        ],
            id="caixa-tabela-flutuante",
            style={
                "display": "none",
                "position": "absolute",
                "top": "60px",
                "right": "10px",
                "width": "250px",
                "zIndex": "1000",
                "backgroundColor": "white",
                "border": "1px solid #ccc",
                "borderRadius": "5px",
                "boxShadow": "2px 2px 5px rgba(0,0,0,0.3)",
                "padding": "10px"
            }
        ),

        html.Div([
            html.H3("Restaurantes e Bares", style={"margin": "10px 0"}),
            dash_table.DataTable(
                id="tabela-estabelecimentos",
                columns=[
                    {"name": "NOME", "id": "NOME"},
                    {"name": "ENDEREÇO", "id": "ENDERECO"},
                    {"name": "POSSUI ALVARÁ?", "id": "IND_POSSUI_ALVARA"},
                    {"name": "DATA DE ABERTURA", "id": "DATA_INICIO_ATIVIDADE"},
                ],
                data=[],
                page_size=5,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "padding": "5px"},
                style_header={"fontWeight": "bold"},
            )
        ], style={"padding": "20px"}),

        dcc.Store(id="visibilidade-flutuante", data=False)
    ])