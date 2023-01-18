# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = JupyterDash(__name__)

unique_launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})
for launch_site in unique_launch_sites:
    launch_sites.append({'label': launch_site, 'value': launch_site})

# Create an app layout
app.layout = html.Div(children=[
    html.Div([
        html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
    ]),
    
    html.Div([
        # TASK 1: Add a Launch Site Drop-down Input Component
        dcc.Dropdown(
                id = 'site-dropdown',
                options = launch_sites,
                placeholder = 'Select a Launch Site here',
                searchable = True ,
                clearable = False,
                value = 'All Sites'
            ),
        # TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
        html.Div(dcc.Graph(id='success-pie-chart')),
    ], style={'padding': '0 30px'}),

    html.Div([
        # TASK 3: Add a Range Slider to Select Payload
        html.Div("Payload range (Kg):", 
            style={'color': '#503D36','font-size': 20, 'padding': '0 30px', 'margin-left': '11px'}
            ),
        html.Div([
            dcc.RangeSlider(
                id = 'payload_slider',
                min = 0,
                max = 10000,
                step = 1000,
                marks = {
                        0: {'label': '0 Kg', 'style': {'color': '#77b0b1'}},
                        1000: {'label': '1000 Kg'},
                        2000: {'label': '2000 Kg'},
                        3000: {'label': '3000 Kg'},
                        4000: {'label': '4000 Kg'},
                        5000: {'label': '5000 Kg'},
                        6000: {'label': '6000 Kg'},
                        7000: {'label': '7000 Kg'},
                        8000: {'label': '8000 Kg'},
                        9000: {'label': '9000 Kg'},
                        10000: {'label': '10000 Kg', 'style': {'color': '#f50'}},
                },
                value = [min_payload,max_payload]
            ),
        ], style={'padding': '40px 30px'}),

        # TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
        html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
    ]),
],style={'padding': '0 20px'})

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value')])
def update_piegraph(site_dropdown):
    if (site_dropdown== 'All Sites' or site_dropdown == 'None'):
        df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df,names = 'Launch Site',hole=.3,title = 'Total Success Launches By all sites')
    else:
        site_specific = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(site_specific,names= 'class',hole=.3,title ='Total Success Launches for site '+site_dropdown)
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload_slider',component_property='value')])

def update_scattergraph(site_dropdown,payload_slider):
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        low, high = payload_slider
        df  = spacex_df
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version Category",
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    else:
        low, high = payload_slider
        site_specific = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mask = (site_specific ['Payload Mass (kg)'] > low) & (site_specific ['Payload Mass (kg)'] < high)
        fig = px.scatter(
            site_specific [mask], x="Payload Mass (kg)", y="class",
            color="Booster Version Category",
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(mode='jupyterlab', port = 8050 ,dev_tools_ui=True,debug=True,dev_tools_hot_reload =True,threaded=True)