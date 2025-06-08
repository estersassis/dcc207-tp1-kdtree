def convert_df_to_geojson(df):
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["LONGITUDE"], row["LATITUDE"]],
            },
            "properties": {
                "NOME": row["NOME"],
                "ENDERECO": row["ENDERECO"],
                "popup": f"<b>{row['NOME']}</b><br>{row['ENDERECO']}"
            }
        }
        for i, row in df.iterrows()
    ]
    geojson = {"type": "FeatureCollection", "features": features}
    return geojson
