import dash_leaflet.express as dlx


def convert_df_to_geojson(df):
    items = [
        dict(name=row['NOME'], lat=row['LATITUDE'], lon=row['LONGITUDE'], endereco=row['ENDERECO']) 
        for _, row in df.iterrows()
    ]

    features = [{**item, "tooltip": item["name"], "id": i} for i, item in enumerate(items)]
    return dlx.dicts_to_geojson(features)