from dash_extensions.enrich import Output, Input, State
import dash


def register_callbacks(app, tree, data_default, data_default_buteco):
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
        State("visibilidade-flutuante", "data"),
        prevent_initial_call=True
    )
    def toggle_tabela_flutuante(n, visivel):
        novo_visivel = not visivel
        style = {
            "display": "block" if novo_visivel else "none",
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
        if not novo_visivel:
            style["display"] = "none"
        return style, novo_visivel, data_default_buteco
    
    @app.callback(
        Output("mapa", "center"),
        Output("mapa", "zoom"),
        Input("tabela-flutuante", "active_cell"),
        State("tabela-flutuante", "data"),
        prevent_initial_call=True
    )
    def focar_no_estabelecimento(active_cell, data):
        if not active_cell:
            raise dash.exceptions.PreventUpdate

        linha = active_cell["row"]
        if linha >= len(data):
            raise dash.exceptions.PreventUpdate

        lat = data[linha].get("LATITUDE")
        lon = data[linha].get("LONGITUDE")

        if lat is None or lon is None:
            raise dash.exceptions.PreventUpdate

        return [lat, lon], 20  # zoom máximo (ajuste conforme necessário)
