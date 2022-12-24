import webbrowser

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType

from tinydb import TinyDB

db = TinyDB('./city_fly.json')

ci_t = db.table('city_index')
ci_l = db.table('city_line')

c = (
    Geo()
    .add_schema(
        maptype="china",
        itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="#111"),
    )
    .add(
        "",
        [(cit['city'], cit['index']) for cit in ci_t.all()],
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
    .add(
        "geo",
        [(cit['from'], cit['to']) for cit in ci_l.all()],
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="blue"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Lines-background"))
    .render("geo_lines_background.html")
)



webbrowser.open(url='geo_lines_background.html')
