from dash import html, dash_table
import dash_leaflet as dl

def build_layout(geojson):
    return html.Div([
        dl.Map(children=[
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
        ], style={"padding": "20px"})
    ])