import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import json
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css']
external_scripts = ["https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
app.scripts.config.serve_locally = True

path = ''

#takes json file of network generated by networkx and pyvis
raw_data = open(path + 'data.json', 'r').read()

data = json.loads(raw_data)

for node in data['nodes']:
    node['shape'] = 'dot'

#data of when courses are offered
year_data = pd.read_csv(path + 'year.csv', index_col=0)
year_data = year_data.iloc[:, :18]
year_data.index = [year.upper() for year in year_data.index]

years_offered = list(year_data.columns[1:])

# color for legend
unselected = '#D3D3D3'
selected = '#D184C4'
future_selected = '#DB4670'
intersect_selected = '#8F1A25'

app.layout = html.Div(children=[
    dcc.Input(id='year-chooser', placeholder='input YYYYS or YYYYF'),

    html.Div(id='mynetwork'),
    html.Div(id='loading'),

    html.Div(className='legend unselected', children='not offered this sem'),
    html.Div(className='legend selected', children='only offered this sem'),
    html.Div(className='legend future_selected', children='only offered next sem'),
    html.Div(className='legend intersect_selected', children='offered both sem'),

    html.Div(id='instructions', children='only shows classes from 2018S to 2026S'),

    html.Div(id='config'),

    #use div#graph-data to store json data that will be accessed by display.js
    html.Div(id='graph-data', style={'display': 'none'}, children=json.dumps(data)),
    html.Script(src='display.js', defer=True)
])


@app.callback(Output('graph-data', 'children'),
               [Input('year-chooser', 'value')])
def color_setter(year):
    if year not in years_offered:
        for node in data['nodes']:
            node['color'] = selected
    else:
        for node in data['nodes']:
            try:
                if year_data.loc[node['id'][0:8]][year]: #if course is offered in given year
                    node['color'] = selected
                    next_sem = years_offered[years_offered.index(year) + 1]
                    if year_data.loc[node['id'][0:8]][next_sem]:
                        node['color'] = intersect_selected
                elif year_data.loc[node['id'][0:8]][next_sem]:
                    node['color'] = future_selected
                else:
                    node['color'] = unselected
            except:
                node['color'] = unselected
    return json.dumps(data)


if __name__ == '__main__':
    app.run_server(debug=True)