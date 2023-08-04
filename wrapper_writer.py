from pathlib import Path
import pandas as pd
from plotly_scripts import overall_box_graph, position_box_graph, \
    overall_histogram_1, overall_histogram_2, wr_te_graphs, rb_graphs, qb_graphs


    # Read Data, Make Graphs, Save as HTML
data = pd.read_parquet(Path('data', 'all_Off.parquet'))
folder = Path('templates','figures')

# overall
fig = overall_box_graph(data)
fig.write_html(Path(folder,'overall_box.html'), include_plotlyjs='cdn')

fig = overall_histogram_1(data)
fig.write_html(Path(folder,'overall_hist1.html'), include_plotlyjs='cdn')

fig = overall_histogram_2(data)
fig.write_html(Path(folder,'overall_hist2.html'), include_plotlyjs='cdn')

# position breakdowns
for position in ['QB','RB','WR','TE']:
    for pergame in [False, True]:
        fig = position_box_graph(data[data.Position == position], position, pergame)
        fig.write_html(Path(folder, f'{position}_{"pergame" if pergame else "total"}_2022.html'))

# wr
df = data[data.Position == 'WR'].copy()
fig = wr_te_graphs(df, 'Receiving_Tgt')
fig.write_html(Path(folder,'targets_wr.html'), include_plotlyjs='cdn')
fig = wr_te_graphs(df, 'Receiving_Rec')
fig.write_html(Path(folder,'receptions_wr.html'), include_plotlyjs='cdn')

# te
df = data[data.Position == 'TE'].copy()
fig = wr_te_graphs(df, 'Receiving_Tgt')
fig.write_html(Path(folder,'targets_te.html'), include_plotlyjs='cdn')
fig = wr_te_graphs(df, 'Receiving_Rec')
fig.write_html(Path(folder,'receptions_te.html'), include_plotlyjs='cdn')

# rb
df = data[data.Position == 'RB'].copy()
fig2d, fig3d, fact_check_rb = rb_graphs(df)
fig2d.write_html(Path(folder,'2d_rb.html'), include_plotlyjs='cdn')
fig3d.write_html(Path(folder,'3d_rb.html'), include_plotlyjs='cdn')

# qb
df = data[data.Position == 'QB'].copy()
fig2d, fig3d, fact_check_qb = qb_graphs(df)
fig2d.write_html(Path(folder,'2d_qb.html'), include_plotlyjs='cdn')
fig3d.write_html(Path(folder,'3d_qb.html'), include_plotlyjs='cdn')

del df, data, fig2d, fig3d, fig

# # hardcode after initial graph creation
# fact_check_rb = 0.9846136926236232
# fact_check_qb = 0.9843381428485901



    # Write HTML and other info into Jinja Template
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment( 
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
from datetime import datetime

date = datetime.now().strftime('%x %X')
# write to template and save
template = env.get_template('base_template.html')
with open(Path('index.html'), 'w', encoding='utf-8') as page:
    page.write(template.render(date=date, fact_check_rb=fact_check_rb, fact_check_qb=fact_check_qb))