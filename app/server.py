from dash_extensions.enrich import DashProxy
import pandas as pd
from kdtree.kdtree import KDTree, Point
from app.geojson_utils import convert_df_to_geojson
from app.layout import build_layout
from app.callbacks import register_callbacks

df = pd.read_csv("data/bares_restaurantes_geocodificados.csv")
df_buteco = pd.read_csv("data/comida_di_buteco_corrigido.csv")

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
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background-color: #eee3d1;
                overflow-x: hidden;
                overflow-y: visible;
            }

            #_dash-app-content {
                margin: 0 !important;
                padding: 0 !important;
                width: 100%;
                box-sizing: border-box;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = build_layout(geojson)
register_callbacks(app, tree, df.to_dict("records"), df_buteco.to_dict("records"))

if __name__ == "__main__":
    app.run()
