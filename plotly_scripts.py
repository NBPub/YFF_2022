import pandas as pd
import numpy as np
rng = np.random.default_rng()

import plotly.graph_objects as go
import plotly.express as px
from plotly.figure_factory import create_distplot


# Overall
pos_order = ['QB', 'RB', 'WR', 'TE']

def overall_box_graph(data):
    fig = px.box(data, x="Fantasy Pts", notched=True, y='Position', color='Position', points='all',
                hover_data=['Name','Team','Fantasy Pts','GP','Rankings_Actual'],
                category_orders={'Position':pos_order},
                 )
    fig.update_traces(hovertemplate='<b>%{customdata[0]} (%{customdata[1]})</b>\
    <br>%{x:.0f} pts | %{customdata[2]} games | rank %{customdata[3]}')
    
    fig.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>Fantasy Performance vs Position, 2022</b><br>\
<span style="font-size:0.7em;">{" | ".join([f"{data[data.Position==val].shape[0]} {val}" for val in pos_order])}</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
        'showlegend':False,
        'xaxis.title':'Fantasy Points',
        'xaxis.title.font.size':24,
        'xaxis.gridwidth':3,
        'xaxis.gridcolor':'aliceblue',
        'xaxis.tickfont.size':16,
        'yaxis.title':'',
        'yaxis.tickfont.size':16,
        'yaxis.ticks':'outside',
        'yaxis.tickcolor':'#111111',
})    
    return fig


def position_box_graph(df, position, pergame):
    
    # suppress pandas chained assignment warning
    pd.set_option('mode.chained_assignment',None)

    # base figure, add boxplot and scatter traces
    base = go.Figure()
    
    # y jitter
    # df.loc[:,'y'] = np.zeros(df.shape[0])
    df.loc[:,'y'] = rng.uniform(low=-1, high=1, size=df.shape[0])*.2
    
    # hover_data based on position
    hover_data=['Name','Team','Fantasy Pts', 'Rankings_Actual', 'GP']
    
    if pergame:
        df['Fantasy Pts'] = df['Fantasy Pts'].div(df.GP,axis=0)
        df[df.columns[6:19]] = df[df.columns[6:19]].div(df.GP, axis=0) 
        df[df.columns[6:19]] = df[df.columns[6:19]].round(1)
        template = '<b>%{customdata[0]} (%{customdata[1]})</b><br>%{x:.1f} pts '
    else:
        template = '<b>%{customdata[0]} (%{customdata[1]})</b><br>%{x:.0f} pts '
    
    
    pos_stats = {'QB':'Passing', 'RB':'Rushing', 
                 'WR':'Receiving','TE':'Receiving'}
    pos_cols = df.columns[df.columns.str.startswith(pos_stats[position])]
    hover_data.extend(pos_cols)
    if position == 'RB':
        hover_data.extend(df.columns[df.columns.str.startswith('Receiving')])
    elif position == 'QB':
        hover_data.extend(df.columns[df.columns.str.startswith('Rushing')])
    
    if position == 'QB':
        template =''.join([template, '| %{customdata[3]} games\
<br>%{customdata[4]} yd, %{customdata[5]} td, %{customdata[6]} int\
<br>%{customdata[7]} rush, %{customdata[8]} yd, %{customdata[9]} td<br>'])
    
    elif position == 'RB':
        template =''.join([template, '| %{customdata[3]} games\
<br>%{customdata[4]} att, %{customdata[5]} yd, %{customdata[6]} td\
<br>%{customdata[7]} rec, %{customdata[10]} tgt, %{customdata[8]} yd<br>'])
    
    else:
        template =''.join([template, '| %{customdata[3]} games\
<br>%{customdata[5]} yd, %{customdata[6]} td\
<br>%{customdata[4]} rec, %{customdata[7]} targets<br>'])
    
    template = ''.join([template, 'Final ranking: %{customdata[2]}<extra></extra>'])
    
    # scatter for individual points with team-based colors
    points = px.scatter(df, x='Fantasy Pts', y='y', color='Name',
                        hover_data=hover_data
                       ).data
    for val in points:
        # print(val)
        ind = df[df.Name == val.name].index.values[0]
        mark = val.marker
        mark['color'] = df.loc[ind,'c1']
        mark['line'] = dict(color=df.loc[ind,'c2'], width=1)
        mark['size'] = 15
        val['hovertemplate'] = template
        val.marker = mark
        base.add_trace(val)

    box = go.Figure(data=[go.Box(x=df['Fantasy Pts'],
                fillcolor='lavenderblush', boxmean=True,
                opacity=0.8, hoverinfo='skip', boxpoints='outliers',
                  )]).data

    base.add_trace(box[0])
    base.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>{position} Fantasy Performance{" per game" if pergame else ""}, 2022</b><br><span style="font-size:0.7em;">top {df.shape[0]} scorers</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
        'showlegend':False,
        'xaxis.title':f'Fantasy Points{" per game" if pergame else ""}',
        'xaxis.title.font.size':24,
        'xaxis.gridwidth':3,
        'xaxis.gridcolor':'aliceblue',
        'xaxis.tickfont.size':16,
        'yaxis.color':'#111111',
    })
    return base

def overall_histogram_1(data):
    fig = px.histogram(data, x="Fantasy Pts", color="Position", marginal="rug",
                       hover_data=['Name','Team','Fantasy Pts','GP','Rankings_Actual'],
                       category_orders={'Position':pos_order}, barmode='group', 
                       histnorm='probability density')
    
    for val in fig.data:
        if 'boxpoints' in val:
            val['hovertemplate'] = '<b>%{customdata[0]} (%{customdata[1]})</b>\
    <br>%{x:.0f} pts | %{customdata[2]} games | rank %{customdata[3]}'
            
    fig.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>Fantasy Distribution vs Position, 2022</b><br>\
<span style="font-size:0.7em;">{" | ".join([f"{data[data.Position==val].shape[0]} {val}" for val in pos_order])}</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
        'xaxis.title':'Fantasy Points',
        'xaxis.title.font.size':24,
        'yaxis.title':'Count',
        'yaxis.title.font.size':24,    
        'yaxis.ticks':'outside',
        'yaxis.tickcolor':'#111111',
    })    
    return fig

def rug_texter(info):
    new_text = []
    for customdata in info:
        new_text.append(f'<b>{customdata[0]} ({customdata[1]})</b>\
<br>{customdata[2]:.0f} pts | {customdata[3]} games | rank {customdata[4]}')
    return new_text

def overall_histogram_2(data):
    fig = create_distplot([data[data.Position == val]['Fantasy Pts'].values \
                           for val in pos_order], pos_order, bin_size=10,
          colors = ['#636efa','#00cc96','#EF553B','#ab63fa'], curve_type='normal',
          rug_text = [rug_texter(data[data.Position == val]\
                     [['Name','Team','Fantasy Pts','GP','Rankings_Actual']]\
                     .values.tolist()) for val in pos_order])
    
    fig.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>Fantasy Distribution vs Position, 2022</b><br>\
    <span style="font-size:0.7em;">{" | ".join([f"{data[data.Position==val].shape[0]} {val}" for val in pos_order])}</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
        'xaxis.title':'Fantasy Points',
        'xaxis.title.font.size':24,
        'yaxis.color':'#111111',
    })    
    return fig

# WR/TE
def wr_te_graphs(df, col):
    hover_data=['Name', 'Team', 'Fantasy Pts', 'Rankings_Actual', 'GP']
    hover_data.extend(df.columns[df.columns.str.startswith('Receiving')])
    pos = df.Position.values[0]
    
    if col == 'Receiving_Tgt':
        title_text = "Targets"
        hovertemplate = '<b>%{customdata[0]} (%{customdata[1]})</b><br>%{y:.0f} pts | %{customdata[3]} games\
    <br>%{customdata[5]} yd, %{customdata[6]} td\
    <br>%{customdata[4]} rec, %{x} targets\
    <br>Final ranking: %{customdata[2]}'
    else:
        title_text = "Receptions"
        hovertemplate = '<b>%{customdata[0]} (%{customdata[1]})</b><br>%{y:.0f} pts | %{customdata[3]} games\
    <br>%{customdata[4]} yd, %{customdata[5]} td\
    <br>%{x} rec, %{customdata[6]} targets\
    <br>Final ranking: %{customdata[2]}'

    fig = px.scatter(df, x=col, y='Fantasy Pts', hover_data=hover_data, 
                      trendline='ols', trendline_scope='overall', trendline_color_override='black',
                      size='Receiving_Yds', color='Receiving_TD', color_continuous_scale='jet_r',
                      labels={'Receiving_TD':'Rec TD'})
    for val in fig.data:
        if val.name == 'Overall Trendline': 
            continue
        val['hovertemplate'] = hovertemplate
        
    fig.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>{pos} Fantasy Performance vs {title_text}, 2022</b><br><span style="font-size:0.7em;">top {df.shape[0]} scorers</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
        'showlegend':False,
        'xaxis.title':title_text,
        'xaxis.title.font.size':24,
        'xaxis.tickfont.size':16,
        'yaxis.title.font.size':24,   
        'yaxis.tickfont.size':16,
        'yaxis.ticks':'outside',
        'yaxis.tickcolor':'#111111',
    })   
    
    return fig

def rb_graphs(df):
    df['Receiving Pts'] = df['Receiving_Yds']*.1 + df['Receiving_TD']*6 + df['Receiving_Rec']*1
    df['Rushing Pts'] = df['Rushing_Yds']*.1 + df['Rushing_TD']*6  
    
    fact_check = np.sum(df['Receiving Pts'] + df['Rushing Pts'])/np.sum(df['Fantasy Pts'])
    
    # 2d
    fig2d = px.scatter(df, x='Receiving Pts', y='Rushing Pts', color='Fantasy Pts', size='Fantasy Pts', color_continuous_scale='jet_r',
                    hover_data=['Name', 'Team', 'Fantasy Pts', 'Rankings_Actual'])
    
    fig2d.update_traces(hovertemplate='<b>%{customdata[0]} (%{customdata[1]})</b>\
    <br>%{x:.0f} rec | %{y:.0f} rush\
    <br>%{customdata[2]:.0f} pts | rank %{customdata[3]}')
    
    line = dict(color='black',width=2,dash='dash')
    fig2d.add_trace(go.Scatter(x=[df['Receiving Pts'].mean(),df['Receiving Pts'].mean()], y = [0,df['Rushing Pts'].max()], line=line, showlegend=False))
    fig2d.add_trace(go.Scatter(x=[0,df['Receiving Pts'].max()], y = [df['Rushing Pts'].mean(),df['Rushing Pts'].mean()], line=line, showlegend=False))
    
    fig2d.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>Receiving Contribution to RB Fantasy Performance, 2022</b><br><span style="font-size:0.7em;">top {df.shape[0]} scorers</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
        'xaxis.title.font.size':24,
        'yaxis.title.font.size':24,
        'xaxis.tickfont.size':16,
        'yaxis.tickfont.size':16,
        'yaxis.ticks':'outside',
        'yaxis.tickcolor':'#111111',
    }) 
    # 3d
    fig3d = px.scatter_3d(df, y='Receiving Pts', x='Rushing Pts', z='Fantasy Pts', color='Receiving Pts', size='Fantasy Pts', color_continuous_scale='jet_r',
                hover_data=['Name', 'Team', 'Fantasy Pts', 'Rankings_Actual'],)

    fig3d.update_traces(hovertemplate='<b>%{customdata[0]} (%{customdata[1]})</b>\
    <br>%{y:.0f} rec | %{x:.0f} rush\
    <br>%{z:.0f} pts | rank %{customdata[2]}')
    
    fig3d.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>Receiving Contribution to RB Fantasy Performance, 2022</b><br><span style="font-size:0.7em;">top {df.shape[0]} scorers</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
    })
    
    return fig2d, fig3d, fact_check
    

def qb_graphs(df):
    df['Passing Pts'] = df['Passing_Yds']*.04 + df['Passing_TD']*4 + df['Passing_Int']*-2
    df['Rushing Pts'] = df['Rushing_Yds']*.1 + df['Rushing_TD']*6 + df['Fum_Lost']*-2 
    
    fact_check = np.sum(df['Passing Pts'] + df['Rushing Pts'])/np.sum(df['Fantasy Pts'])
    
    # 2d
    fig2d = px.scatter(df, x='Rushing Pts', y='Passing Pts', color='Fantasy Pts', size='Fantasy Pts', color_continuous_scale='jet_r',
                    hover_data=['Name', 'Team', 'Fantasy Pts', 'Rankings_Actual'])
    
    fig2d.update_traces(hovertemplate='<b>%{customdata[0]} (%{customdata[1]})</b>\
    <br>%{x:.0f} rush | %{y:.0f} pass\
    <br>%{customdata[2]:.0f} pts | rank %{customdata[3]}')
    
    line = dict(color='black',width=2,dash='dash')
    fig2d.add_trace(go.Scatter(x=[df['Rushing Pts'].mean(),df['Rushing Pts'].mean()], y = [0,df['Passing Pts'].max()], line=line, showlegend=False))
    fig2d.add_trace(go.Scatter(x=[0,df['Rushing Pts'].max()], y = [df['Passing Pts'].mean(),df['Passing Pts'].mean()], line=line, showlegend=False))
    
    fig2d.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>Rushing Contribution to QB Fantasy Performance, 2022</b><br><span style="font-size:0.7em;">{"&nbsp;"*3} top {df.shape[0]} scorers</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
        'xaxis.title.font.size':24,
        'yaxis.title.font.size':24,
        'xaxis.tickfont.size':16,
        'yaxis.tickfont.size':16,
        'yaxis.ticks':'outside',
        'yaxis.tickcolor':'#111111',
    })    
    # 3d
    fig3d = px.scatter_3d(df, y='Rushing Pts', x='Passing Pts', z='Fantasy Pts', color='Rushing Pts', size='Fantasy Pts', color_continuous_scale='jet_r',
                    hover_data=['Name', 'Fantasy Pts', 'Team', 'Rankings_Actual'])
    
    fig3d.update_traces(hovertemplate='<b>%{customdata[0]} (%{customdata[1]})</b>\
    <br>%{y:.0f} rush | %{x:.0f} pass\
    <br>%{z:.0f} pts | rank %{customdata[2]}')
    
    fig3d.update_layout({
        'font.color':'aliceblue',
        'title':f'<b>Rushing Contribution to QB Fantasy Performance, 2022</b><br><span style="font-size:0.7em;">top {df.shape[0]} scorers</span>',
        'title.font.size':20,
        'plot_bgcolor':'silver',
        'paper_bgcolor':'#111111',
    })
    
    return fig2d, fig3d, fact_check