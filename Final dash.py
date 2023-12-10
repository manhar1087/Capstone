# Import required libraries

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

spacex_df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

app=dash.Dash(__name__)

app.title="SpaceX Launch Records Dashboard"

min_payload = 0
max_payload = 10000

app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 30}),
    dcc.Dropdown(id='site-dropdown',
                        options=[
                            {'label': 'All Sites', 'value': 'ALL'},
                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                        ],
                        value='ALL',
                        placeholder="Select a Lauch Site here",
                        searchable=True
                        ),
    dcc.Graph(id='success-pie-chart'),
    dcc.Markdown("#### Payload Mass (kg):"),
    dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={i: str(i) for i in range(0, 10001, 2500)},
                value=[min_payload, max_payload]),
    dcc.Graph(
        id='success-payload-scatter-chart'
    )
                        ])

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:# return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
                    
                    # Count success and failure for the selected site
        success_count = filtered_df[filtered_df['class'] == 1].shape[0]
        failure_count = filtered_df[filtered_df['class'] == 0].shape[0]
                    
                    # Create a pie chart for the selected site
        fig = px.pie(values=[success_count, failure_count], 
                                names=['Success', 'Failure'], 
                                title=f'Total Success Launches for Site {entered_site}')
        return fig

# Callback to update scatter plot based on site and payload range selection
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, selected_payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                                (spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Correlation between Payload and Success for {selected_site}')
    
    return fig

suppress_callback_exceptions=True

if __name__ == '__main__':
    app.run_server(debug=True)       