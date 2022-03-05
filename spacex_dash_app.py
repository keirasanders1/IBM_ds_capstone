# Import required libraries
import pandas as pd
import dash
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("C:\\Users\\keira\\IBM_data_science\\capstone_project\\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites.append('All_sites')

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),
                                html.Div(dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label':i,'value': i} for i in launch_sites],
                                    placeholder='Select site',value='All_sites'
                                )),                                
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                html.Br(),
                                html.Div(dcc.RangeSlider(id='payload-slider', min=0,max=10000,
                                step=1000,value=[min_payload,max_payload],
                                marks={0:'0',2500:'2500',5000:'5000',7500:'7500',10000:'10000'},
                                tooltip={'placement':'bottom','always_visible':True})
                                ),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output('success-pie-chart','figure'),
    Output('success-payload-scatter-chart','figure'),
    Input('site-dropdown','value'),
    Input('payload-slider','value'))

def create_graphs(launch_site,payload_range):
    if launch_site == 'All_sites':
        #pie chart of success rate for each launch site
        launch_data = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        fig1 = px.pie(launch_data,values='class',names='Launch Site',title='Success rate by launch site')

        #scatter plot of payload mass by class for selected payload range
        scatter_data = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_range[0]) & (spacex_df['Payload Mass (kg)']<=payload_range[1])]
        fig2 = px.scatter(scatter_data,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        
        return[fig1,fig2]
    else:
        #return pie chart of success/failure for just the 1 site
        df = spacex_df[spacex_df['Launch Site'] == launch_site]
        pie_data = df.groupby('class')['class'].count().to_frame()
        pie_data = pie_data.rename(columns={'class':'Total_missions'}).reset_index()
        fig1 = px.pie(pie_data,values='Total_missions',names='class',title='Success/Failure rate for site: '+launch_site)
        
        #scatter plot of payload mass by class for selected payload range and launch site
        scatter_data = df[(df['Payload Mass (kg)']>=payload_range[0]) & (df['Payload Mass (kg)']<=payload_range[1])]
        fig2 = px.scatter(scatter_data,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        
        return[fig1,fig2]

# Run the app
if __name__ == '__main__':
    app.run_server()
