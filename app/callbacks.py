from dash_extensions.enrich import Output, Input, State
import dash_leaflet.express as dlx
import dash_leaflet as dl
import dash
from dash import html, no_update, ctx

ultimo_click = -1

def register_callbacks(app, tree, geojson_original, data_default, data_default_buteco):
    @app.callback(
        Output("tabela-estabelecimentos", "data"),
        Input("edit_control", "geojson")
    )
    def filtrar_por_area(geojson):
        if not geojson or not geojson.get("features"):
            return data_default

        coords = geojson["features"][0]["geometry"]["coordinates"][0]
        lons = [p[0] for p in coords]
        lats = [p[1] for p in coords]
        lon_min, lon_max = min(lons), max(lons)
        lat_min, lat_max = min(lats), max(lats)

        pontos = tree.search([(lon_min, lat_min), (lon_max, lat_max)])
        return [{"NOME": p.name, "ENDERECO": p.address, "IND_POSSUI_ALVARA": p.alvara, "DATA_INICIO_ATIVIDADE": p.date} for p in pontos]

    @app.callback(
        Output("caixa-tabela-flutuante", "style"),
        Output("visibilidade-flutuante", "data"),
        Output("tabela-flutuante", "data"),
        Input("btn-toggle-tabela-flutuante", "n_clicks"),
        State("btn-toggle-tabela-flutuante", "n_clicks_timestamp"),
        State("visibilidade-flutuante", "data"),
        prevent_initial_call=True
    )
    def toggle_tabela_flutuante(n_clicks, ts, visivel):
        global ultimo_click

        if ts == ultimo_click:
            return no_update, no_update, no_update

        if ctx.triggered_id != "btn-toggle-tabela-flutuante":
            raise dash.exceptions.PreventUpdate

        if ts == ultimo_click:
            print("Clique duplicado ignorado.")
            raise dash.exceptions.PreventUpdate
        
        ultimo_click = ts
        novo_visivel = not visivel

        style = {
            "display": "block" if novo_visivel else "none",
            "position": "absolute",
            "top": "50%",
            "right": "1%",
            "width": "20em",
            "maxWidth": "90vw",
            "zIndex": "1000",
            "backgroundColor": "#ffffff",
            "borderRadius": "10px",
            "boxShadow": "2px 2px 8px rgba(0,0,0,0.2)",
            "padding": "10px",
            "border": "none"
        }

        return style, novo_visivel, data_default_buteco
    
    @app.callback(
        Output("marcador-selecionado", "children"),
        Input("tabela-flutuante", "selected_cells"),
        State("tabela-flutuante", "data"),
        prevent_initial_call=True
    )
    def destacar_estabelecimento(selected_cells, data):
        if not selected_cells:
            raise dash.exceptions.PreventUpdate

        cell = selected_cells[0]
        row = cell.get("row")
        
        if row is None or row >= len(data):
            raise dash.exceptions.PreventUpdate

        lat = data[row].get("LATITUDE")
        lon = data[row].get("LONGITUDE")
        nome = data[row].get("NOME")
        address = data[row].get("ENDERECO")

        if lat is None or lon is None:
            raise dash.exceptions.PreventUpdate
        
        custom_icon = dict(
            iconUrl="https://cdb-static-files.s3.amazonaws.com/wp-content/uploads/2022/03/25112702/logo-comida-di-buteco.webp",
            iconSize=[60, 43]
        )

        return [
            dl.Marker(
                position=[lat, lon],
                icon=custom_icon,
                zIndexOffset=1000,
                children=[
                    dl.Popup(
                        html.Div([
                            html.Img(src=data[row].get("IMG_URL"), style={"width": "100%", "borderRadius": "10px"}),
                            html.H4(nome, style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.P(address, style={"fontSize": "12px", "margin": 0, "color": "#555"}),
                            html.Hr(),
                            html.B("🍽 Prato: "), html.Span(data[row].get("PRATO", "Não informado")),
                            html.Br(),
                            html.B("📞 Telefone: "), html.Span(data[row].get("TELEFONE", "Não informado")),
                            html.Br(),
                            html.P(data[row].get("DESCRICAO", ""), style={"marginTop": "10px", "fontStyle": "italic", "fontSize": "13px", "color": "#444"})
                        ], style={
                            "maxWidth": "250px",
                            "fontFamily": "Arial",
                            "padding": "5px"
                        }),
                        autoPan=True
                    )
                ]
            )
        ]
