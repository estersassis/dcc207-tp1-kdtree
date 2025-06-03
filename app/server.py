from dash_extensions.enrich import DashProxy
import pandas as pd
from kdtree.kdtree import KDTree, Point
from app.geojson_utils import convert_df_to_geojson
from app.layout import build_layout
from app.callbacks import register_callbacks

df = pd.read_csv("data/bares_restaurantes_geocodificados.csv")

tree = KDTree([
    Point(
        point=(row["LONGITUDE"], row["LATITUDE"]),
        name=row["NOME"],
        alvara=row["IND_POSSUI_ALVARA"],
        date=row["DATA_INICIO_ATIVIDADE"],
        address=row["ENDERECO"]
    ) for _, row in df.iterrows()
])

geojson = convert_df_to_geojson(df)

app = DashProxy()
app.layout = build_layout(geojson)
register_callbacks(app, tree, df.to_dict("records"))

if __name__ == "__main__":
    app.run()
