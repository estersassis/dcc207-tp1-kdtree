import dash_leaflet as dl
import dash_leaflet.express as dlx
import pandas as pd
from dash_extensions.enrich import DashProxy, html, Output, Input

def convert_df_to_geojson(df):
    items = [
        dict(name=row['NOME'], lat=row['LATITUDE'], lon=row['LONGITUDE']) 
        for index, row in df.iterrows()
    ]

    features = [
        {**item, "tooltip": item["name"], "id": i}
        for i, item in enumerate(items)
    ]

    geojson = dlx.dicts_to_geojson(features)
    return geojson


df = pd.read_csv("bares_restaurantes_geocodificados.csv")
geojson = convert_df_to_geojson(df)

app = DashProxy()
app.layout = html.Div(
    [
        dl.Map(
            children=[
                dl.TileLayer(),
                dl.GeoJSON(
                    data=geojson,
                    cluster=True,
                    zoomToBoundsOnClick=True
                )
            ],
            style={"height": "100vh", "width": "100vw"},
            center=[-19.92, -43.94],
            zoom=17,
        ),
    ],
    style={"margin": "0", "padding": "0"}
)

if __name__ == "__main__":
    app.run()
