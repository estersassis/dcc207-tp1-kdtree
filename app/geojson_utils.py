def convert_df_to_geojson(df):
    """
    Converte um DataFrame contendo informações de estabelecimentos em um objeto GeoJSON.
    """
    
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
