from dash_extensions.enrich import Output, Input

def register_callbacks(app, tree, data_default):
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
